from django.urls import path

from .views import ShopView, CategoryView, RegisterAccount

app_name = 'app'

urlpatterns = [
    path('shops', ShopView.as_view(), name='shops'),
    path('category', CategoryView.as_view(), name='category'),
    path('user/register', RegisterAccount.as_view(), name='user-register'),
]