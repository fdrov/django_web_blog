from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.utils.html import format_html

from .models import *


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'category', 'created_at', 'get_photo']
    prepopulated_fields = {'slug': ('title',)}
    form = PostAdminForm
    save_as = True
    save_on_top = True
    readonly_fields = ['views', 'created_at', 'get_photo']
    list_display_links = ['id', 'title']
    search_fields = ['title']
    list_filter = ['category', 'tags']
    fields = ['title', 'slug', 'category', 'tags', 'content', 'photo','get_photo', 'views', 'created_at', ]

    def get_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50">', obj.photo.url)
        else:
            return '-'

    get_photo.short_description = 'Фото'
# Register your models here.
