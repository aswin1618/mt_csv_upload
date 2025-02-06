from django.urls import path
from .views import CsvUploadView

urlpatterns = [
    path('test/', CsvUploadView.as_view(),name='testview')
]
