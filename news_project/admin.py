from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in Post._meta.get_fields()]
    list_display = ('postType', 'postAuthor', 'autoDate', 'title',)
    list_filter = ('postType', 'postAuthor', 'autoDate', 'title',)
    search_fields = ('title', 'postType', 'autoDate', 'PostCategory')

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)



# Register your models here.
