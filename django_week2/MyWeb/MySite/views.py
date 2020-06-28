from django.shortcuts import render,HttpResponse
from MySite.models import Goods
from MySite.models import Users

from django.core import serializers
from django.db.models import Q
import json


# Create your views here.
#首页视图函数
def index(request):
    return render(request, 'index.html')

#查询全部数据
def searchall(request):
    goods_list = Goods.objects.all()
    return render(request, 'search_result.html', {'goods_list': goods_list})

#查询指定商品名称数据
def searchname(request):
    goods_name = request.GET['goods_name']
    goods_list = Goods.objects.filter(goods_name=goods_name)  # 完全匹配搜索关键字
    # goods_list = Goods.objects.get(goods_name=goods_name)# 查询满足条件的一个结果（查询到多个结果时异常）
    # goods_list = Goods.objects.filter(goods_name__contains=goods_name)  # 模糊匹配搜索关键字
    return render(request, 'search_result.html', {'goods_list': goods_list})

#按价格查询
def searchprice(request):
    min_price = request.GET['min_price']
    max_price = request.GET['max_price']
    goods_list = Goods.objects.filter(goods_price__gt=min_price, goods_price__lt=max_price)  # 满足全部多个条件
    # goods_list = Goods.objects.filter(Q(goods_price=0.5) | Q(goods_price=2.4)) # 满足任何一个条件
    return render(request, 'search_result.html', {'goods_list': goods_list})

#查询后进行排序
def searchsort(request):
    sort = {'all_asc': Goods.objects.order_by('goods_price'),  # 查询全部结果后升序排列
            'all_desc': Goods.objects.order_by('-goods_price'),  # 查询全部结果后降序排列
            'result_asc': Goods.objects.filter(goods_price__lt='5').order_by('goods_price')  # 对某一查询结果排序
            }
    return render(request, 'search_result.html', {'goods_list': sort[request.GET['sort']]})

#注册
def reg(request):
    return render(request, 'register.html')

#修改密码
def change(request):
    return render(request, 'change.html')

#查看用户名是否已注册
def check(request):
    user_name = request.GET['user_name']
    user = Users.objects.filter(user_name=user_name)
    if user:
        status = 100  # 返回表示已注册的编号
    else:
        status = 200  # 返回表示未注册的编号
    return HttpResponse(status)

#注册
def register(request):
    user_name = request.GET['user_name']
    password = request.GET['password']
    try:
        user = Users(user_name=user_name, password=password)
        user.save()
        status = 200  # 返回注册成功的编号
    except:
        status = 100  # 返回注册失败的编号
    return HttpResponse(json.dumps({'status': status}))

#提交密码修改
def changepass(request):
    user_name = request.GET['user_name']
    password = request.GET['password']
    user = Users.objects.filter(user_name=user_name)  # 查询已存在用户的数据对象
    try:
        user.update(password=password)  # 通过数据对象更新数据库中的数据
        status = 200
    except:
        status = 100
    return HttpResponse(json.dumps({'status': status}))

#查看商品清单
def goodslist(request):
    result = Goods.objects.all()
    return render(request, 'goods_list.html', {'goods_list': result})

#添加
def add(request):
    goods_name = request.GET['goods_name']
    goods_price = request.GET['goods_price']
    goods_number = request.GET['goods_number']
    isexist = Goods.objects.filter(goods_name=goods_name)
    try:
        if not isexist:
            goods = Goods()
            goods.goods_name = goods_name
            goods.goods_price = goods_price
            goods.goods_number = goods_number
            goods.save()
            result = 200
        else:
            result = 100
    except:
        result = 100
    return HttpResponse(result)

#删除
def delete(request):
    goods_name = request.GET['goods_name']
    goods = Goods.objects.filter(goods_name=goods_name)
    try:
        goods.delete()
        result = 200
    except:
        result = 100
    return HttpResponse(result)

#搜索
def search(request):
    min_price = int(request.GET['min_price'])
    max_price = int(request.GET['max_price'])
    goods = Goods.objects.filter(goods_price__gte=min_price, goods_price__lte=max_price)
    try:
        if goods:
            result = json.dumps(serializers.serialize('json', goods))
        else:
            result = 100
    except:
        result = 100
    return HttpResponse(result)

