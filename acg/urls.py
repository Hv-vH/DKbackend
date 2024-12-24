from django.urls import path
from .views import (LoginView,RegisterView,TestView,UserProfileView,PostView,
                    FollowListView, FollowUserView, UnfollowUserView,TopicView,
                    CommentView,MessageView, UnreadMessageCountView)


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
    path('api/follows/', FollowListView.as_view(), name='follow-list'),
    path('api/follows/', FollowUserView.as_view(), name='follow-user'),
    path('api/follows/<int:pk>/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('topic/',TopicView.as_view(),name='topic'),
    path('topic/<int:pk>/',TopicView.as_view(),name='topic'),
    path('test/',TestView.as_view(),name='test'),
    path('comment/',CommentView.as_view(),name='comment'),
]



