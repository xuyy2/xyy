from django.db import models
from django.utils.six import python_2_unicode_compatible


# Create your models here.
@python_2_unicode_compatible
class Comment(models.Model):
    # 评论人的名字
    name = models.CharField(max_length=100)
    # 评论人的邮件
    email = models.EmailField(max_length=255)
    # 个人网站
    url = models.URLField(blank=True)
    # 评论内容
    text = models.TextField(default='')
    # 评论时间 自动生成当前时间
    created_time = models.DateTimeField(auto_now_add=True)
    # 评论文章 级联删除
    post = models.ForeignKey('blog.post', on_delete=models.CASCADE)
