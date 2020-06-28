"""MyWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from MySite import views as siteviews  # 从项目的包中导入视图模块

urlpatterns = {
    # path('', siteviews.index),
    # path('filter/', siteviews.fiter_test),
    # path('news_list/<str:news_type>', siteviews.news_list),
    path('admin/', admin.site.urls),
    path('',siteviews.index),
    # path('reg/', siteviews.reg),  # 打开注册页面
    # path('register/', siteviews.register),  # 提交注册
    # path('check/', siteviews.check),  # 检查用户名是否注册
    # path('change/', siteviews.change),  # 打开修改密码页面
    # path('changepass/', siteviews.changepass),  # 提交密码修改
    path('all/', siteviews.searchall),#所有商品信息
    path('search_name/', siteviews.searchname),#按名称搜索界面
    path('search_price/', siteviews.searchprice),#按价格搜索界面
    path('search_sort/', siteviews.searchsort),#排序后显示界面
    path('goods_list/', siteviews.goodslist),#商品清单
    path('add/', siteviews.add),#添加
    path('del/', siteviews.delete),#删除
    path('search/', siteviews.search),

}
