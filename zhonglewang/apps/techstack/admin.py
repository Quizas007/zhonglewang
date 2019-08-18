from django.contrib import admin
from .models import Category,Tag,Articles


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Articles)