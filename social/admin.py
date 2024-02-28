from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Post, Comment

# Unregister Groups
admin.site.unregister(Group)

# Mix profile info into User info
class ProfileInline(admin.StackedInline):
    model = Profile

# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    # Just display username fields on admin page
    fields = ["username"]
    inlines = [ProfileInline]

# Unregister User
admin.site.unregister(User)

#  Register new User Admin with customized fields
admin.site.register(User, UserAdmin)
# admin.site.register(Profile)

admin.site.register(Post)
admin.site.register(Comment)