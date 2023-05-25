from typing import Optional
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse, Http404
from django.views import generic, View
from django.views.generic.edit import FormView
from django.views.decorators.http import require_GET
from dotenv import load_dotenv
from json import JSONDecodeError
from django.http import JsonResponse
from django.core import serializers
from rest_framework.parsers import JSONParser
from rest_framework import views, status
from rest_framework.response import Response
from django.db.models import Q
from .models import Livestream, CustomUser
from .serializers import *
from .forms import *

import ffmpeg
import os

load_dotenv() # load environment variables from .env file

class SearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        if query:
            search_results = Livestream.objects.filter(
                Q(title__icontains=query) |
                Q(created_by__username__icontains=query)
            )
            data = LivestreamSerializer(search_results, many=True).data
        else:
            data = LivestreamSerializer(Livestream.objects.all(), many=True).data
        return JsonResponse(data, safe=False)
    
class DashboardView(generic.ListView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        context['users'] = CustomUser.objects.all()
        context['livestreams'] = Livestream.objects.all()
        context['is_authenticated'] = self.request.user.is_authenticated
        context['username'] = self.request.user.username if self.request.user.is_authenticated else ''
        context['viewports'] = self.request.user.viewports.all() if self.request.user.is_authenticated else ''
        return context
    
    def get_queryset(self):
        return Livestream.objects.all()

class StreamView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
    template_name = "dashboard/stream.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['username'] = self.request.user.username if self.request.user.is_authenticated else ''
        livestreams = Livestream.objects.all()
        context['livestreams'] = livestreams
        context['hls_links'] = {livestream.id: livestream.hls for livestream in livestreams if livestream.hls}
        return context
    
    def test_func(self):
        return self.request.user.groups.filter(name='Theia').exists()
    
    def handle_no_permission(self):
        raise Http404("You are not authorized to view this page")

class GroupView(generic.DetailView):
    model = Group
    template_name = "dashboard/group_homepage.html"

    def invite_user(request, group_id):
        group = Group.objects.get(pk=group_id)

        if request.method == 'POST':
            form = InviteUserForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                user = CustomUser.objects.get(email=email)
                group.members.add(user)
                group.save()
                messages.success(request, f'User {user} invited to {group.name}!')
                return redirect('dashboard:group_homepage', pk=group_id)
        else:
            form = InviteUserForm()

        return render(request, 'dashboard/invite_user.html', {'form': form, 'group': group})

class ViewportView(generic.DetailView):
    model = Viewport
    template_name = "dashboard/viewport.html"
    
    # get the most recent viewport created by the user
    def get_object(self):
        user_id = self.kwargs['user_id']
        viewport_id = self.kwargs['viewport_id']
        return Viewport.objects.filter(user__id=user_id, id=viewport_id).latest('time_created')
    
    # return pk as the pk of the most recent viewport created by the user
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_id'] = self.kwargs['user_id']
        context['viewport_id'] = self.kwargs['viewport_id']
        return context
    
    def post(request):
        if request.method == 'POST':
            try:
                data = JSONParser().parse(request)
                serializer = ViewportSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
                return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except JSONDecodeError:
                return JsonResponse({"status": "error", "message": "No data provided"}, status=400)
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
    
    def delete(request, viewport_id):
        viewport = Viewport.objects.get(pk=viewport_id)
        viewport.delete()
        return JsonResponse({"status": "success", "message": "Viewport deleted"}, status=200)

class UserView(LoginRequiredMixin, FormView):
    model = CustomUser
    template_name = "dashboard/user_homepage.html" 
    form_class = LivestreamVisibilityForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    # make success_url stay on the same page
    def get_success_url(self):
        return reverse('dashboard:user_homepage')
    
    # def form_valid(self, form):
    #     livestream_id = form.cleaned_data.get('livestream_id')
    #     livestream = Livestream.objects.get(pk=livestream_id)
    #     livestream.groups.set(form.cleaned_data.get('groups'))
    #     livestream.save()
    #     return super().form_valid(form)
    
    def stop_stream(request, livestream_id):
        try:
            livestream = Livestream.objects.get(pk=livestream_id)
            if livestream in request.user.created_livestreams.all():
                livestream.delete()
                return JsonResponse({"status": "success"}, status=200)
            else:
                return JsonResponse({"status": "error", "message": "Livestream not found in user's livestreams"}, status=404)
        except Livestream.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Livestream not found"}, status=404)

class LivestreamVisibilityView(LoginRequiredMixin, FormView):
    model = Livestream
    template_name = "dashboard/user_homepage.html" 
    form_class = LivestreamVisibilityForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    # make success_url stay on the same page
    def get_success_url(self):
        return reverse('dashboard:user_homepage')
    
    def form_valid(self, form):
        livestream_id = form.cleaned_data.get('livestream_id')
        livestream = Livestream.objects.get(pk=livestream_id)
        livestream.groups.set(form.cleaned_data.get('groups'))
        livestream.save()
        return super().form_valid(form)

class LoginView(auth_views.LoginView):
    model = CustomUser
    template_name = "dashboard/login.html"

    def get_success_url(self):
        # redirect to /dashboard/
        return reverse('dashboard:dashboard')

class UserAPIView(LoginRequiredMixin, views.APIView):
    serializer_class = CustomUserSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
            }
    
    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)
    
    def post(self, request):
        try:
            data = JSONParser().parse(request)
            serializer = CustomUserSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)
        
class StreamAPIView(LoginRequiredMixin, views.APIView):
    serializer_class = LivestreamSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
            }
    
    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)
    
    def post(self, request):
        try:
            data = JSONParser().parse(request)
            serializer = LivestreamSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)