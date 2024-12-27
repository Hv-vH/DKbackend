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
    path('test/',TestView.as_view(),name='test'),
    path('follows/', FollowListView.as_view(), name='follow-list'),
    path('follows/', FollowUserView.as_view(), name='follow-user'),
    path('follows/<int:pk>/', UnfollowUserView.as_view(), name='unfollow-user'),
    #获取消息列表和发送新消息
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
    path('comment/',CommentView.as_view(),name='comment'),
]



