from django.urls import path
from .views import SignUpView, LoginView, AccountView, RetrieveMobileCarrierView


urlpatterns = [
    path('signup', SignUpView.as_view(), name='sigunup'),
    path('login', LoginView.as_view(), name='login'),
    path('account', AccountView.as_view(), name='account'),
    path('mobile-carrier', RetrieveMobileCarrierView.as_view({'get': 'list'}), name='mobile-carrier_list'),
]
