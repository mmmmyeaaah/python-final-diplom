from django.urls import path

from shops.views import ShopView, CategoryView, ProductInfoView, PartnerUpdate, PartnerState

app_name = 'shops'

urlpatterns = [
    path('shops', ShopView.as_view(), name='shops'),
    path('category', CategoryView.as_view(), name='category'),
    path('products', ProductInfoView.as_view(), name='products'),
    path('partner/update', PartnerUpdate.as_view(), name='partner-update'),
    path('partner/state', PartnerState.as_view(), name='partner-state'),
]
