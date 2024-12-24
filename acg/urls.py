from django.urls import path
from django.views.generic import RedirectView
from .views import (LoginView,RegisterView,TestView,UserProfileView,PostView,
                    FollowListView, FollowUserView, UnfollowUserView,TopicView,
                    CommentView,MessageView, UnreadMessageCountView)


urlpatterns = [
    path('', RedirectView.as_view(url='login/', permanent=False)),
    path('login/',LoginView.as_view(),name='login'),
    path('register/',RegisterView.as_view(),name='register'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('post/',PostView.as_view(),name='post'),
    path('post/<int:pk>/',PostView.as_view(),name='post'),
<<<<<<< HEAD
    path('test/',TestView.as_view(),name='test'),
    path('follows/', FollowListView.as_view(), name='follow-list'),
    path('follows/', FollowUserView.as_view(), name='follow-user'),
    path('follows/<int:pk>/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('follows/', FollowListView.as_view(), name='follow-list'),
    # 获取关注列表 path('api/follows/', FollowUserView.as_view(), name='follow-user'),  # 关注用户 path('api/follows/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),  # 取消关注
=======
    path('messages/', MessageView.as_view(), name='messages'),
    path('messages/<int:pk>/', MessageView.as_view(), name='message-detail'),
    path('messages/unread/count/', UnreadMessageCountView.as_view(), name='unread-message-count'),
    path('api/follows/', FollowListView.as_view(), name='follow-list'),
    path('api/follows/', FollowUserView.as_view(), name='follow-user'),
    path('api/follows/<int:pk>/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('topic/',TopicView.as_view(),name='topic'),
    path('topic/<int:pk>/',TopicView.as_view(),name='topic'),
    path('test/',TestView.as_view(),name='test'),
    path('comment/',CommentView.as_view(),name='comment'),

>>>>>>> b40e5caf891bffb9fe8083ff6b4231a81d535c0a
]


