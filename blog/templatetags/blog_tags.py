from django import template
from django.db.models.aggregates import Count

from ..models import Category, Post, Tag

register = template.Library()


@register.simple_tag
def get_recent_posts(num=5):
    """
    最新文章模板标签
    """
    return Post.objects.all().order_by('-created_time')[:num]


@register.simple_tag
def archives():
    """
    归档模板标签
    """
    return Post.objects.dates('created_time', 'month', order='DESC')


@register.simple_tag
def get_categories():
    """
    分类模板标签
    """
    # 别忘了在顶部引入 Category 类
    # return Category.objects.all()

    # 记得在顶部引入 count 函数
    # Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称
    return Category.objects.annotate(num_posts=Count('post')).filter(
        num_posts__gt=0)


@register.simple_tag
def get_tags():
    """
    标签云模板标签
    """
    # 别忘了在顶部引入 Category 类
    # return Tag.objects.all()
    return Tag.objects.annotate(num_posts=Count('post')).filter(
        num_posts__gt=0)
