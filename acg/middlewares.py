from django.utils.deprecation import MiddlewareMixin
from rest_framework.authentication import get_authorization_header
from django.conf import settings
from rest_framework import exceptions
from jwt.exceptions import ExpiredSignatureError
from django.contrib.auth.models import User, AnonymousUser
import jwt
from django.http.response import JsonResponse
from rest_framework import status
import re

class LogCostMiddleware(MiddlewareMixin):

    keyword = 'JWT'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 对于那些不需要登录就能访问的接口，可以写在这里
        # 静态路径匹配
        self.white_list = ['/acg/login/',
                           '/acg/register/',
                           '/acg/post/',
                           '/acg/messages/unread/count/',
                           ]
        # 使用正则表达式匹配动态路径
        self.white_list_patterns = [
            # 匹配动态路径 '/acg/post/<int:pk>/
            re.compile(r'^/acg/post/\d+/'),
        ]

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        #如果返回None,那么会正常执行视图函数以及其他中间件
        #如果返回HttpResponse对象,那么不会执行视图函数以及其他中间件

        #静态路径匹配
        if request.path in self.white_list:
            request.user = AnonymousUser()
            request.auth = None
            return None
        #动态路径匹配
        for pattern in self.white_list_patterns:
            if pattern.match(request.path):
                # 匹配成功，直接返回
                request.user = AnonymousUser()
                request.auth = None
                return None

        try:
            auth = get_authorization_header(request).split()

            if not auth or auth[0].lower() != self.keyword.lower().encode():
                raise exceptions.ValidationError('请传入JWT Token！')

            if len(auth) == 1:
                msg = "不可用的JWT请求头！"
                raise exceptions.AuthenticationFailed(msg)
            elif len(auth) > 2:
                msg = '不可用的JWT请求头！JWT Token中间不应该有空格！'
                raise exceptions.AuthenticationFailed(msg)

            try:
                jwt_token = auth[1]
                jwt_info = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms='HS256')
                userid = jwt_info.get('userid')
                try:
                    # 绑定当前user到request对象上
                    user = User.objects.get(pk=userid)
                    request.user = user
                    request.auth = jwt_token
                except:
                    msg = '用户不存在！'
                    raise exceptions.AuthenticationFailed(msg)
            except ExpiredSignatureError:
                msg = "JWT Token已过期！"
                raise exceptions.AuthenticationFailed(msg)

        except Exception as e:
            print(e)
            return JsonResponse({'detail': '请先登录'}, status=status.HTTP_403_FORBIDDEN)