from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile,Post,LikePost,CollectPost,Comment,Article,Topic,Follow, Message, LikeComment
import ast

#创建登录序列化器
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField()
    #验证逻辑
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            #验证用户名和密码是否正确
            user = User.objects.filter(username=username).first()
            if not user:
                raise serializers.ValidationError('用户名不存在')
            if not user.check_password(password):
                raise serializers.ValidationError('密码错误')
            #将用户信息保存到attrs中
            attrs['user'] = user
        else:
            raise serializers.ValidationError('用户名或密码不能为空')
        return attrs

#创建注册序列化器
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    #验证逻辑
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password :
            #验证用户名是否存在
            user = User.objects.filter(username=username).first()
            if user:
                raise serializers.ValidationError('用户名已存在')
            #创建用户
            user = User.objects.create_user(username=username,password=password)
            #同时创建用户信息
            UserProfile.objects.create(userid=user)
            #将用户信息保存到attrs中
            attrs['user'] = user
        else:
            raise serializers.ValidationError('用户名或密码或邮箱不能为空')
        return attrs

#创建用户信息序列化器
class UserProfileSerializer(serializers.ModelSerializer):
    # 包含 User 和 UserProfile 的字段
    username = serializers.CharField(source='userid.username')
    email = serializers.CharField(source='userid.email')

    class Meta:
        model = UserProfile
        fields = '__all__'

#创建动态信息序列化器
class PostSerializer(serializers.ModelSerializer):
    #包含UserProfile和User的字段
    userid = serializers.IntegerField(source='authorid.userid.id',read_only=True)
    username = serializers.CharField(source='authorid.userid.username',read_only=True)
    email = serializers.CharField(source='authorid.userid.email',read_only=True)
    nickname = serializers.CharField(source='authorid.nickname',read_only=True)
    avatar = serializers.CharField(source='authorid.avatar',read_only=True)
    description = serializers.CharField(source='authorid.description',read_only=True)
    #点赞数
    like_count = serializers.SerializerMethodField()
    #收藏数
    collect_count = serializers.SerializerMethodField()
    #还需要评论数
    comment_count = serializers.SerializerMethodField()
    #是否点赞
    is_like = serializers.SerializerMethodField()
    #是否收藏
    is_collect = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id',
                  'userid','username','email','nickname','avatar','description',
                  'posttitle','postcontent','postcreated_time','postimages','posttags',
                  'like_count','collect_count','comment_count','is_like','is_collect'
                  )

    def create(self, validated_data):
        #从请求中获取用户ID
        authorid = self.context.get('request').user.id
        #创建动态
        post = Post.objects.create(authorid_id=authorid,**validated_data)
        return post

    def get_like_count(self,obj):
        return LikePost.objects.filter(post=obj).count()

    def get_collect_count(self,obj):
        return CollectPost.objects.filter(post=obj).count()
    
    def get_comment_count(self,obj):
        return Comment.objects.filter(postid=obj).count()

    def get_is_like(self,obj):
        request = self.context.get('request')
        if not request.user.is_authenticated:
            return False
        return LikePost.objects.filter(liker=request.user.id,post=obj).exists()

    def get_is_collect(self,obj):
        request = self.context.get('request')
        if not request.user.is_authenticated:
            return False
        return CollectPost.objects.filter(collector=request.user.id,post=obj).exists()

class FollowSerializer(serializers.ModelSerializer):
    followed = UserProfileSerializer()  # 嵌入用户序列化器
    class Meta:
        model = Follow
        fields = ['follower', 'followed']
        
class TopicSerializer(serializers.ModelSerializer):
    #话题下的动态数
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = '__all__'

    def get_post_count(self, obj):
        # 现在topictags是一个字符串，需要转换成列表
        topic_tags = set(ast.literal_eval(obj.topictags))
        count = 0
        for post in Post.objects.all():
            post_tags = set(ast.literal_eval(post.posttags))
            if topic_tags & post_tags:
                count += 1
        return count


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    is_read = serializers.BooleanField(source='is_read')
    created_time = serializers.DateTimeField(source='created_time')
    
    class Meta:
        model = Message
        fields = ['id', 'type', 'content', 'sender', 'created_time', 'is_read', 'metadata']
        
    def get_sender(self, obj):
        return {
            'id': obj.sender.id,
            'username': obj.sender.nickname,
            'avatar': obj.sender.avatar
        }

class CommentSerializer(serializers.ModelSerializer):
    #包含UserProfile和User的字段
    userid = serializers.IntegerField(source='commentauthor.userid.id',read_only=True)
    username = serializers.CharField(source='commentauthor.userid.username',read_only=True)
    email = serializers.CharField(source='commentauthor.userid.email',read_only=True)
    nickname = serializers.CharField(source='commentauthor.nickname',read_only=True)
    avatar = serializers.CharField(source='commentauthor.avatar',read_only=True)
    description = serializers.CharField(source='commentauthor.description',read_only=True)
    #点赞数
    like_count = serializers.SerializerMethodField()
    #是否点赞
    is_like = serializers.SerializerMethodField()
    #嵌套的评论
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id',
                  'userid','username','email','nickname','avatar','description',
                  'commenttype','postid','articleid','commentid','commentcontent','comment_time',
                  'like_count','is_like',
                  'replies',
                  ]

    def validate(self, attrs):
        commenttype = attrs.get('commenttype')
        postid = attrs.get('postid')
        articleid = attrs.get('articleid')
        commentid = attrs.get('commentid')

        #判断postid、articleid有且只有一个，commentid在子评论时会有
        if not (postid or articleid):
            raise serializers.ValidationError('postid和articleid不能同时为空')
        #如果是对评论的评论，那么commenttype一定为comment
        if commentid:
            if commenttype != 'comment':
                raise serializers.ValidationError('commentid不为空时，commenttype必须为comment')
        return attrs

    def create(self, validated_data):
        #从请求中获取用户ID
        commentauthor = self.context.get('request').user.id
        #创建评论
        comment = Comment.objects.create(commentauthor_id=commentauthor,**validated_data)
        return comment

    #实现嵌套的评论
    def get_replies(self,obj):
        #评论的评论
        replies = Comment.objects.filter(commentid=obj)
        #
        if replies.exists():
            return CommentSerializer(replies,many=True,context=self.context).data
        else:
            return None

    def get_like_count(self,obj):
        return LikeComment.objects.filter(comment=obj).count()

    def get_is_like(self,obj):
        request = self.context.get('request')
        return LikeComment.objects.filter(liker=request.user.id,comment=obj).exists()