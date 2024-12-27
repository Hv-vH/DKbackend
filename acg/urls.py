from django.urls import path
from .views import (LoginView,RegisterView,TestView,UserProfileView,PostView,
                    FollowView,TopicView,
                    CommentView,MessageView, UnreadMessageCountView,LikePostView,
                    LikeArticleView, LikeCommentView,CollectPostView, CollectArticleView,UncollectArticleView,UncollectPostView)


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
    path('messages/<int:pk>/', MessageView.as_view(), name='message-detail'),
    path('messages/unread/count/', UnreadMessageCountView.as_view(), name='unread-message-count'),
    path('messages/read/', MessageView.as_view(), name='messages-read'),
    path('messages/<int:pk>/read/', MessageView.as_view(), name='message-read'),
    path('topic/',TopicView.as_view(),name='topic'),
    path('topic/<int:pk>/',TopicView.as_view(),name='topic'),
    path('test/',TestView.as_view(),name='test'),
    path('comment/', CommentView.as_view(), name='comment'),
    path('like/post/<int:post_id>/', LikePostView.as_view(), name='like_post'),
    path('like/article/<int:article_id>/', LikeArticleView.as_view(), name='like_article'),
    path('like/comment/<int:comment_id>/', LikeCommentView.as_view(), name='like_comment'),
    path('collect/post/<int:post_id>/', CollectPostView.as_view(), name='collect_post'),
    path('article/collect/<int:article_id>/', CollectArticleView.as_view(), name='collect_article'),
    path('uncollect/post/<int:post_id>', UncollectPostView.as_view(), name='uncollect_post'),
    path('article/uncollect/<int:article_id>', UncollectArticleView.as_view(), name='uncollect_article'),
]



