# coding=utf-8
from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    """
    评论表单
    """
    class Meta:
        # 表单对应的数据库模型
        model = Comment
        # 表单要显示字段
        fields = ['name', 'email', 'url', 'text']
