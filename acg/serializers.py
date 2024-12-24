from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile,Post,LikePost,CollectPost,Article, Message

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
    userid = serializers.IntegerField(source='authorid.userid.id')
    username = serializers.CharField(source='authorid.userid.username')
    email = serializers.CharField(source='authorid.userid.email')
    nickname = serializers.CharField(source='authorid.nickname')
    avatar = serializers.CharField(source='authorid.avatar')
    description = serializers.CharField(source='authorid.description')
    #点赞数
    like_count = serializers.SerializerMethodField()
    #收藏数
    collect_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id',
                  'userid','username','email','nickname','avatar','description',
                  'posttitle','postcontent','postcreated_time','postimages','posttags',
                  'like_count','collect_count')

    def get_like_count(self,obj):
        return LikePost.objects.filter(post=obj).count()

    def get_collect_count(self,obj):
        return CollectPost.objects.filter(post=obj).count()


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    createTime = serializers.DateTimeField(source='created_time', format='%Y-%m-%dT%H:%M:%SZ')
    isRead = serializers.BooleanField(source='is_read')
    
    class Meta:
        model = Message
        fields = ['id', 'type', 'title', 'content', 'sender', 'createTime', 'isRead', 'metadata']
        
    def get_sender(self, obj):
        return {
            'id': obj.sender.id,
            'username': obj.sender.nickname,
            'avatar': obj.sender.avatar
        }
