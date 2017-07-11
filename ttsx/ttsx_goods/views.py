#coding=utf-8
from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator
import datetime
# Create your views here.
def index(request):
    goods_list=[]#[{},{},{}]===>{'typeinfo':,'new_list':,'click_list':}
    #查询分类对象
    #查询每个分类中最新的4个商品
    #查询每个分类中最火的4个商品
    type_list=TypeInfo.objects.all()
    for t1 in type_list:
        nlist=t1.goodsinfo_set.order_by('-id')[0:4]
        clist=t1.goodsinfo_set.order_by('-gclick')[0:4]
        goods_list.append({'t1':t1,'nlist':nlist,'clist':clist})
    context={'title':'首页','glist':goods_list,'cart_show':'1'}
    return render(request,'ttsx_goods/index.html',context)

def goods_list(request,tid,pindex,orderby):
    try:
        t1=TypeInfo.objects.get(pk=int(tid))
        new_list=t1.goodsinfo_set.order_by('-id')[0:2]
        desc = 1
        #查询：当前分类的所有商品，按每页15个来显示
        if orderby=='1':
            # 默认排序
            glist=t1.goodsinfo_set.order_by('-id')
        elif orderby=='2':
            # 价格排序
            desc = int(request.GET.get('desc',1))
            if desc==1:
                glist = t1.goodsinfo_set.order_by('-gprice')

            elif desc==2:
                glist = t1.goodsinfo_set.order_by('gprice')

        elif orderby=='3':
            # 点击量排序
            glist = t1.goodsinfo_set.order_by('-gclick')
        paginator=Paginator(glist,3)
        pindex1=int(pindex)
        if pindex1<1:
            pindex1=1
        elif pindex1>paginator.num_pages:
            pindex1=paginator.num_pages,
        # 分页页码的列表
        page_range = []
        if paginator.num_pages <= 5:
            page_range = range(1,paginator.num_pages+1)
        else:
            if pindex1 <= 2:
                page_range = range(1,6)
            elif pindex1 >=paginator.num_pages-1:
                page_range = range(paginator.num_pages-4,paginator.num_pages+1)
            else:
                page_range = range(pindex1-2,pindex1+3)
        page=paginator.page(pindex1)
        context={'title':'商品列表页','cart_show':'1','t1':t1,'new_list':new_list,'page':page,'tid':tid,
                 'pindex':pindex,'orderby':orderby,'desc':desc,'page_range':page_range}
        return render(request,'ttsx_goods/list.html',context)
    except Exception as e:
        print(type(e), e)
        return render(request,'404.html')

def detail(request,id):
    try:
        goods=GoodsInfo.objects.get(pk=int(id))
        goods.gclick+=1
        goods.save()
        new_list=goods.gtype.goodsinfo_set.order_by('-id')[0:2]
        context={'title':'商品详细页','cart_show':'1','goods':goods,'new_list':new_list}
        response = render(request,'ttsx_goods/detail.html',context)
        ids = request.COOKIES.get('goods_ids')
        ids = [] if ids is None else ids.split(',')
        if id in ids:
            ids.remove(id)
        ids.insert(0, id)
        response.set_cookie('goods_ids', ','.join(ids[:5]), max_age=60*60*24*7)
        return response
    except Exception as e:
        print(type(e), e)
        return render(request,'404.html')

'''
列表页：排序，页码控制
最近浏览
全文检索

购物车：模型类，视图，模板，列表页购买，详细页购买，
订单：模型类，购买，事务处理
'''

from haystack.generic_views import SearchView

class MySearchView(SearchView):
    """My custom search view."""

    def get_context_data(self, *args, **kwargs):
        context = super(MySearchView, self).get_context_data(*args, **kwargs)
        # do something
        context['title'] = '搜索商品列表页'
        pindex1 = context['page_obj'].number
        # 分页页码的列表
        page_range = []
        if context['paginator'].num_pages <= 5:
            page_range = range(1, context['paginator'].num_pages + 1)
        else:
            if pindex1 <= 2:
                page_range = range(1, 6)
            elif pindex1 >= context['paginator'].num_pages - 1:
                page_range = range(context['paginator'].num_pages - 4, context['paginator'].num_pages + 1)
            else:
                page_range = range(pindex1 - 2, pindex1 + 3)
        context['page_range'] = page_range
        print(context)
        return context
