from django.db import models
from django.contrib.auth.models import User
import random
# Create your models here.

class UserProfile(models.Model):
    #userid，通过外键关联到User表
    userid = models.OneToOneField(User, on_delete=models.CASCADE)
    #昵称,不能为空，数据库不能为空，前端可以不传，默认为100+默认8位随机数
    nickname = models.CharField(max_length=20,null=False,blank=True)
    #头像文件，存放前端，这里是相对路径,数据库不能为空，前端可以不传 默认为‘avatars/avatar.jpg’
    avatar = models.TextField(null=False,blank=True,default='avatars/avatar.jpg')
    #个性描述，可以为空
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.nickname:
            self.nickname = '用户100' + str(random.randint(10000000, 99999999))
        super(UserProfile, self).save(*args, **kwargs)

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
    #评论有可能是对动态的评论，也有可能是对文章的评论，也有可能是对评论的评论 post/article/comment
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
        
#定义关注模型
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"


class Topic(models.Model):
    #话题标题
    topictitle = models.CharField(max_length=50)
    #话题下的tag
    topictags = models.TextField()
    #话题描述
    topicdescription = models.TextField()

class Activity(models.Model):
    #活动标题
    activitytitle = models.CharField(max_length=50)
    #活动封面图
    activitycoverimage = models.TextField()
    #活动内容
    activitycontent = models.TextField()
    #活动发布时间
    activitypublish_time = models.DateTimeField(auto_now_add=True)
    #活动开始时间
    activitystart_time = models.DateTimeField()
    #活动结束时间
    activityend_time = models.DateTimeField()
    #活动组织者
    activityorganizer = models.CharField(max_length=50)
    #联系方式
    activitycontract = models.CharField(max_length=50)
