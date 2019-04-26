from rest_framework import serializers
from server.models import Users
from server.models import Passage
from server.models import Search
from server.models import Home
from server.models import Topic


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'username', 'password','total','like','name','imgUrl')
class PassageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passage
        fields = ('id', 'user', 'title','content','pic')
class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = ('id', 'search', 'times')
class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home
        fields = ('id', 'pic', 'types')
class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('id','title','img')