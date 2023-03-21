from django.shortcuts import render

from django.shortcuts import render,redirect
from  django.contrib.auth import authenticate ,login,logout
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.
@login_required
def forum(request):
    context = {}
    cursor = connection.cursor()

    # print(request.method)
    if request.method == 'POST':
        sql = "INSERT INTO thread (AuthorID,Thr_mes,title) VALUES (%s,%s,%s)"
        cursor.execute(sql, [1, request.POST['content'],request.POST['title']])
        sql = "INSERT INTO forum (ForumID,CourID) VALUES (%s,%s)"
        cursor.execute(sql,[request.POST['id'],request.POST['id']])

        print(request.POST)
        new_url = '/forum/forum/?id={}'.format(request.POST.get('id'))
        print(new_url)
        return redirect(new_url)

    course_id = request.GET.get('id')
    sql = 'SELECT ThreadID FROM forum where CourID=%s'

    cursor.execute(sql,[course_id])
    thread_f = cursor.fetchall()
    thread_f_main=[]
    for main in thread_f:
        sql = 'SELECT * FROM thread where ThreadID=%s'

        cursor.execute(sql, [main[0]])
        thread_one=list(cursor.fetchone())
        print(thread_one)
        sql = 'SELECT * FROM comment where ThreadID=%s'
        cursor.execute(sql, [thread_one[0]])
        thread_one.append(cursor.fetchall())
        thread_f_main.append(thread_one)
        # thread_f_main.append(list(cursor.fetchone()))

        # sql = 'SELECT * FROM forum where ForumID=%s'
        # cursor.execute(sql,[main[0]])
        # threads=cursor.fetchall()
    # for p in thread_f_main:
    #     sql = 'SELECT ThreadID FROM forum where ForumID=%s'
    #     cursor.execute(sql, p)
    #     for q in cursor.fetchall():
    #         sql = 'SELECT ThreadID FROM thread where ForumID=%s'
    print(thread_f_main)
    page = request.GET.get('page', 1)
    page_size = 4
    paginator = Paginator(thread_f_main, page_size)
    thread_f_main = paginator.page(page)
    strat = (int(page)-1) *4
    # sql = "INSERT INTO forum (ForumID,CourID,ThreadID) VALUES (1,2,3)"
    # cursor.execute(sql)
    # print("ok")


    return render(request, 'forum.html', {
        'thread_main':thread_f_main,
        'id':course_id,
        'strat':strat,
    })

#dashboard view
@login_required
def myaccount(request):
    context = {}
    cursor = connection.cursor()
    if request.method == 'POST':
        sql = 'SELECT * FROM user_info where UserID=1'
        cursor.execute(sql)
        user_info = cursor.fetchone()
        if user_info:
            sql = 'UPDATE user_info SET intro=%s,FirstName=%s,LastName=%s WHERE UserID = 1 '
            cursor.execute(sql,[request.POST.get('intro'),request.POST.get('f_name'),request.POST.get('l_name')])
            return redirect('forum_d')
        else:
            sql = "INSERT INTO user_info (intro,FirstName,LastName,UserID) VALUES (%s,%s,%s,%s)"
            cursor.execute(sql, [request.POST.get('intro'),request.POST.get('f_name'),request.POST.get('l_name'),1])
            return redirect('forum_d')
    sql = 'SELECT * FROM user_info where UserID=1'
    cursor.execute(sql)
    user_info =cursor.fetchone()
    print(user_info)
    # sql = 'SELECT * FROM student where StuID=1'
    # cursor.execute(sql)
    # stu_cour = cursor.fetchall()
    # print(stu_cour)
    # course=[]
    # for s_c in stu_cour:
    #     sql = 'SELECT * FROM course where CourID=%s'
    #     print(s_c)
    #     cursor.execute(sql,[s_c[1]])
    #     course.append(cursor.fetchone())
    #     print(course)

    sql = 'SELECT * FROM simplify_main_app_course'

    cursor.execute(sql)
    course = cursor.fetchall()
    print(course)
    return render(request, 'dashboard.html', {
        'user_info':user_info,
        'course':course,

    })
    # user_info={}
    # course={}
    # return render(request,'dashboard.html',{
    #     'user_info':user_info,
    #      'course':course,})


def creat_comment(request):
    cursor = connection.cursor()
    sql = "INSERT INTO comment (AuthorID,Comment,ThreadID) VALUES (%s,%s,%s)"
    cursor.execute(sql, [1, request.POST['comment'],request.POST['thread_id']])
    new_url = '/forum/forum/?id={}'.format(request.POST.get('id'))
    print(new_url)
    return redirect(new_url)