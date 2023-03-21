from django.db import models

# Create your models here.
class comment(models.Model):
    CommentID = models.AutoField('c_id',max_length=127,primary_key=True)

    AuthorID = models.CharField('a_id', max_length=127,null=True)

    Comment = models.TextField('comment', max_length=512,null=True)

    ThreadID = models.IntegerField('id', max_length=20,null=True)


    # 改变表名
    class Meta:
        db_table = 'comment'

class forum(models.Model):

    ForumID = models.IntegerField('F_id', max_length=127, null=True)

    CourID = models.IntegerField('C_id', max_length=512, null=True)

    ThreadID = models.AutoField('t_id', max_length=127,primary_key=True)


    # 改变表名
    class Meta:
        db_table = 'forum'

class thread(models.Model):
    ThreadID = models.AutoField('t_id', max_length=127, primary_key=True)

    AuthorID = models.IntegerField('A_id', max_length=127,null=True)

    Thr_mes = models.TextField('t_m', max_length=512,null=True)

    title = models.TextField('title', max_length=512, null=True)




    # 改变表名
    class Meta:
        db_table = 'thread'

class user_info(models.Model):
    UserID = models.IntegerField('t_id', max_length=127,null=True)

    UserName = models.CharField('u_id', max_length=127,null=True)

    type = models.TextField('type', max_length=512, null=True)

    FirstName = models.CharField('f_name', max_length=127, null=True)

    LastName = models.CharField('L_name', max_length=127, null=True)

    intro = models.TextField('intro', max_length=512, null=True)



    # 改变表名
    class Meta:
        db_table = 'user_info'

