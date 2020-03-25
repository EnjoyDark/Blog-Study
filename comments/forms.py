from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']

# 那么怎么展现一个表单呢？django 会根据表单类的定义自动生成表单的 HTML 代码，
# 我们要做的就是实例化这个表单类，然后将表单的实例传给模板，让 django 的模板引擎来渲染这个表单。
# 一种是修改detail视图函数，实例化表单再传递给模板，不方便。所以选择自定义模板标签
