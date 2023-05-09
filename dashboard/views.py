from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import generic, View
from django.views.generic.edit import FormView
from dotenv import load_dotenv
from json import JSONDecodeError
from rest_framework.parsers import JSONParser
from rest_framework import views, status
from rest_framework.response import Response
from .models import Agency, Livestream, CustomUser
from .serializers import *
from .forms import *

import os

load_dotenv() # load environment variables from .env file

class DashboardView(generic.ListView):
    template_name = "dashboard/map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['agencies'] = Agency.objects.all()
        context['users'] = CustomUser.objects.all()
        context['livestreams'] = Livestream.objects.all()
        context['is_authenticated'] = self.request.user.is_authenticated
        context['username'] = self.request.user.username if self.request.user.is_authenticated else ''
        return context
    
    def get_queryset(self):
        return MapChoice.objects.all()
    
def stream(request):
    return render(request, 'dashboard/stream.html')

def invite_user(request, agency_id):
    agency = Agency.objects.get(pk=agency_id)

    if request.method == 'POST':
        form = InviteUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = CustomUser.objects.get(email=email)
            agency.members.add(user)
            agency.save()
            messages.success(request, f'User {user} invited to {agency.name}!')
            return redirect('dashboard:agency_homepage', pk=agency_id)
    else:
        form = InviteUserForm()

    return render(request, 'dashboard/invite_user.html', {'form': form, 'agency': agency})

class AgencyView(generic.DetailView):
    model = Agency
    template_name = "dashboard/agency_homepage.html"

class ViewportView(generic.DetailView):
    model = Viewport
    template_name = "dashboard/viewport.html"

    # get the most recent viewport created by the user
    def get_object(self):
        return Viewport.objects.filter(user=self.request.user).latest('time_created')
    
    # return pk as the pk of the most recent viewport created by the user
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.get_object().pk
        return context

class UserView(LoginRequiredMixin, FormView):
    model = CustomUser
    template_name = "dashboard/user_homepage.html" 
    form_class = SRTLinkForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    # make success_url stay on the same page
    def get_success_url(self):
        return reverse_lazy('dashboard:user', kwargs={'pk': self.request.user.pk})

    def form_valid(self, form):
        title = form.cleaned_data.get('title')
        srt_link = form.cleaned_data.get('srt_link')
        agency = form.cleaned_data.get('agency')

        # create a new livestream instance
        livestream = Livestream.objects.create(title=title, source=srt_link, agency=agency, created_by=self.request.user)

        # add the livestream to the CustomUser's livestreams
        self.request.user.created_livestreams.add(livestream)
        self.request.user.save()

        return super().form_valid(form)

class StopStreamView(LoginRequiredMixin, generic.DetailView):
    def post(self, request, *args, **kwargs):
        livestream_id = request.POST.get('livestream_id')
        try:
            livestream = Livestream.objects.get(pk=livestream_id)
            if livestream in request.user.created_livestreams.all():
                livestream.delete()
                return JsonResponse({"status": "success"}, status=200)
            else:
                return JsonResponse({"status": "error", "message": "Livestream not found in user's livestreams"}, status=404)
        except Livestream.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Livestream not found"}, status=404)

class LoginView(auth_views.LoginView):
    model = CustomUser
    template_name = "dashboard/login.html"

    def get_success_url(self):
        return reverse_lazy('dashboard:user', kwargs={'pk': self.request.user.pk})

class UserAPIView(views.APIView):
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