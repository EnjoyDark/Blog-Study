from django.contrib import admin
from .models import Category, Tag, Post


class PostAdmin(admin.ModelAdmin):
    # 文章列表页显示具体信息
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']

    # 添加文章显示字段
    fields = ['title', 'body', 'created_time', 'modified_time', 'excerpt', 'category', 'tags']

    # 自动设置文章作者为当前登录人
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
