from django.db import models
from django.contrib.auth.models import AbstractUser

class UserInfo(AbstractUser):   #用户信息。继承了原有的user表，因为自己加入了一些字段，并且用到原有的认证功能
    nid = models.AutoField(primary_key=True)
    nickname = models.CharField(verbose_name='昵称', max_length=32)
    telephone = models.CharField(max_length=11, null=True, unique=True)
    avatar = models.FileField(upload_to = 'avatars/',default="/avatars/default.png")    #头像
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    blog = models.OneToOneField(to='Blog', to_field='nid',null=True)    #一个用户只有一个博客
    def __str__(self):
        return self.username

class Blog(models.Model):   #博客信息
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题', max_length=64)
    site = models.CharField(verbose_name='个人博客后缀', max_length=32, unique=True)
    theme = models.CharField(verbose_name='博客主题', max_length=32)
    def __str__(self):
        return self.title

class Category(models.Model):   #博主个人文章分类表
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')    #一个博客有很多分类
    def __str__(self):
        return self.title

class Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')    ##一个博客有很多标签
    def __str__(self):
        return self.title

class Article(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=255, verbose_name='文章描述')
    comment_count= models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)   #推荐
    down_count = models.IntegerField(default=0)     #反对
    create_time = models.DateTimeField(verbose_name='创建时间')
    homeCategory = models.ForeignKey(to='Category', to_field='nid', null=True)      #一个分类下面有多个文章
    #siteDetaiCategory = models.ForeignKey(to='SiteCategory', to_field='nid', null=True)
    user = models.ForeignKey(verbose_name='作者', to='UserInfo', to_field='nid')      #一个作者可以写多篇文章
    tags = models.ManyToManyField(      #标签和文章是多对多关系，下面这种格式为不让Django创建第三张表
        to="Tag",
        through='Article2Tag',
        through_fields=('article', 'tag'),
    )
    def __str__(self):
        return self.title

class ArticleDetail(models.Model):  #文章详细表，把文章内容单列出来
    nid = models.AutoField(primary_key=True)
    content = models.TextField()
    article = models.OneToOneField(to='Article', to_field='nid')

class Comment(models.Model):    #评论表
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='评论文章', to='Article', to_field='nid')      #一篇文章有多条评论
    user = models.ForeignKey(verbose_name='评论者', to='UserInfo', to_field='nid')     #一篇文章有多个人评论
    content = models.CharField(verbose_name='评论内容', max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True)       #用于区分是文章的评论还是评论的评论，self表示关联自己表中的主键
    def __str__(self):
        return self.content

class ArticleUpDown(models.Model):      #点赞表
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserInfo', null=True)     #一个用户可以为多篇文章点赞
    article = models.ForeignKey("Article", null=True)   #一篇文章可以有多个赞
    is_up=models.BooleanField(default=True)     #用于判断是否点赞
    class Meta:
        unique_together = [     #联合唯一
            ('article', 'user'),
        ]

class Article2Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='文章', to="Article", to_field='nid')
    tag = models.ForeignKey(verbose_name='标签', to="Tag", to_field='nid')
    class Meta:
        unique_together = [
            ('article', 'tag'),
        ]
    def __str__(self):
        v=self.article.title+"----"+self.tag.title
        return v

