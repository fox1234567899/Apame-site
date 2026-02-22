from django.contrib import admin
from .models import CustomInformationUser
# Register your models here.
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    add_fieldsets =(
        (None,{
            'classes':('wide',),

            'fields':('username', 'email','password1','password2','avatar','first_name','last_name','is_staff','is_active','phone','address', 'city')
        }
        ),
    )
    fieldsets = (
        (None,{
            'classes':('wide',),

            'fields':('username', 'email','password','avatar','first_name','last_name','is_staff','is_active','phone','address', 'city')
            }
        ),
    )


admin.site.register(CustomInformationUser,CustomUserAdmin)
