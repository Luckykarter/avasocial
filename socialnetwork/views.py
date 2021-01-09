from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
import socialnetwork.serializers as serializers
from socialnetwork import models
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
import socialnetwork.forms as forms
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.password_validation import validate_password

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


def _HttpResponse(request, template, context):
    """
    Helper that creates http response from template with cookies included refresh token for JWT
    :param request: http request
    :param template: html template (*.html)
    :param context: page context (dictionaty)
    :return: rendered web-page
    """
    page = loader.get_template(template)
    response = HttpResponse(page.render(context, request))
    if request.user.is_authenticated:
        response.set_cookie('refresh', RefreshToken.for_user(request.user), samesite='strict')

    return response


def _validation_error_response(e):
    return Response(_get_resp(FAIL, "\n".join([x for x in e])), status=status.HTTP_400_BAD_REQUEST)


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

    email = data.get('email')
    try:
        models.validate_email(email)
    except ValidationError as e:
        return _validation_error_response(e)

    user_data = data.pop('user')
    username = user_data.get('username')

    user = User.objects.filter(username=username)
    if user:
        return Response(_get_resp(FAIL, f'User with username {username} already exists'),
                        status=status.HTTP_400_BAD_REQUEST)

    password = user_data.get('password')
    try:
        validate_password(password)
    except ValidationError as e:
        return _validation_error_response(e)

    user = User(username=username, password=password)

    try:
        models.UserProfile.objects.create(user=user, **data)
        return Response(_get_resp(SUCCESS, f'User {username} successfully registered'), status=status.HTTP_200_OK)
    except Exception as e:
        return Response(_get_resp(FAIL, str(e)), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    methods=['POST'],
    operation_id='create_post',
    operation_description='Create new post by logged in user\n'
                          'Use endpoint <b>/user/login</b> for user authentication\n'
                          'In case of successful post - response will contain <b>post_id</b> in tag <b>"message"</b>',
    request_body=serializers.PostSerializer,
    responses={200: openapi.Response('OK', serializers.ResponseStatusSerializer)})
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # post creation only for authenticated users
def create_post(request):
    try:
        post = models.Post.objects.create(user=request.user, content=request.data.get('content'))
        return Response(_get_resp(SUCCESS, post.pk))
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

    if post.user == request.user:
        return Response(_get_resp(FAIL, 'You cannot like your own post'), status=status.HTTP_400_BAD_REQUEST)

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


@login_required(login_url='/accounts/login/')
@permission_classes([IsAuthenticated])
def index(request):
    template = 'index.html'
    # for simplification show only 20 last posts #TODO: infinite scroll or pagination
    posts = models.Post.objects.all().order_by('-timestamp')[:20]
    own_profile = models.UserProfile.objects.filter(user=request.user)

    return _HttpResponse(request, template, {
        "posts": posts,
        "user": request.user.username if not own_profile else own_profile[0]
    })


def login_view(request):
    template = 'registration/login.html'
    response = _HttpResponse(request, template, {})

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
        else:
            response = _HttpResponse(request, template, {
                'form': form,
                'login_error': form.error_messages.get('invalid_login')
            })


    return response


def logout_view(request):
    logout(request)
    return redirect('/')


def signup_view(request):
    return _HttpResponse(request, 'registration/signup.html', {})

def profile_view(request):
    try:
        user = models.UserProfile.objects.get(user=request.user)
    except models.UserProfile.DoesNotExist:
        user = request.user.username

    context = {'user': user}

    if request.method == 'POST':
        form = forms.UserProfileForm(instance=user, data=request.POST)
        if form.is_valid():
            form.save()
            context['update_success'] = f'User {user} updated successfully'

    return _HttpResponse(request, 'profile.html', context)
