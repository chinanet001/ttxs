# coding:utf-8
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.db.models import Sum
from ttsx_user.user_decorators import user_login
from ttsx_user.models import UserInfo

# Create your views here.


def add(request):
    try:
        gid = request.GET.get('gid')
        uid = request.session.get('uid')
        count = int(request.GET.get('count','1'))

        carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)
        if len(carts) == 1:
            cart = carts[0]
            cart.count += count
            cart.save()
        else:
            cart = CartInfo()
            cart.user_id = uid
            cart.goods_id = gid
            cart.count = count
            cart.save()
        return JsonResponse({'is_add': 'true'})
    except Exception as e:
        print(type(e), e)
        return render(request, '404.html')


def count(request):
    uid = request.session.get('uid')
    cart_count = CartInfo.objects.filter(user_id=uid).count()
    # cart_count = CartInfo.objects.filter(user_id=uid).aggregate(Sum('count')).get('count_sum')
    return JsonResponse({'cart_count':cart_count})

@user_login
def index(request):
    context = {'title': '购物车'}
    uid = request.session.get('uid')
    context['cart_list'] = CartInfo.objects.filter(user_id=uid)
    return render(request, 'cart/cart.html', context)


def edit(request):
    id = int(request.GET.get('id'))
    count = int(request.GET.get('count'))
    cart = CartInfo.objects.get(id= id)
    cart.count = count
    cart.save()
    return JsonResponse({'result':'ok'})


def delete(request):
    id = request.GET.get('id')
    cart = CartInfo.objects.get(pk=id)
    cart.delete()
    return JsonResponse({'result': 'ok'})


def order(request):
    user = UserInfo.objects.get(pk=request.session.get('uid'))
    cart_ids = request.POST.getlist('cart_id')
    c_ids = ','.join(cart_ids)
    cart_list = CartInfo.objects.filter(id__in=cart_ids)
    context = {'title': '提交订单', 'user': user, 'cart_list': cart_list, 'c_ids': c_ids}
    return render(request, 'cart/order.html', context)

