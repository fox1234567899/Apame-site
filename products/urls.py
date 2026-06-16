from django.urls import path 
from . import views
urlpatterns = [

    path("items/",views.itemView,name='items'),
    path("detail/<slug:slug>",views.detail_item_view,name='detail'),
    path("add_item/",views.add_item,name='add_item'),
    path("item_in_cart/",views.item_in_cart,name='item_in_cart'),
    path("get_cart/",views.get_cart,name='get_cart'),
    path("get_cart_stat/",views.get_cart_stat,name='get_cart_stat'),
    path("delete_CartItem/",views.delete_CartItem,name='delete_CartItem'),
    path("update_quantity/",views.update_quantity,name='update_quantity'),
    path("get_username/",views.get_username,name='get_username'),
    path("user_information/",views.user_information,name='user_information'),
    path("search/",views.search,name='search'),
    path("registerPart/",views.registerPart,name='registerPart'),
    path("apame_payment/",views.apame_payment,name='apame_payment'),
    path("payment_callback/",views.payment_callback,name='payment_callback'),
    path("changeProfilePicture/",views.changeProfilePicture,name='changeProfilePicture'),


]
