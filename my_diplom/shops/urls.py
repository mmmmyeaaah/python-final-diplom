from django.urls import path

from shops.views import ShopView, CategoryView, ProductInfoView, PartnerUpdate, PartnerState
from rest_framework.routers import DefaultRouter
from django.urls import include

app_name = 'shops'

router = DefaultRouter()
router.register(r'shop', ShopView, basename='shop')
router.register(r'category', CategoryView, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('products', ProductInfoView.as_view(), name='products'),
    path('partner/update', PartnerUpdate.as_view(), name='partner-update'),
    path('partner/state', PartnerState.as_view(), name='partner-state'),
]
