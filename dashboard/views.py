from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.http import JsonResponse, Http404, HttpResponseNotFound, HttpRequest
from json import JSONDecodeError

from django.views import generic, View
from django.views.generic.edit import FormView
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt

from rest_framework import views, status
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.db.models import Q

from asgiref.sync import async_to_sync, sync_to_async

from config.celery import auth_login, auth_path, post_stream
from .models import Livestream, CustomUser
from .serializers import *
from .forms import *

import logging
logger = logging.getLogger(__name__)

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

# TODO:
# - Use formview instead of generic view to handle post requests
class GroupView(generic.DetailView):
    model = Group
    template_name = "dashboard/group_homepage.html"

    @require_POST
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
    
class SearchView(View):

    @require_GET
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
    
class StreamAPIView(LoginRequiredMixin, views.APIView):
    serializer_class = LivestreamSerializer
    
    @require_GET
    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
            }
    
    @require_GET
    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)
    
    @require_POST
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
    
class UserAPIView(LoginRequiredMixin, views.APIView):
    serializer_class = CustomUserSerializer

    @require_GET
    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
            }
    
    @require_GET
    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)
    
    @require_POST
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
        
class UserView(LoginRequiredMixin, FormView):
    model = CustomUser
    template_name = "dashboard/user_homepage.html" 
    form_class = LivestreamVisibilityForm  # This is used only for the GET request.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['visibility_form'] = LivestreamVisibilityForm(user=self.request.user)
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def post(self, request, *args, **kwargs):
        logger.info("POST request: ")
        logger.info(request.POST)
        form_name = request.POST.get('form_name')
        logger.info("form_name: ")
        logger.info(form_name)

        if form_name == 'visibility_form':
            form_class = LivestreamVisibilityForm
        else:
            return self.form_invalid(None)
        
        form = self.get_form(form_class)
        logger.info("post_data after form: ")
        logger.info(form)

        if form.is_valid():
            logger.info("form is valid")
            logger.info
            form.livestream_id = request.POST.get('livestream_id')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
            
    def form_valid(self, form):
            livestream_id = form.cleaned_data.get('livestream_id')
            try:
                livestream = Livestream.objects.get(pk=livestream_id)
            except Livestream.DoesNotExist:
                return HttpResponseNotFound("Livestream not found")
            
            selected_groups = form.cleaned_data.get('groups')
            livestream.groups.set(selected_groups)
            livestream.save()

            return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('dashboard:user', kwargs={'pk': self.request.user.id})

    #TODO: refactor this into the post method above and add a formview to make the request
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

# TODO:
# - restructure viewportview into separate formviews to handle get, post, and delete requests
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
    
    @require_POST
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

@csrf_exempt
def auth_stream(request):
    """ Handle incoming api request from media server to authenticate stream
    """
    if request.method == 'POST':
        try: # check if request contains user credentials
            data = JSONParser().parse(request)
            logger.info(data)
            userInput = data.get('user')
            passInput = data.get('password')
            pathInput = data.get('path') 
            action = data.get('action')

            # request credentials from mediamtx after receiving first request (always empty)
            if userInput == "" and passInput == "":
                return JsonResponse({"status": "error", "message": "Empty credentials provided"}, status=401)
        except KeyError:
            return JsonResponse({"status": "error", "message": "No credentials provided"}, status=401)
        
        # if action is 'read', let the user view the stream
        if action == 'read':
            return JsonResponse({"status": "success", "message": "Stream authorized"}, status=200)
        
        # Offload the authentication and stream posting to Celery
        # auth_login -> auth_path
        is_authorized = auth_login.s(userInput, passInput)()
        print(is_authorized)
        if is_authorized == True:
            # check if path name matches id of user
            userId = CustomUser.objects.get(username=userInput).id
            if (str(userId) == pathInput):
                # TODO: fix deadlock when calling auth_path with requests library
                #
                # call auth_path to check if path exists
                logger.info("Warning: skipping auth_path check...")
                result = post_stream.s(data)()
                logger.info("result: " + str(result))
                return result
                # logger.info("calling requests.get ...")
                # path_exists = auth_path.s(pathInput)()
                # print("path_exists: " + path_exists)
                # if path_exists == True:
                #     result = post_stream.delay(data)
                #     return result.get()
                # else:
                #     return JsonResponse({"status": "error", "message": "Invalid path"}, status=401)
                # result = post_stream.delay(data)
                # return result.get()
            else:
                return JsonResponse({"status": "error", "message": "Invalid path"}, status=401)
        else:
            return JsonResponse({"status": "error", "message": "Invalid credentials"}, status=401)
            
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
