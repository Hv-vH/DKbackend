from django.urls import path
from .views import (LoginView,RegisterView,TestView,UserProfileView,PostView,
                    FollowListView, FollowUserView, UnfollowUserView,TopicView,
                    CommentView,MessageView, UnreadMessageCountView,LikePostView,
                    LikeArticleView, LikeCommentView,CollectPostView, CollectArticleView)


urlpatterns = [
    path('login/',LoginView.as_view(),name='login'),
    path('register/',RegisterView.as_view(),name='register'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('post/',PostView.as_view(),name='post'),
    path('post/<int:pk>/',PostView.as_view(),name='post'),
    path('test/',TestView.as_view(),name='test'),
    path('follows/', FollowListView.as_view(), name='follow-list'),
    path('follows/', FollowUserView.as_view(), name='follow-user'),
    path('follows/<int:pk>/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('messages/', MessageView.as_view(), name='messages'),
    path('messages/<int:pk>/', MessageView.as_view(), name='message-detail'),
    path('messages/unread/count/', UnreadMessageCountView.as_view(), name='unread-message-count'),
    path('messages/read/', MessageView.as_view(), name='messages-read'),
    path('messages/<int:pk>/read/', MessageView.as_view(), name='message-read'),
    path('follows/', FollowListView.as_view(), name='follow-list'),
    path('follows/', FollowUserView.as_view(), name='follow-user'),
    path('follows/<int:pk>/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('topic/',TopicView.as_view(),name='topic'),
    path('topic/<int:pk>/',TopicView.as_view(),name='topic'),
    path('test/',TestView.as_view(),name='test'),
    path('comment/',CommentView.as_view(),name='comment'),
    path('posts/<int:post_id>/like', LikePostView.as_view(), name='like_post'),
    path('articles/<int:article_id>/like', LikeArticleView.as_view(), name='like_article'),
    path('comments/<int:comment_id>/like', LikeCommentView.as_view(), name='like_comment'),
    path('activity/collect/<int:post_id>', CollectPostView.as_view(), name='collect_post'),
    path('article/collect/<int:article_id>', CollectArticleView.as_view(), name='collect_article'),
]



