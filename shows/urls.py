from django.urls import path
from .views import ShowListView

urlpatterns = [
    path('', ShowListView.as_view()),
]
