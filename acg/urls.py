from django.urls import path
from .views import LoginView,RegisterView,TestView,UserProfileView,PostView,MessageView, UnreadMessageCountView
from django.views.generic import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='login/', permanent=False)),
    path('login/',LoginView.as_view(),name='login'),
    path('register/',RegisterView.as_view(),name='register'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('post/',PostView.as_view(),name='post'),
    path('post/<int:pk>/',PostView.as_view(),name='post'),
    path('test/',TestView.as_view(),name='test'),
    path('messages/', MessageView.as_view(), name='messages'),
    path('messages/<int:pk>/', MessageView.as_view(), name='message-detail'),
    path('messages/unread/count/', UnreadMessageCountView.as_view(), name='unread-message-count'),
]


