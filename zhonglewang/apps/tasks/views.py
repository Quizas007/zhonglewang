from django.shortcuts import render,redirect,reverse
from django.core.paginator import Paginator
from django.db.models import Q
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Category,Tasks
from apps.accounts.models import User
from .forms import TaskCreateForm
from django.http import HttpResponse,JsonResponse
import logging
logger = logging.getLogger('tasks')

def freelist(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    # 取出所有自由模式的任务
    tasks_free = Tasks.objects.filter(mode=1)
    # 根据GET请求中查询条件返回不同排序的对象数组
    if search:
        if order == 'total_views':
            # 联合搜索
            tasks_free = tasks_free.filter(
                Q(title__icontains=search)|
                Q(content__icontains=search)
            ).order_by('-total_views')
            order = 'total_views'
        else:
            tasks_free = tasks_free.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search)
            )
            order = 'normal'
    else:
        # 将search参数重置为空
        search = ''
        if order == 'total_views':
            tasks_free = tasks_free.order_by('-total_views')
    # 每页显示的任务数量
    paginator = Paginator(tasks_free, 3)
    # 获取url中的页码
    page = request.GET.get('page',1)
    # 将导航对象响应的页码内容返回给tasks
    tasks_free = paginator.page(page)
    kwgs = {
        'tasks_free':tasks_free,
        'order':order,
        'search':search,
    }
    return render(request,'task_freelist.html',kwgs)

def securitylist(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    # 取出所有担保模式的任务
    tasks_security = Tasks.objects.filter(mode=2)
    # 根据GET请求中查询条件返回不同排序的对象数组
    if search:
        if order == 'total_views':
            # 联合搜索
            tasks_security = tasks_security.filter(
                Q(title__icontains=search)|
                Q(content__icontains=search)
            ).order_by('-total_views')
            order = 'total_views'
        else:
            tasks_security = tasks_security.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search)
            )
            order = 'normal'
    else:
        # 将search参数重置为空
        search = ''
        if order == 'total_views':
            tasks_security = tasks_security.order_by('-total_views')
    # 每页显示的任务数量
    paginator = Paginator(tasks_security, 3)
    # 获取url中的页码
    page = request.GET.get('page',1)
    # 将导航对象响应的页码内容返回给tasks
    tasks_security = paginator.page(page)
    kwgs = {
        'tasks_security':tasks_security,
        'order':order,
        'search':search,
    }
    return render(request,'task_securitylist.html',kwgs)

class TaskCreate(LoginRequiredMixin,View):
    def get(self,request):
        category = Category.objects.all().values("id", "name")
        mode = Tasks.MODE_CHOICES
        kwgs = {
            'category':category,
            'mode':mode
        }
        return render(request,'task_create.html',kwgs)
    def post(self,request):
        task_create_form = TaskCreateForm(request.POST,request.FILES)
        if task_create_form.is_valid():
            new_task = task_create_form.save(commit=False)
            new_task.publisher = User.objects.get(id=request.user.id)
            if request.POST['category'] != 'none':
                new_task.category = Category.objects.get(id=request.POST['category'])
            new_task.save()
            task_create_form.save_m2m()
            return redirect(reverse("tasks:freelist"))
        else:
            return HttpResponse("表单内容有误，请重新填写。")

def free_detail(request,id):
    # 取出对应的文章
    task = Tasks.objects.get(id=id)
    # 浏览量+1
    task.total_views += 1
    task.save(update_fields=['total_views'])
    # 参数
    kwgs = {
        'task': task
    }
    return render(request,'task_free_detail.html')

def security_detail(request,id):
    # 取出对应的文章
    task = Tasks.objects.get(id=id)
    # 浏览量+1
    task.total_views += 1
    task.save(update_fields=['total_views'])
    # 参数
    kwgs = {
        'task':task
    }
    return render(request,'task_security_detail.html',kwgs)