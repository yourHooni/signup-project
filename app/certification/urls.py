from django.urls import path
from .views import PhoneCertificationViewSet, CheckCertificationCodeViewSet


urlpatterns = [
    path('phone-certification', PhoneCertificationViewSet.as_view(),
         name='phone-certification'),
    path('check-certification', CheckCertificationCodeViewSet.as_view({'patch': 'partial_update'}),
         name='check-certification')
]
