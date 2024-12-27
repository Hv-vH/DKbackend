from django.urls import path
from .views import (LoginView,RegisterView,TestView,UserProfileView,PostView,
                    FollowView,TopicView,
                    CommentView,MessageView, UnreadMessageCountView,LikePostView,
                    LikeArticleView, LikeCommentView,PostCollectionView,ArticleCollectionView)


urlpatterns = [
    path('login/',LoginView.as_view(),name='login'),
    path('register/',RegisterView.as_view(),name='register'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('post/',PostView.as_view(),name='post'),
    path('post/<int:pk>/',PostView.as_view(),name='post'),
    path('test/',TestView.as_view(),name='test'),
    path('follows/list/', FollowView.as_view(), name='follow-list'),  # 获取关注列表
    path('follows/user/', FollowView.as_view(), name='follow-user'),  # 关注用户
    path('follows/<int:user_id>/', FollowView.as_view(), name='unfollow-user'),  # 取消关注
    path('messages/', MessageView.as_view(), name='messages'),
    #处理单条消息的操作（GET 请求：获取单条消息详情   DELETE 请求：删除单条消息）
    path('messages/<int:pk>/', MessageView.as_view(), name='message-detail'),
    #获取未读消息数量
    path('messages/unread/count/', UnreadMessageCountView.as_view(), name='unread-message-count'),
    #批量标记消息为已读
    path('messages/read/', MessageView.as_view(), name='messages-read'),
    #标记单条消息为已读
    path('messages/read/<int:pk>/', MessageView.as_view(), name='message-read'),
    path('topic/',TopicView.as_view(),name='topic'),
    path('topic/<int:pk>/',TopicView.as_view(),name='topic'),
    path('test/',TestView.as_view(),name='test'),
    path('comment/', CommentView.as_view(), name='comment'),
    path('like/post/<int:post_id>/', LikePostView.as_view(), name='like_post'),
    path('like/article/<int:article_id>/', LikeArticleView.as_view(), name='like_article'),
    path('like/comment/<int:comment_id>/', LikeCommentView.as_view(), name='like_comment'),
    path('posts/<int:post_id>/collect/', PostCollectionView.as_view(), name='collect-post'),  # 收藏帖子
    path('posts/<int:post_id>/uncollect/', PostCollectionView.as_view(), name='uncollect-post'),  # 取消收藏帖子
    path('articles/<int:article_id>/collect/', ArticleCollectionView.as_view(), name='collect-article'),  # 收藏文章
    path('articles/<int:article_id>/uncollect/', ArticleCollectionView.as_view(), name='uncollect-article'),  # 取消收藏文章
]



