from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
import rest_framework.serializers as serializers
import socialnetwork.models as models


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class ProfileSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = models.UserProfile
        fields = '__all__'


class ResponseStatusSerializer(ModelSerializer):
    class Meta:
        model = models.ResponseStatus
        fields = ['status', 'message']


class PostSerializer(ModelSerializer):

    class Meta:
        model = models.Post
        fields = ['content']