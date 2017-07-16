from django.shortcuts import render, redirect
from django.db import transaction
from .models import *
from datetime import datetime
from ttsx_cart.models import CartInfo
# Create your views here.


@transaction.atomic
def do_order(request):
    is_ok = True
    sid = transaction.savepoint()
    try:
        # 创建主表
        uid = request.session.get('uid')
        now_str = datetime.now().strftime("%Y%m%d%H%M%S")
        main = OrderMain()
        main.order_id = '%s%d' % (now_str, uid)
        main.user_id = uid
        main.total = 0
        main.state = 0
        main.save()
        # 接受所有购物车请求
        cart_ids = request.POST.get('c_ids').split(',')

        # 查询到请求的购物车信息
        cart_list = CartInfo.objects.filter(id__in=cart_ids)
        total = 0
        for cart in cart_list:
            print(cart.count, cart.goods.gkucun)
            # 逐个判断库存
            if cart.count <= cart.goods.gkucun:
                # 创建订单详单
                detail = OrderDetail()
                detail.order = main
                detail.goods = cart.goods
                detail.count = cart.count
                detail.price = cart.goods.gprice
                detail.save()
                # 减库存
                cart.goods.gkucun -= cart.count
                cart.goods.save()
                # 计算小计
                total += cart.count * cart.goods.gprice
                # 删除购物车
                cart.delete()
            else:
                # 回滚事务
                is_ok = False
                transaction.savepoint_rollback(sid)
                break
        if is_ok:
            # 保存小计
            main.total = total
            main.save()
            transaction.savepoint_commit(sid)
    except Exception as e:
        print(type(e), e)
        transaction.savepoint_rollback(sid)
        is_ok = False
    if is_ok:
        return redirect('/user/order/')
    else:
        return redirect('/cart/')

