from celery import shared_task, group

from django.http import JsonResponse, QueryDict
from json import JSONDecodeError

from dashboard.models import CustomUser, Livestream
from dashboard.serializers import LivestreamSerializer

from rest_framework import status

import requests
import logging
logger = logging.getLogger(__name__)

@shared_task(task_time_limit=3)
def auth_login(username, password):
    """ Authenticate CustomUser with username=username and password=password
        Returns True if user exists and password is correct, False otherwise
    """
    try:
        logger.info("authenticating user '" + username + "'...")
        user = CustomUser.objects.get(username=username)
        if user.check_password(password):
            logger.info("user '" + username + "' authenticated")
            return True
        else:
            return False
    except CustomUser.DoesNotExist:
        return False

@shared_task(task_time_limit=3)
def auth_path(path):
    """ Gets path from mediamtx API with name=path
        Returns True if the path exists, False otherwise
        @Requires: is_authorized is the return value of auth_login
    """
    logger.info("getting path data for '" + path + "'...")
    response = requests.get("http://mediamtx:9997/v2/paths/get/" + path)
    if response.status_code == 200:
        return True
    else:
        return False

@shared_task
def post_stream(data):
    """ Post new stream to database
    """
    username = data.get('user')
    created_by_id = CustomUser.objects.get(username=username).id
    path = data.get('path')
    try:
        
        try: # see if stream already exists
            stream = Livestream.objects.get(title=path)
            if stream:
                # update stream status to live
                stream.is_live = True
                stream.save()
                return JsonResponse({"status": "success", "message": "Stream permitted"}, status=200)
        except Livestream.DoesNotExist:
            pass
        
        serializer = LivestreamSerializer(data={'title': path, 'source': 'http://localhost:8888/'+path, 'created_by_id': created_by_id})
        if serializer.is_valid():
            logger.info("serializer valid, posting stream...")
            serializer.save()
            put_latest_frame(serializer.data['source'], serializer.data['id'])
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except JSONDecodeError:
        return JsonResponse({"status": "error", "message": "No data provided"}, status=400)
    
def put_latest_frame(source, livestream_id):
    """ Put latest frame from stream to database
    """
    logger.info("putting latest frame... source: " + source + " livestream_id: " + str(livestream_id))
    #TODO: update livestream object with latest frame screenshot pulled from stream