from django.shortcuts import render,redirect,reverse
from django.db import connection

#进行数据库的操作
def get_corsor():
    return connection.cursor()

# Create your views here.
#首页
def index(request):
    cursor = get_corsor()
    cursor.execute("select id,name,author from book")
    books = cursor.fetchall()
    #[(1,'三国演义'，'罗贯中')]
    return  render(request,'index.html',context={"books": books})

#添加书籍
def add_book(request):
    if request.method == 'GET':
        return render(request,'add_book.html')
    else:
        name = request.POST.get("name")
        author = request.POST.get("author")
        cursor = get_corsor()
        cursor.execute("insert into book(id,name,author) values(null ,'%s','%s')" % (name,author))
        # 跳转到首页
        return redirect(reverse('index'))

#书籍详情
def book_detail(request,book_id):
    cursor = get_corsor()
    cursor.execute("select id,name,author from book where id=%s" % book_id)
    book = cursor.fetchone()
    return render(request, 'book_detail.html', context={"book":book})
#删除书籍
def delete_book(request):
    if request.method == 'POST':
        book_id = request.POST.get("book_id")
        cursor = get_corsor()
        cursor.execute("delete from book where id=%s" % book_id)
        return redirect(reverse('index'))
    else:
        raise RuntimeError("删除图书出错！")
