from django.contrib import admin
from blog.models import Comment
from .models import Blog
from django_summernote.admin import SummernoteModelAdmin

admin.site.register(Comment)

class CommentInline(admin.TabularInline):
    model = Comment
    fields = ['content', 'author']

# @admin.register(Blog)
# class BlogAdmin(admin.ModelAdmin):
#     inlines = [
#         CommentInline
#     ]

@admin.register(Blog)
class BlogAdmin(SummernoteModelAdmin):
    summernote_fields = ['content',]
    inlines = [CommentInline]