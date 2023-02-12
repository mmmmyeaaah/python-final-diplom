from django.urls import path

from .views import ShopView, CategoryView, RegisterAccount, ConfirmAccount, LoginAccount, AccountDetails, PartnerUpdate, \
    ContactView, ProductInfoView, PartnerState

app_name = 'app'

urlpatterns = [
    path('shops', ShopView.as_view(), name='shops'),
    path('category', CategoryView.as_view(), name='category'),
    path('products', ProductInfoView.as_view(), name='products'),
    path('user/register', RegisterAccount.as_view(), name='user-register'),
    path('user/register/confirm', ConfirmAccount.as_view(), name='user-register-confirm'),
    path('user/login', LoginAccount.as_view(), name='user-login'),
    path('user/details', AccountDetails.as_view(), name='user-details'),
    path('user/contact', ContactView.as_view(), name='user-contact'),
    path('partner/update', PartnerUpdate.as_view(), name='partner-update'),
    path('partner/state', PartnerState.as_view(), name='partner-state'),
]
