from django.shortcuts import render,HttpResponse
from django.contrib import auth
from django.http import JsonResponse
import json
from app01.utils import valid_code
from django import forms
from django.forms import widgets
from .models import *
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError

def login(request):
    if request.method=="POST":
        user=request.POST.get("user")
        pwd=request.POST.get("pwd")
        input_valid_codes=request.POST.get("valid_code")    #用户输入的验证码
        keep_valid_codes=request.session.get("keep_valid_codes")    #随机生成的验证码
        '''
        1  拿到cookie中sessionid对应的随机字符串
        2  在django-session表中过滤记录
        3  .... 
        '''
        login_response={"user":None,"error_msg":""}     #返回错误信息
        if keep_valid_codes.upper()==input_valid_codes.upper():     # 校验验证码
            user=auth.authenticate(username=user,password=pwd)
            if user:
                auth.login(request,user)    #用户登录成功，设置session
                login_response["user"]=user.username
            else:
                login_response["error_msg"] = "username or password error!"
        else:
            login_response["error_msg"]="valid_code error!"
        return HttpResponse(json.dumps(login_response))
    else:
        return render(request,"login.html")

def get_valid_img(request):     #生成验证码
    data=valid_code.get_valid_value(request)
    return HttpResponse(data)

def index(request):
    print("==",request.user)
    return render(request,"index.html")

class RegForm(forms.Form):      #form组件进行验证
    user = forms.CharField(label="登录名称", min_length=4, max_length=16,
                           widget=widgets.TextInput(
                               attrs={"class": "form-control", "placeholder": "用户名至少4位"}),
                           error_messages={"min_length": "太短", "required": "必填"})

    pwd = forms.CharField(label="密  码", min_length=6,
                          widget=widgets.PasswordInput(
                              attrs={"class": "form-control","placeholder": "密码至少6位"}),
                          error_messages={"min_length": "太短", "required": "必填"})

    repeat_pwd = forms.CharField(label="确认密码", min_length=6,
                           widget=widgets.PasswordInput(
                               attrs={"class": "form-control","placeholder": "请输入确认密码"}),
                           error_messages={"min_length": "太短", "required": "必填"})

    # pwd=forms.CharField(
    #     widget=widgets.PasswordInput(attrs={"class": "form-control"}))
    #
    # repeat_pwd=forms.CharField(
    #     widget=widgets.PasswordInput(attrs={"class": "form-control"}))

    email = forms.EmailField(
                              error_messages={'required': u'邮箱不能为空', 'invalid': u'邮箱格式错误！'},
                              widget=widgets.TextInput(attrs={'class': "form-control", 'placeholder': u'请输入邮箱账号'}))

    def clean_user(self):
        val = self.cleaned_data.get("user")
        if not val.isdigit():
            return val
        else:
            raise ValidationError("用户名不能是纯数字！")

    def clean(self):
        pwd = self.cleaned_data.get("pwd")
        repeat_pwd = self.cleaned_data.get("repeat_pwd")
        print(pwd, repeat_pwd)
        if pwd == repeat_pwd:
            return self.cleaned_data
        else:
            raise ValidationError("确认密码错误！")

def register(request):
    if request.is_ajax():   #如果提交的是ajax请求
        print("request.POST",request.POST)   # <QueryDict: {'user': ['123'], 'pwd': ['1231'], 'repeat_pwd': ['1231'], 'email': ['123'], 'csrfmiddlewaretoken': ['PjMKenIgrFYWY52U5EcYbkfmib2EiMzK19K5xv4qBon5XZbPDkuiMhMf2LqaV2wy']}>
        print("request.FILES",request.FILES) # request.FILES <MultiValueDict: {'avatar_img': [<InMemoryUploadedFile: linhaifeng.jpg (image/jpeg)>]}>
        form_obj = RegForm(request.POST)
        reg_response={"user":None,"error_mes":None}     #为前端返回状态信息
        if form_obj.is_valid():     #验证信息通过
            user=form_obj.cleaned_data.get("user")
            pwd=form_obj.cleaned_data.get("pwd")
            email=form_obj.cleaned_data.get("email")
            avatar_img=request.FILES.get("avatar_img")
            if avatar_img:  #有头像时，创建用户
                 print("avatar_img....",avatar_img)
                 user=UserInfo.objects.create_user(username=user,password=pwd,email=email,avatar=avatar_img)
            else:
                user = UserInfo.objects.create_user(username=user, password=pwd, email=email)
            reg_response["user"]=user.username
        else:
            reg_response["error_mes"]=form_obj.errors
        return JsonResponse(reg_response)
    else:   # 实例化form组件的类get请求
        form_obj=RegForm()
        return render(request,"reg.html",{"form_obj":form_obj})
