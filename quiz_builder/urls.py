# urls.py
from django.urls import path
from .views import TestCreateView, TestPreviewView, HomeView, TestCheckView, TestResultsView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # URL dla strony głównej
    path('test/create/', TestCreateView.as_view(), name='create_test'),
    path('test/preview/', TestPreviewView.as_view(), name='preview_test'),
    path('test/check/', TestCheckView.as_view(), name='check_test'),
    path('test/results/', TestResultsView.as_view(), name='test_results'),
]
