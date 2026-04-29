from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/',views.login_page,name='login'),
    path('logout/',views.logout_page,name='logout'),
    path('register/',views.register_page,name='register'),
    path('add_cart/<uuid:pizza_uid>/',views.add_cart,name='add_cart'),
    path('my_cart /',views.my_cart,name='my_carts'),
    path('remove_cart_item/<uuid:item_uid>/',views.remove_cart_item,name='remove_cart_item')

]