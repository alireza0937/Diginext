from django.urls import path
from report.views.reporting_view import ReportingAPIView

urlpatterns = [
    path('', ReportingAPIView.as_view(), name='driver-report-api'),
]
