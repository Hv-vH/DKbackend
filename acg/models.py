from django.db import models
from django.contrib.auth.models import User
import random
# Create your models here.

class UserProfile(models.Model):
    #userid，通过外键关联到User表
    userid = models.OneToOneField(User, on_delete=models.CASCADE)
    #昵称,不能为空，数据库不能为空，前端可以不传，默认为100+默认8位随机数
    nickname = models.CharField(max_length=20,null=False,blank=True,default='用户100'+str(random.randint(10000000,99999999)))
    #头像文件，存放前端，这里是相对路径,数据库不能为空，前端可以不传 默认为'avatars/avatar.jpg'
    avatar = models.TextField(null=False,blank=True,default='avatars/avatar.jpg')
    #个性描述，可以为空
    description = models.TextField(blank=True)

class Post(models.Model):
    #作者id,外键关联到UserProfile表
    authorid = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    #动态标题,不能为空
    posttitle = models.CharField(max_length=50,blank=False)
    #动态内容
    postcontent = models.TextField()
    #动态中的图片，存放前端，这里是相对路径
    postimages = models.TextField(blank=False)
    #动态所属的标签
    posttags = models.TextField()
    #动态创建时间
    postcreated_time = models.DateTimeField(auto_now_add=True)

class LikePost(models.Model):
    #点赞者id,外键关联到UserProfile表
    liker = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    #被点赞的动态id,外键关联到Post表
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    #点赞时间
    like_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        #联合唯一键
        unique_together = ('liker','post')

class CollectPost(models.Model):
    #收藏者id,外键关联到UserProfile表
    collector = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    #被收藏的动态id,外键关联到Post表
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    #收藏时间
    collect_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        #联合唯一键
        unique_together = ('collector','post')

class Article(models.Model):
    #作者id,外键关联到UserProfile表
    authorid = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    #文章标题,不能为空
    articletitle = models.CharField(max_length=50,blank=False)
    #文章所属的标签
    articletags = models.TextField()
    #文章的封面图
    articlecoverimage = models.TextField()
    #文章的摘要
    articlesummary = models.TextField()
    #文章创建时间
    articlecreated_time = models.DateTimeField(auto_now_add=True)
    #文章状态
    articlestatus = models.CharField(max_length=10)


class ArticleContent(models.Model):
    #文章内容有三种类型，subtitle, text, image
    articletype = models.CharField(max_length=10)
    #文章内容
    content = models.TextField()
    #内容的顺序
    order = models.IntegerField()
    #文章id,外键关联到Article表
    articleid = models.ForeignKey(Article, on_delete=models.CASCADE)

class LikeArticle(models.Model):
    #点赞者id,外键关联到UserProfile表
    liker = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    #被点赞的文章id,外键关联到Article表
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    #点赞时间
    like_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        #联合唯一键
        unique_together = ('liker','article')

class CollectArticle(models.Model):
    #收藏者id,外键关联到UserProfile表
    collector = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    #被收藏的文章id,外键关联到Article表
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    #收藏时间
    collect_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        #联合唯一键
        unique_together = ('collector','article')

class Comment(models.Model):
    #评论有可能是对动态的评论，也有可能是对文章的评论，也有可能是对评论的评论
    commenttype = models.CharField(max_length=10)
    #评论的动态id,外键关联到Post表
    postid = models.ForeignKey(Post, on_delete=models.CASCADE,blank=True,null=True)
    #评论的文章id,外键关联到Article表
    articleid = models.ForeignKey(Article, on_delete=models.CASCADE,blank=True,null=True)
    #评论的评论id,关联自身表
    commentid = models.ForeignKey('self', on_delete=models.CASCADE,blank=True,null=True)
    #评论者id,外键关联到UserProfile表
    commentauthor = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    #评论内容
    commentcontent = models.TextField()
    #评论时间
    comment_time = models.DateTimeField(auto_now_add=True)

class LikeComment(models.Model):
    #点赞者id,外键关联到UserProfile表
    liker = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    #被点赞的评论id,外键关联到Comment表
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    #点赞时间
    like_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        #联合唯一键
        unique_together = ('liker','comment')

class Message(models.Model):
    MESSAGE_TYPES = (
        ('system', '系统消息'),
        ('activity', '活动消息'),
        ('comment', '评论消息'),
        ('like', '点赞消息')
    )
    
    # 发送者id,外键关联到UserProfile表
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_messages')
    # 接收者id,外键关联到UserProfile表
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_messages')
    # 消息标题
    title = models.CharField(max_length=50)
    # 消息内容
    content = models.TextField()
    # 消息类型
    type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    # 消息创建时间
    created_time = models.DateTimeField(auto_now_add=True)
    # 是否已读
    is_read = models.BooleanField(default=False)
    # 额外数据(JSON格式)
    metadata = models.JSONField(null=True, blank=True)





