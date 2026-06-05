from django.urls import path
from .views import HabitListCreateView,HabitDetailView

urlpatterns=[
    path('',HabitListCreateView.as_view()),
    path('<int:pk>/',HabitDetailView.as_view()),
    
]