from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import LoginSerializer,UserProfileSerializer,RegisterSerializer,PostSerializer,MessageSerializer
from datetime import datetime
from .authentications import generate_jwt
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile,Post,Message
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
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

class MessageView(APIView):
    def get(self, request, pk=None):
        if pk:
            # 获取单个消息详情
            try:
                message = Message.objects.get(
                    pk=pk,
                    receiver=request.user.userprofile
                )
                serializer = MessageSerializer(message)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Message.DoesNotExist:
                return Response({'message': '消息不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        # 获取消息列表
        page = int(request.query_params.get('page', 1))
        size = int(request.query_params.get('size', 10))
        message_type = request.query_params.get('type')
        
        messages = Message.objects.filter(receiver=request.user.userprofile)
        if message_type:
            messages = messages.filter(type=message_type)
            
        paginator = Paginator(messages, size)
        messages = paginator.get_page(page)
        
        serializer = MessageSerializer(messages, many=True)
        return Response({
            'total': paginator.count,
            'items': serializer.data
        }, status=status.HTTP_200_OK)
        
    def put(self, request, pk=None):
        if not pk:
            # 批量标记已读
            ids = request.data.get('ids', [])
            Message.objects.filter(
                receiver=request.user.userprofile,
                id__in=ids
            ).update(is_read=True)
        else:
            # 标记单个消息已读
            try:
                message = Message.objects.get(
                    pk=pk,
                    receiver=request.user.userprofile
                )
                message.is_read = True
                message.save()
            except Message.DoesNotExist:
                return Response({'message': '消息不存在'}, status=status.HTTP_404_NOT_FOUND)
                
        return Response({'success': True}, status=status.HTTP_200_OK)
        
    def delete(self, request, pk=None):
        if not pk:
            # 批量删除消息
            ids = request.data.get('ids', [])
            Message.objects.filter(
                receiver=request.user.userprofile,
                id__in=ids
            ).delete()
        else:
            # 删除单个消息
            try:
                message = Message.objects.get(
                    pk=pk,
                    receiver=request.user.userprofile
                )
                message.delete()
            except Message.DoesNotExist:
                return Response({'message': '消息不存在'}, status=status.HTTP_404_NOT_FOUND)
                
        return Response({'success': True}, status=status.HTTP_200_OK)

class UnreadMessageCountView(APIView):
    def get(self, request):
        count = Message.objects.filter(
            receiver=request.user.userprofile,
            is_read=False
        ).count()
        return Response({'count': count}, status=status.HTTP_200_OK)


