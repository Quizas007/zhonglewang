from django.shortcuts import render,redirect,reverse
from django.views.generic import View
from .forms import RegisterForm,LoginForm
from .models import User
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
import logging
logger = logging.getLogger('account')



class Register(View):
    def get(self,request):
        form = RegisterForm()
        return render(request,"register.html",{"form":form})

    # Ajax提交表单
    def post(self, request):
        from django.core.cache import cache
        ret = {"status": 400, "msg": "调用方式错误"}
        if request.is_ajax():
            form = RegisterForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                mobile = form.cleaned_data["mobile"]
                mobile_captcha = form.cleaned_data["mobile_captcha"]
                mobile_captcha_reids = cache.get(mobile)
                if mobile_captcha == mobile_captcha_reids:
                    user = User.objects.create(username=username, password=make_password(password))
                    user.save()
                    ret['status'] = 200
                    ret['msg'] = "注册成功"
                    logger.debug(f"新用户{user}注册成功！")
                    user = auth.authenticate(username=username, password=password)
                    if user is not None and user.is_active:
                        auth.login(request, user)
                        logger.debug(f"新用户{user}登录成功")
                    else:
                        logger.error(f"新用户{user}登录失败")
                else:
                    # 验证码错误
                    ret['status'] = 401
                    ret['msg'] = "验证码错误或过期"
            else:
                ret['status'] = 402
                ret['msg'] = form.errors
        logger.debug(f"用户注册结果：{ret}")
        return JsonResponse(ret)

class Login(View):
    def get(self,request):
        # 设置下一跳转地址
        request.session["next"] = request.GET.get('next', reverse('index'))
        # 如果已登录，则直接跳转到index页面
        # request.user 表示的是当前登录的用户对象,没有登录 `匿名用户`
        if request.user.is_authenticated:
            return redirect(reverse('index'))
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    # Form表单直接提交
    def post(self, request):
        # 表单数据绑定
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            user, flag = form.check_password()
            # user = auth.authenticate(username=username, password=password)
            if flag and user and user.is_active:
                auth.login(request, user)
                logger.info(f"{user.username}登录成功")
                # 跳转到next
                return redirect(request.session.get("next", '/'))
            msg = "用户名或密码错误"
            logger.error(f"{username}登录失败, 用户名或密码错误")
        else:
            msg = "表单数据不完整"
            logger.error(msg)
        return render(request, "login.html", {"form": form, "msg": msg})

def logout(request):
    auth.logout(request)
    # return redirect(reverse("index"))
    return render(request,"index.html")