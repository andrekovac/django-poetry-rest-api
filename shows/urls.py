from django.urls import path
from .views import ShowListView, ShowDetailView

urlpatterns = [
    path('', ShowListView.as_view()),
    # with `<str:pk>` we store whatever is part of the url at that position in a variable called 'pk'
    path('<str:pk>/', ShowDetailView.as_view())
]
