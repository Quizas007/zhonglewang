from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from .models import User
from django.contrib.auth.hashers import check_password as auth_check_password

# 用户注册
class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(
        widget=widgets.PasswordInput(
            attrs={
                "class":"pwd",
                "placeholder":"请再次输入密码",
            }
        )
    )
    mobile_captcha = forms.CharField(
        widget=widgets.TextInput(
            attrs={
                "style":"width:142px;",
                "class":"validinput",
                "palceholder":"验证码",
                "error_messages":{
                    "invalid":"验证码错误"
                }
            }
        )
    )
    class Meta:
        model = User
        fields = {"username","mobile","password"}
        widgets = {
            'username':widgets.TextInput(
                attrs={
                    "class":"username",
                    "placeholder":"请输入用户名",
                }
            ),
            'mobile':widgets.TextInput(
                attrs={
                    "class":"phone",
                    "placeholder":"请输入手机号",
                }
            ),
            'password':widgets.PasswordInput(
                attrs={
                    "class":"pwd",
                    "placeholder":"请输入密码",
                }
            )
        }

    # username是否重复django会自动检查，因为它是unique的，所以不需要自己写clean_username

    def clean_mobile(self):
        ret = User.objects.filter(mobile=self.cleaned_data.get("mobile"))
        if not ret:
            return self.cleaned_data.get("mobile")
        else:
            raise ValidationError("手机号已绑定")

    def clean_password(self):
        data = self.cleaned_data.get("password")
        if not data.isdigit():
            return self.cleaned_data.get("password")
        else:
            raise ValidationError("密码不能全是数字")

    def clean(self):
        if self.cleaned_data.get("password") == self.cleaned_data.get("password2"):
            return self.cleaned_data
        else:
            raise ValidationError("两次密码不一致")

# 用户登录
# 因为是登录功能，所以不适合ModelForm。
# ModelForm对于unique字段会检查是否已经存在，如果存在，is_valid结果会为False

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=widgets.TextInput(
            attrs={
                "class":"username",
                "placeholder":"请输入用户名"
            }
        )
    )
    password = forms.CharField(
        widget=widgets.PasswordInput(
            attrs={
                "class":"pwd",
                "placeholder":"请输入密码"
            }
        )
    )

    def check_password(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        try:
            user = User.objects.get(username=username)
            return user,auth_check_password(password,user.password)
        except:
            return None,False

    def clean_username(self):
        ret = User.objects.filter(username=self.cleaned_data.get("username"))
        if ret:
            return self.cleaned_data.get("username")
        else:
            raise ValidationError("用户名或密码不正确")
