from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route
from django.contrib.auth.hashers import make_password, check_password   #密码存储加密和校验
import json

from server.models import Users
from server.models import Passage
from server.models import Search
from server.models import Home
from server.models import Topic
from server.serializers import UserSerializer
from server.serializers import PassageSerializer
from server.serializers import SearchSerializer
from server.serializers import HomeSerializer
from server.serializers import TopicSerializer
# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    #serializer_class = UserSerializer

    @list_route (methods = ['post'])
    def register (self, request):
        data = json.loads(request.body)
        # 注册用户名校验
        user = Users.objects.filter(username = data['username'])
        if len(user):
            res = {
                "success": True,
                "data": False
            }
            return Response(res)
        data['password'] = make_password(data['password'])
        data['name']=data['username'];
        print(data)
        Users.objects.create(**data)
        res = {
            "success": True,
            "data":True,
            "username":data['username'],
            "imgUrl":"https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=2905424204,1949750727&fm=26&gp=0.jpg",
            "userId":data['username']
        }
        return Response(res)

    @list_route(methods = ['post'])
    def login (self, request):
        data = json.loads(request.body)
        filter_user = Users.objects.filter(username = data['username'])
        if not len(filter_user):
            res = {
                "success": True,
                "data": False
            }
            return Response(res)
        user = UserSerializer(filter_user, many = True).data[0]
        check_pass_result = check_password(data['password'], user['password'])
        if not check_pass_result:
            res = {
                "success": True,
                "data": False
            }
            return Response(res)
        # print(user.get('username'))
        # print(user.get('imgUrl'))
        res = {
            "success": True,
            "data": True,
            "username":user.get('name'),
            "imgUrl":user.get('imgUrl'),
            "userId":user.get('username')
        }
        return Response(res)

    #serializer_class = SearchSerializer
    @list_route(methods = ['get'])
    def headerList (self, request):
        search = SearchSerializer(Search.objects.all().order_by('-times')[:50], many = True).data
        searchList=[]
        for item in search:
            searchList.append(item.get('search'))
            #print(item.get('search'))
        res = {
            "success": True,
            "data": searchList
        }
        #print(res)
        return Response(res)

    @list_route(methods = ['get'])
    def homeList (self, request):
        topic = TopicSerializer(Topic.objects.all()[:5], many = True).data
        topicList=[]
        for item in topic:
            topicList.append({"id":item.get('id'),"title":item.get('title'),"imgUrl":item.get('img')})

        article = PassageSerializer(Passage.objects.all()[:5], many = True).data
        articleList=[]
        for item in article:
            articleList.append({"id":item.get('id'),"title":item.get('title'),"desc":item.get('content')[:75]+"...","imgUrl":item.get('pic')})

        recommend = HomeSerializer(Home.objects.filter(types = 'r'), many = True).data
        recommendList=[]
        for item in recommend:
            recommendList.append({"id":item.get('id'),"imgUrl":item.get('pic')})

        carouse = HomeSerializer(Home.objects.filter(types = 'c'), many = True).data
        carouseList=[]
        for item in carouse:
            carouseList.append({"id":item.get('id'),"imgUrl":item.get('pic')})

        writter = UserSerializer(Users.objects.all(), many = True).data
        writterList=[]
        for item in writter:
            desc="写了%.1fk字 · %.1fk喜欢" % (item.get('total')/1000, item.get("like")/1000)
            writterList.append({"id":item.get('id'),"name":item.get('name'),"desc":desc,"imgUrl":item.get('imgUrl')})
        res={    
        "success":True,
        "data":{
            "topicList":topicList,
            "articleList":articleList,
            "recommendList":recommendList,
            "carouselList":carouseList,
            "writterList":writterList
        }
        }
        return Response(res)

    @list_route(methods = ['get'])
    def moreHomeList (self, request):
        start=5*int(request.GET['page'])
        end=start+5
        article = PassageSerializer(Passage.objects.all()[start:end], many = True).data
        articleList=[]
        for item in article:
            articleList.append({"id":item.get('id'),"title":item.get('title'),"desc":item.get('content'),"imgUrl":item.get('pic')})
        res = {
            "success":True,
            "data":articleList
        }
        return Response(res)

    @list_route(methods = ['get'])
    def getDetail (self, request):
        id=int(request.GET['id'])
        item = PassageSerializer(Passage.objects.filter(id=id)[0]).data
        content="<img src='%s' alt=''/><p>%s</p>"%(item.get('pic'),item.get('content'))
        res = {    
                "success":True,
                "data":{
                        "title":item.get('title'),
                        "content":content
                }
            }
        return Response(res)

    @list_route(methods = ['post'])
    def passage (self, request):
        data = json.loads(request.body)
        filter_user = Users.objects.filter(username = data['user_id'])
        user = UserSerializer(filter_user, many = True).data[0]
        data['user_id'] = user.get('id')
        # print(data)
        Passage.objects.create(**data)
        res = {    
                "success":True,
                "data":True
            }
        return Response(res)