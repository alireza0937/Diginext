from django.urls import path
from . import views

urlpatterns = [
    path('location/', views.LocationAPIView.as_view(), name='location-api'),
    path('acceleration/', views.AccelerationStandardAPIView.as_view(), name='acceleration-api'),
    path('velocity/', views.VelocityStandardAPIView.as_view(), name='velocity-api'),
    path('isintehran/', views.IsInTehranAPIView.as_view(), name='isintehran-api'),
]
