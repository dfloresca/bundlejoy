from django.contrib import admin
from django.contrib.auth.models import Group, User

# Unregister Groups
admin.site.unregister(Group)

# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    # Just display username fields on admin page
    fields = ["username"]

# Unregister User
admin.site.unregister(User)

#  Register new User Admin with customized fields
admin.site.register(User, UserAdmin)
