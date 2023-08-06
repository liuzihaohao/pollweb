import time,datetime
from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse,HttpResponseForbidden
from django.contrib.auth.models import User
from .models import *

# Create your views here.

@login_required
def root_page(request):
    return redirect("/poll/list/")

@login_required
def list_poll(request):
    page = request.GET.get('page',1)
    limit = 30
    all_count=None
    if request.user.is_superuser:
        all_count=Activity.objects.all()
    else:
        all_count=Activity.objects.filter(registered_list=request.user)
    paginator = Paginator(all_count, limit)
    page_1 = paginator.get_page(page)
    return render(request,"poll/view.html",{"request":request,"obj":page_1})

@login_required
def add_poll(request):
    if request.user.is_superuser or request.user.is_staff:
        if request.method=="GET":
            return render(request,"poll/add.html",{"request":request,"User":User.objects.all()})
        else:
            title=request.POST.get("title")
            if not title:messages.add_message(request, messages.ERROR,'标题不能为空');return render(request,"poll/add.html",{"request":request,"User":User.objects.all()})
            text=request.POST.get("text")
            if not text:messages.add_message(request, messages.ERROR,'简介不能为空');return render(request,"poll/add.html",{"request":request,"User":User.objects.all()})
            question_list=request.POST.get("question_list")
            if not question_list:messages.add_message(request, messages.ERROR,'题目列表不能为空');return render(request,"poll/add.html",{"request":request,"User":User.objects.all()})
            
            start_time_y=request.POST.get("start_time_y")
            start_time_m=request.POST.get("start_time_m")
            start_time_d=request.POST.get("start_time_d")
            start_time_h=request.POST.get("start_time_h")
            start_time_f=request.POST.get("start_time_f")
            start_time_s=request.POST.get("start_time_s")
            
            end_time_y=request.POST.get("end_time_y")
            end_time_m=request.POST.get("end_time_m")
            end_time_d=request.POST.get("end_time_d")
            end_time_h=request.POST.get("end_time_h")
            end_time_f=request.POST.get("end_time_f")
            end_time_s=request.POST.get("end_time_s")
            
            start_time=end_time=None
            
            try:
                start_time=datetime.datetime(int(start_time_y),int(start_time_m),int(start_time_d),int(start_time_h),int(start_time_f),int(start_time_s))
                end_time=datetime.datetime(int(end_time_y),int(end_time_m),int(end_time_d),int(end_time_h),int(end_time_f),int(end_time_s))
            except Exception:
                messages.add_message(request, messages.ERROR,'时间格式不正确');return render(request,"poll/add.html",{"request":request,"User":User.objects.all()})
            
            public_grade=request.POST.get("public_grade")
            
            registered_list=request.POST.getlist("registered_list")
            admins=request.POST.getlist("admins")
            
            if not len(admins):messages.add_message(request, messages.ERROR,'此题目的管理员不能为空');return render(request,"poll/add.html",{"request":request,"User":User.objects.all()})
            is_all_registered=True if request.POST.get("is_all_registered") else False
            is_active=True if request.POST.get("is_active") else False
            
            obj=Activity.objects.create(
                title=title,
                text=text,
                start_time=start_time,
                end_time=end_time,
                public_grade=public_grade,
                is_all_registered=is_all_registered,
                question_list=question_list,
                is_active=is_active,
            )
            temp=[]
            print(registered_list)
            for i in admins:
                temp=temp+[User.objects.get(username=i).id]
            obj.admins.set(temp)
            temp=[]
            for i in registered_list:
                temp=temp+[User.objects.get(username=i).id]
            obj.registered_list.set(temp)
            messages.add_message(request, messages.SUCCESS,'创建成功')
            return redirect("/poll/list/")
    return redirect("/")