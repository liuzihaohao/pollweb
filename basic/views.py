import time
from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse,HttpResponseForbidden
from django.contrib.auth.models import User
from .models import Log
from pollweb.settings import RUN_TIME

# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method=="GET":
        return render(request,"basic/register.html")
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.INFO,'用户名已经存在')
            return redirect("/register/")
        User.objects.create_user(username=username,password=password,email=email)
        return redirect("/login/")
    
def login(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method=="GET":
        return render(request,"basic/login.html")
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        # print(request.GET.get("next"))
        user_obj = auth.authenticate(username=username,password=password)
        if user_obj:
            auth.login(request,user_obj)
            nexts=request.GET.get('next','/')
            return redirect(nexts)
        else:
            messages.add_message(request, messages.INFO,'登录失败')
            return redirect("/login/")

@login_required
def index(request):
    return redirect("/poll/")

@login_required
def logout(request):
    auth.logout(request)
    return redirect("/")

@login_required
def change_password(request):
    if request.method=="GET":
        return render(request,"basic/change_password.html",{"request":request})
    else:
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        r_new_password = request.POST.get("r_new_password")
        if request.user.check_password(old_password):
            if new_password != r_new_password:
                messages.add_message(request, messages.INFO,'两次输入密码的不一样')
                return redirect("/change_password/")
            else:
                request.user.set_password(new_password)
                request.user.save()
                messages.add_message(request, messages.INFO,'修改成功')
                return redirect("/login/")
        else:
            messages.add_message(request, messages.INFO,'旧密码输入错误')
            return redirect("/change_password/")
        
@login_required
def view_log(request):
    if request.user.is_superuser or request.user.is_staff:
        page = request.GET.get('page',1)
        limit = 30
        all_count=None
        all_count=Log.objects.all()
        paginator = Paginator(all_count, limit)
        page_1 = paginator.get_page(page)
        return render(request, "basic/log/view.html",{'page_1':page_1,"request":request})
    return redirect("/")

@login_required
def basic_admin(request):
    if request.user.is_superuser or request.user.is_staff:
        return render(request, "basic/admin.html",{'request':request,"ttm":int(time.time()-RUN_TIME)})
    return redirect("/")

@login_required
def view_user(request):
    if request.user.is_superuser or request.user.is_staff:
        page = request.GET.get('page',1)
        limit = 30
        all_count=None
        all_count=User.objects.all()
        paginator = Paginator(all_count, limit)
        page_1 = paginator.get_page(page)
        return render(request, "basic/user/view.html",{'page_1':page_1,"request":request})
    return redirect("/")

@login_required
def add_user(request):
    if request.user.is_superuser or request.user.is_staff:
        if request.method=="GET":
            return render(request, "basic/user/add.html",{'request':request})
        else:
            username=request.POST.get("username")
            password=request.POST.get("password")
            email=request.POST.get("email")
            is_active=True if request.POST.get("is_active") else False
            is_staff=True if request.POST.get("is_staff") else False
            is_superuser=True if request.POST.get("is_superuser") else False
            if User.objects.filter(username=username):
                messages.add_message(request, messages.ERROR,'用户名已存在')
                return render(request, "basic/user/add.html",{'request':request})
            else:
                User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    is_active=is_active,
                    is_staff=is_staff,
                    is_superuser=is_superuser
                )
                messages.add_message(request, messages.INFO,'创建成功')
                return render(request, "basic/user/add.html",{'request':request})
    return redirect("/")

@login_required
def view_one_user(request,uid):
    return redirect("/basic/user/{}/edit/".format(uid))

@login_required
def edit_user(request,uid):
    if request.user.is_superuser or request.user.is_staff:
        if not User.objects.filter(id=uid):
            messages.add_message(request, messages.ERROR,'用户不存在')
            return redirect("/basic/user/{}/edit/".format(uid))
        
        obj=User.objects.get(id=uid)
        
        if request.method=="GET":
            return render(request, "basic/user/edit.html",{'request':request,"obj":obj})
        else:
            username=request.POST.get("username")
            password=request.POST.get("password")
            email=request.POST.get("email")
            is_active=True if request.POST.get("is_active") else False
            is_staff=True if request.POST.get("is_staff") else False
            is_superuser=True if request.POST.get("is_superuser") else False
            if User.objects.filter(username=username).count()>1:
                messages.add_message(request, messages.ERROR,'用户名已注册')
                return render(request, "basic/user/edit.html",{'request':request,"obj":obj})
            elif User.objects.filter(email=email).count()>1:
                messages.add_message(request, messages.ERROR,'邮箱已注册')
                return render(request, "basic/user/edit.html",{'request':request,"obj":obj})
            else:
                obj.username=username
                if password!="":
                    obj.password=password
                obj.email=email
                obj.is_active=is_active
                obj.is_staff=is_staff
                obj.is_superuser=is_superuser
                obj.save()
                messages.add_message(request, messages.INFO,'修改成功')
                return render(request, "basic/user/edit.html",{'request':request,"obj":obj})
    return redirect("/")