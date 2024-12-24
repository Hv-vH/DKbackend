from django.urls import path
from .views import LoginView,RegisterView,TestView,UserProfileView,PostView,FollowListView, FollowUserView, UnfollowUserView


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
    path('follows/', FollowListView.as_view(), name='follow-list'),
    # 获取关注列表 path('api/follows/', FollowUserView.as_view(), name='follow-user'),  # 关注用户 path('api/follows/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),  # 取消关注
]


