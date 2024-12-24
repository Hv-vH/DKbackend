from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import LoginSerializer,UserProfileSerializer,RegisterSerializer,PostSerializer,FollowSerializer
from datetime import datetime
from .authentications import generate_jwt
from rest_framework.response import Response
from rest_framework import status,generics
from .models import UserProfile,Post,Follow
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
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
    #更新用户信息
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
            posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)

#这是需要token的接口测试例子
class TestView(APIView):
    def post(self,request):
        return Response({'message':'成功'},status=status.HTTP_200_OK)



# 获取关注列表
class FollowListView(APIView):
    def get(self, request):
        follows = Follow.objects.filter(follower=request.user)
        serializer = FollowSerializer(follows, many=True)
        return Response(serializer.data)

# 关注用户
class FollowUserView(APIView):
    def post(self, request):
        user_id = request.data.get('userId')
        followed_user = get_object_or_404(User, id=user_id)
 # 创建关注关系 follow, created = Follow.objects.get_or_create(follower=request.user, followed=followed_user)

# 取消关注
class UnfollowUserView(APIView):
    def delete(self, request, user_id):
        follow = get_object_or_404(Follow, follower=request.user, followed_id=user_id)
        follow.delete()
        return Response({'message': 'Successfully unfollowed.'}, status=status.HTTP_204_NO_CONTENT)