# coding:utf-8
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.six import python_2_unicode_compatible

import markdown


# Create your models here
# 类名 对应 表名
@python_2_unicode_compatible
class Category(models.Model):
    """
    分类
    """
    # 属性名 对应列名 ；name的类型是插入
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Tag(models.Model):
    """
    标签
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Post(models.Model):
    """
    博客内容
    """
    # 文章标题 短字符型
    title = models.CharField(max_length=70)
    # 文章内容
    body = models.TextField()
    # 文章创建时间
    created_time = models.DateTimeField()
    # 文章修改时间
    modified_time = models.DateTimeField(auto_now_add=True)
    # 文章摘要 可以为空;
    # blank=True 和 null=True 后者是数据库可以为空
    # 前者是CharField可以为空，传到数据库是空字符串
    excerpt = models.CharField(max_length=200, null=True, blank=True)
    # 分类 如果外键对应的category 被删除，则置空
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL)
    # 标签
    tag = models.ForeignKey(
        Tag, null=True, blank=True, on_delete=models.SET_NULL)
    # 作者
    author = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL)
    # 浏览量 PisitiveIntegerField 只允许是正整数，0
    views = models.PositiveIntegerField(default=0)

    def increase_views(self):
        """
        阅读量自增函数
        """
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title

    # 自定义 get_absolute_url 方法
    # 记得从 django.urls 中导入 reverse 函数
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    # 自动生成摘要
    def save(self, *args, **kwargs):
        # 如果没有填写摘要
        if not self.excerpt:
            # 首先实例化一个 Markdown 类，用于渲染 body 的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        # 调用父类的 save 方法将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)

    class Meta:
        # 负号表示逆序排列
        ordering = ['-created_time', 'title']
