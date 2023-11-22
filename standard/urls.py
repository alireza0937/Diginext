from django.urls import path
from standard.views.LocationView import LocationAPIView
from standard.views.StandardsView import StandardsAPIView

urlpatterns = [
    path('location/', LocationAPIView.as_view(), name='location-api'),
    path('standards/', StandardsAPIView.as_view(), name='Standards-api'),
]
