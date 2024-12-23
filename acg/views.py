from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import LoginSerializer,UserProfileSerializer,RegisterSerializer,PostSerializer,FollowSerializer,TopicSerializer
from datetime import datetime
from .authentications import generate_jwt
from rest_framework.response import Response
from rest_framework import status,generics
from .models import UserProfile,Post,Follow,Topic
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

# Create your views here.

#这是登录视图
class LoginView(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            user.last_login = datetime.now()
            user.save()
            #生成jwt token
            token = generate_jwt(user)
            #获取用户信息
            user_profile = UserProfile.objects.get(userid=user)
            #同时返回用户信息
            return Response({'token':token,'user':UserProfileSerializer(user_profile).data},status=status.HTTP_200_OK)
        else:
            return Response({"messages":"参数验证失败"},status=status.HTTP_400_BAD_REQUEST)

#这是注册视图
class RegisterView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            user.last_login = datetime.now()
            user.save()
            #生成jwt token
            token = generate_jwt(user)
            #获取用户信息
            user_profile = UserProfile.objects.get(userid=user)
            #同时返回用户信息
            return Response({'token':token,'user':UserProfileSerializer(user_profile).data},status=status.HTTP_200_OK)
        else:
            return Response({"messages":"参数验证失败"},status=status.HTTP_400_BAD_REQUEST)

#这是用户信息视图
class UserProfileView(APIView):
    #获取用户信息
    def get(self,request):
        user_profile = UserProfile.objects.get(userid=request.user)
        return Response(UserProfileSerializer(user_profile).data,status=status.HTTP_200_OK)
    #更新用户信息 ,接口通用
    def put(self,request):
        user_profile = UserProfile.objects.get(userid=request.user)
        serializer = UserProfileSerializer(user_profile,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class PostView(APIView):
    def get_object(self,pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return None

    def get(self, request, pk=None):
        if pk:
            post = self.get_object(pk)
            #如果post不存在
            if post is None:
                return Response({'message':'动态不存在'},status=status.HTTP_404_NOT_FOUND)
            serializer = PostSerializer(post)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            #先判断是否有search关键字
            search_query = request.query_params.get('search', None)
            if search_query:
                #从动态标题和动态内容中搜索
                posts = Post.objects.filter(
                    Q(posttitle__icontains=search_query) |
                    Q(postcontent__icontains=search_query)
                )
            else:
                posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request):
        pass

class TopicView(APIView):
    def get_object(self,pk):
        try:
            return Topic.objects.get(pk=pk)
        except Topic.DoesNotExist:
            return None

    def get(self, request, pk=None):
        if pk:
            topic = self.get_object(pk)
            #如果topic不存在
            if topic is None:
                return Response({'message':'话题不存在'},status=status.HTTP_404_NOT_FOUND)
            serializer = TopicSerializer(topic)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            topics = Topic.objects.all()
            serializer = TopicSerializer(topics, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)



#这是需要token的接口测试例子
class TestView(APIView):
    def post(self,request):
        return Response({'message':'成功'},status=status.HTTP_200_OK)



# 获取关注列表
class FollowListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)

# 关注用户
class FollowUserView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)

# 取消关注
class UnfollowUserView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)