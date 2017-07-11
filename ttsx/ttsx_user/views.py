#coding=utf-8
from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
from hashlib import sha1
import datetime
from .user_decorators import *
from ttsx_goods import models
# Create your views here.
def register(request):
    context={'title':'注册','top':'0'}
    return render(request,'ttsx_user/register.html',context)
def register_handle(request):
    #接收数据
    post=request.POST
    uname=post.get('user_name')
    upwd=post.get('user_pwd')
    umail=post.get('user_email')
    #加密
    upwd = bytes(upwd, 'utf-8')
    s1=sha1()
    s1.update(upwd)
    upwd_sha1=s1.hexdigest()
    #创建对象
    user=UserInfo()
    user.uname=uname
    user.upwd=upwd_sha1
    user.umail=umail
    user.save()
    #完成后转向
    return redirect('/user/login/')
def register_valid(request):
    uname=request.GET.get('uname')
    result=UserInfo.objects.filter(uname=uname).count()
    context={'valid':result}
    return JsonResponse(context)

def login(request):
    if request.session.has_key('uid'):
        return redirect('/user/')
    uname=request.COOKIES.get('uname','')
    context={'title':'登录','uname':uname,'top':'0'}
    return render(request,'ttsx_user/login.html',context)
def login_handle(request):
    post=request.POST
    uname=post.get('user_name')
    upwd=post.get('user_pwd')
    uname_jz=post.get('name_jz','0')

    upwd = bytes(upwd, 'utf-8')
    s1=sha1()
    s1.update(upwd)
    upwd_sha1=s1.hexdigest()

    context = {'title': '登录','uname':uname,'upwd':upwd,'top':'0'}
    #根据用户名查询数据，如果未查到返回[]，如果查到则返回[UserInfo]
    users=UserInfo.objects.filter(uname=uname)
    if len(users)==0:
        #用户名错误
        context['name_error']='1'
        return render(request,'ttsx_user/login.html',context)
    else:
        if users[0].upwd==upwd_sha1: #登录成功
            #记录当前登录的用户
            request.session['uid']=users[0].id
            request.session['uname']=uname
            #记住用户名
            path=request.session.get('url_path','/')
            response=redirect(path)
            if uname_jz=='1':
                response.set_cookie('uname',uname,expires=datetime.datetime.now() + datetime.timedelta(days = 7))
            else:
                response.set_cookie('uname','',max_age=-1)
            return response
        else:
            #密码错误
            context['pwd_error']='1'
            return render(request, 'ttsx_user/login.html', context)
def logout(request):
    request.session.flush()
    return redirect('/user/login/')

def islogin(request):

    if request.session.get('uid') is None:
        return JsonResponse({'islogin':0})
    else:
        return JsonResponse({'islogin':1})

@user_login
def center(request):
    try:
        user=UserInfo.objects.get(pk=request.session['uid'])
        ids_zj = request.COOKIES.get('goods_ids')
        ids_zj = [] if ids_zj is None else ids_zj.split(',')
        goods_zj = []
        for id in ids_zj:
            goods_zj.append(models.GoodsInfo.objects.get(id=id))
        context={'title':'用户中心','user':user,'goods_zj':goods_zj}
        return render(request,'ttsx_user/center.html',context)
    except Exception as e:
        print(type(e), e)
        return render(request, '404.html')
@user_login
def order(request):
    context={'title':'用户订单'}
    return render(request,'ttsx_user/order.html',context)
@user_login
def site(request):
    user=UserInfo.objects.get(pk=request.session['uid'])
    if request.method=='POST':
        post=request.POST
        user.ushou=post.get('ushou')
        user.uaddress=post.get('uaddress')
        user.ucode=post.get('ucode')
        user.uphone=post.get('uphone')
        user.save()
    context={'title':'收货地址','user':user}
    return render(request,'ttsx_user/site.html',context)



'''
在页面A中，转到登录页，登录完成后，转回A页
****=request.path

第一个问题：如果这段代码写在视图中，则需要维护的视图非常多
第二个问题：对于必须登录的页面，由于装饰器的影响，在未登录时，并不会执行
问题一的解决：让可以在每个视图中执行
问题二的解决：在视图执行前执行
'''

