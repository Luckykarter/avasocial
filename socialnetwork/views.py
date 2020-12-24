from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
import socialnetwork.serializers as serializers
from socialnetwork import models
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User

FAIL = 'fail'
SUCCESS = 'success'


def _get_resp(sta, msg):
    """
    Helper that returns for body of informative HTTP responses
    :param sta: status of response - fail/success
    :param msg: describes the event
    :return: serialized object of ResponseStatus
    """
    return serializers.ResponseStatusSerializer(
        models.ResponseStatus(
            status=sta, message=msg)).data


@swagger_auto_schema(
    methods=['POST'],
    operation_id='register_user',
    operation_description='Register New User\n\n'
                          'The missing profile data is retrieved from open sources via the service '
                          '<a href="https://clearbit.com/" target="_blank">ClearBit</a>\n'
                          'E-mail validated using validator from '
                          '<a href="https://hunter.io" target="_blank">Hunter</a>',
    request_body=serializers.ProfileSerializer,
    responses={200: openapi.Response('OK', serializers.ResponseStatusSerializer)})
@api_view(['POST'])
@permission_classes([AllowAny])  # signup allowed to everyone
def sign_up(request):
    data = request.data
    if 'user' not in data:
        return Response(_get_resp(FAIL, 'User data is missing'), status=status.HTTP_400_BAD_REQUEST)

    user_data = data.pop('user')
    username = user_data.get('username')

    user = User.objects.filter(username=username)
    if user:
        return Response(_get_resp(FAIL, f'User with username {username} already exists'),
                        status=status.HTTP_400_BAD_REQUEST)

    user = User(username=username, password=user_data.get('password'))

    try:
        models.UserProfile.objects.create(user=user, **data)
        return Response(_get_resp(SUCCESS, f'User {username} successfully registered'), status=status.HTTP_200_OK)
    except Exception as e:
        return Response(_get_resp(FAIL, str(e)), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    methods=['POST'],
    operation_id='create_post',
    operation_description='Create new post by logged in user\n'
                          'Use endpoint <b>/user/login</b> for user authentication',
    request_body=serializers.PostSerializer,
    responses={200: openapi.Response('OK', serializers.ResponseStatusSerializer)})
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # post creation only for authenticated users
def create_post(request):
    try:
        post = models.Post.objects.create(user=request.user, **request.data)
        return Response(_get_resp(SUCCESS, f'Post with id {post.pk} successfully created'))
    except Exception as e:
        return Response(_get_resp(FAIL, str(e)), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    methods=['GET'],
    operation_id='trigger_like_post',
    operation_description='Likes/unlikes post with given ID by logged in user\n\n'
                          'If post is not liked by - likes it\n'
                          'If post is already liked by - unlikes it',
    responses={200: openapi.Response('OK', serializers.ResponseStatusSerializer)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trigger_like(request, **kwargs):
    post_id = kwargs.get('post_id')
    try:
        post = models.Post.objects.get(pk=post_id)
    except models.Post.DoesNotExist:
        return Response(_get_resp(FAIL, f'Post with id {post_id} not found'), status=status.HTTP_404_NOT_FOUND)

    try:
        users = post.likes_users.split(',')
        un = ''
        if request.user.username not in users:
            users.append(request.user.username)
            post.likes += 1
        else:
            un = 'un'
            users.remove(request.user.username)
            post.likes -= 1

        post.likes_users = ",".join(users)
        post.save()
        return Response(_get_resp(SUCCESS, f'Post with id {post_id} {un}liked'), status=status.HTTP_200_OK)
    except Exception as e:
        return Response(_get_resp(FAIL, str(e)), status.HTTP_500_INTERNAL_SERVER_ERROR)
