# coding:utf-8
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.db.models import Sum
from ttsx_user.user_decorators import user_login

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
