from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import (LoginSerializer,UserProfileSerializer,RegisterSerializer,
                          PostSerializer,FollowSerializer,TopicSerializer,CommentSerializer,
                          MessageSerializer)
from datetime import datetime
from .authentications import generate_jwt
from rest_framework.response import Response
from rest_framework import status,generics
from .models import UserProfile,Post,Follow,Topic,Comment,Message,Article,LikePost, LikeArticle, LikeComment,CollectPost, CollectArticle
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
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
            return Response({"messages":"参数验证失败",'errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

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
            return Response({"messages":"参数验证失败",'errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
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
            serializer = PostSerializer(post,context={'request':request})
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            #先判断是否有search关键字
            search_query = request.query_params.get('search', None)
            #还需要判断是否有category关键字
            category_query = request.query_params.get('category', None)
            #还需要判断是否有owner关键字
            owner_query = request.query_params.get('owner', None)
            if search_query:
                #从动态标题和动态内容中搜索
                posts = Post.objects.filter(
                    Q(posttitle__icontains=search_query) |
                    Q(postcontent__icontains=search_query)
                )
                #可能没有对应的数据
                if not posts:
                    return Response({'message':'没有找到对应的动态'},status=status.HTTP_404_NOT_FOUND)
            elif category_query:
                #从动态标签中搜索
                posts = Post.objects.filter(posttags__icontains=category_query)
                #可能没有对应的数据
                if not posts:
                    return Response({'message':'没有找到对应的动态'},status=status.HTTP_404_NOT_FOUND)
            elif owner_query:
                #从userid中搜索
                posts = Post.objects.filter(authorid__userid__id=owner_query)
                if not posts:
                    return Response({'message':'没有找到对应的动态'},status=status.HTTP_404_NOT_FOUND)
            else:
                posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True,context={'request':request})
            return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request):
        serializer = PostSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


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

class MessageView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                # 获取单条消息
                message = Message.objects.get(
                    pk=pk,
                    receiver=request.user.userprofile
                )
                # 如果消息未读,标记为已读
                if not message.is_read:
                    message.is_read = True
                    message.save()
                    
                serializer = MessageSerializer(message)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Message.DoesNotExist:
                return Response({'message': '消息不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        # 获取消息列表
        message_type = request.query_params.get('type')
        
        # 基础查询
        messages = Message.objects.filter(
            receiver=request.user.userprofile
        ).order_by('-created_time')
        
        # 根据消息类型筛选
        if message_type:
            messages = messages.filter(type=message_type)
        
        # 获取未读消息的ID列表
        unread_ids = list(messages.filter(is_read=False).values_list('id', flat=True))
        
        # 将未读消息标记为已读
        if unread_ids:
            Message.objects.filter(
                id__in=unread_ids,
                receiver=request.user.userprofile
            ).update(is_read=True)
        
        serializer = MessageSerializer(messages, many=True)
        return Response({
            'total': messages.count(),
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

    def post(self, request):
        # 获取请求数据
        receiver_id = request.data.get('receiver')
        content = request.data.get('content')
        message_type = request.data.get('type')
        metadata = request.data.get('metadata', None)

        # 添加数据验证
        if not all([receiver_id, content, message_type]):
            return Response(
                {'message': '缺少必要字段'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 验证消息类型是否合法
        if message_type not in dict(Message.MESSAGE_TYPES):
            return Response(
                {'message': '无效的消息类型'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 获取接收者的 UserProfile
            receiver = UserProfile.objects.get(id=receiver_id)
            
            # 验证不能给自己发消息
            if receiver == request.user.userprofile:
                return Response(
                    {'message': '不能给自己发送消息'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 创建消息
            message = Message.objects.create(
                sender=request.user.userprofile,
                receiver=receiver,
                content=content,
                type=message_type,
                metadata=metadata
            )
            
            serializer = MessageSerializer(message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except UserProfile.DoesNotExist:
            return Response({'message': '接收者不存在'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UnreadMessageCountView(APIView):
    def get(self, request):
        # 获取所有类型的未读消息数量
        counts = {
            'reply': Message.objects.filter(
                receiver=request.user.userprofile,
                type='reply',
                is_read=False
            ).count(),
            'mention': Message.objects.filter(
                receiver=request.user.userprofile,
                type='mention',
                is_read=False
            ).count(),
            'like': Message.objects.filter(
                receiver=request.user.userprofile,
                type='like',
                is_read=False
            ).count(),
            'private': Message.objects.filter(
                receiver=request.user.userprofile,
                type='private',
                is_read=False
            ).count(),
            'total': Message.objects.filter(
                receiver=request.user.userprofile,
                is_read=False
            ).count()
        }
        return Response(counts, status=status.HTTP_200_OK)



# 关注列表、关注用户和取消关注的视图
class FollowView(APIView):

    def get(self, request):
        follows = Follow.objects.filter(follower=request.user)
        serializer = FollowSerializer(follows, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_id = request.data.get('userId')
        followed_user = get_object_or_404(User, id=user_id)
        follow, created = Follow.objects.get_or_create(follower=request.user, followed=followed_user)
        return Response({'message': 'Successfully followed.'}, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        follow = get_object_or_404(Follow, follower=request.user, followed_id=user_id)
        follow.delete()
        return Response({'message': 'Successfully unfollowed.'}, status=status.HTTP_204_NO_CONTENT)


#这是评论视图
class CommentView(APIView):
    def get(self,request):
        comment_type = request.query_params.get('type',None)
        if comment_type == 'post':
            post_id = request.query_params.get('id',None)
            if not post_id:
                return Response({'message':'参数错误'},status=status.HTTP_400_BAD_REQUEST)
            comments = Comment.objects.filter(commenttype='post',postid=post_id)
            serializer = CommentSerializer(comments,many=True,context={'request':request})
            return Response(serializer.data,status=status.HTTP_200_OK)
        elif comment_type == 'article':
            article_id = request.query_params.get('id',None)
            if not article_id:
                return Response({'message':'参数错误'},status=status.HTTP_400_BAD_REQUEST)
            comments = Comment.objects.filter(commenttype='article',articleid=article_id)
            serializer = CommentSerializer(comments,many=True,context={'request':request})
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response({'message':'参数错误'},status=status.HTTP_400_BAD_REQUEST)
    def post(self,request):
        serializer = CommentSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LikePostView(APIView):
    def post(self, request, post_id):
        user_id = request.user.id  # 获取当前用户的 ID
        try:
            post = Post.objects.get(id=post_id)
            like, created = LikePost.objects.get_or_create(liker=user_id, post=post)

            if created:
                return Response({'detail': '点赞成功'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail': '您已经点赞过了'}, status=status.HTTP_400_BAD_REQUEST)

        except Post.DoesNotExist:
                return Response({'detail': '动态未找到'}, status=status.HTTP_404_NOT_FOUND)

class LikeArticleView(APIView):
    def post(self, request, article_id):
        user_id = request.user.id  # 获取当前用户的 ID
        try:
            article = Article.objects.get(id=article_id)
            like, created = LikeArticle.objects.get_or_create(liker=user_id, article=article)

            if created:
                return Response({'detail': '点赞成功'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail': '您已经点赞过了'}, status=status.HTTP_400_BAD_REQUEST)

        except Article.DoesNotExist:
            return Response({'detail': '文章未找到'}, status=status.HTTP_404_NOT_FOUND)

class LikeCommentView(APIView):
    def post(self, request, comment_id):
        user_id = request.user.id  # 获取当前用户的 ID
        try:
            comment = Comment.objects.get(id=comment_id)
            like, created = LikeComment.objects.get_or_create(liker=user_id, comment=comment)

            if created:
                return Response({'detail': '点赞成功'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail': '您已经点赞过了'}, status=status.HTTP_400_BAD_REQUEST)

        except Comment.DoesNotExist:
            return Response({'detail': '评论未找到'}, status=status.HTTP_404_NOT_FOUND)

# 收藏和取消收藏 Post
class PostCollectionView(APIView):
    def post(self, request, post_id):
        user_id = request.user.id  # 获取当前用户的 ID
        try:
            post = Post.objects.get(id=post_id)
            collect, created = CollectPost.objects.get_or_create(collector_id=user_id, post=post)

            if created:
                return Response({'detail': '收藏成功'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail': '您已经收藏过了'}, status=status.HTTP_400_BAD_REQUEST)

        except Post.DoesNotExist:
            return Response({'detail': '动态未找到'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, post_id):
        user_id = request.user.id  # 获取当前用户的 ID
        try:
            post = Post.objects.get(id=post_id)
            collect = CollectPost.objects.get(collector_id=user_id, post=post)
            collect.delete()
            return Response({'detail': '取消收藏成功'}, status=status.HTTP_204_NO_CONTENT)

        except CollectPost.DoesNotExist:
            return Response({'detail': '您尚未收藏此动态'}, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({'detail': '动态未找到'}, status=status.HTTP_404_NOT_FOUND)

# 收藏和取消收藏 Article
class ArticleCollectionView(APIView):
    def post(self, request, article_id):
        user_id = request.user.id  # 获取当前用户的 ID
        try:
            article = Article.objects.get(id=article_id)
            collect, created = CollectArticle.objects.get_or_create(collector_id=user_id, article=article)

            if created:
                return Response({'detail': '收藏成功'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail': '您已经收藏过了'}, status=status.HTTP_400_BAD_REQUEST)

        except Article.DoesNotExist:
            return Response({'detail': '文章未找到'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, article_id):
        user_id = request.user.id  # 获取当前用户的 ID
        try:
            article = Article.objects.get(id=article_id)
            collect = CollectArticle.objects.get(collector_id=user_id, article=article)
            collect.delete()
            return Response({'detail': '取消收藏成功'}, status=status.HTTP_204_NO_CONTENT)

        except CollectArticle.DoesNotExist:
            return Response({'detail': '您尚未收藏此文章'}, status=status.HTTP_400_BAD_REQUEST)
        except Article.DoesNotExist:
            return Response({'detail': '文章未找到'}, status=status.HTTP_404_NOT_FOUND)

def get_user_stats(request, user_id):
    # 获取用户实例
    user = get_object_or_404(User, id=user_id)

    # 查询被关注数量
    followers_count = Follow.objects.filter(followed=user).count()  # 被关注数量
    # 查询关注数量
    following_count = Follow.objects.filter(follower=user).count()  # 关注数量
    # 查询收藏数量
    collections_count = CollectArticle.objects.filter(collector=user).count()  # 收藏数量
    # 返回 JSON 响应
    return Response({
        'followers_count': followers_count,
        'following_count': following_count,
        'collections_count': collections_count,
    })

#收藏列表
class CollectionListView(APIView):
    def get(self, request):
        user_id = request.user.id  # 获取当前用户的 ID

        # 获取用户收藏的动态
        collected_posts = CollectPost.objects.filter(collector_id=user_id).select_related('post')
        post_list = [
            {
                'id': collect.post.id,
                'title': collect.post.title,
                'collect_time': collect.collect_time
            }
            for collect in collected_posts
        ]

        # 获取用户收藏的文章
        collected_articles = CollectArticle.objects.filter(collector_id=user_id).select_related('article')
        article_list = [
            {
                'id': collect.article.id,
                'title': collect.article.title,
                'collect_time': collect.collect_time
            }
            for collect in collected_articles
        ]

        return Response({
            'collected_posts': post_list,
            'collected_articles': article_list
        }, status=status.HTTP_200_OK)


