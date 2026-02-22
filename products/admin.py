from django.contrib import admin
from .models import Item,Cart,CartItem,Order,OrderItem
# Register your models here.
admin.site.register([Item,CartItem,Cart,Order,OrderItem])