from django.contrib import admin
from socialnetwork import models


class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'likes')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'surname', 'email', 'country', 'city')


admin.site.register(models.UserProfile, ProfileAdmin)
admin.site.register(models.Post, PostAdmin)
