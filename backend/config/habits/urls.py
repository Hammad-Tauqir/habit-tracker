from django.urls import path
from .views import HabitListCreateView,HabitDetailView,CompleteHabitView,DashBoardView,WeeklyProgressView

urlpatterns=[
    path('habits/',HabitListCreateView.as_view()),
    path('habits/<int:pk>/',HabitDetailView.as_view()),
    path('habits/<int:pk>/complete/',CompleteHabitView.as_view()),
    path('habits/dashboard/', DashBoardView.as_view()),
    path('habits/weekly-progress/<int:pk>/', WeeklyProgressView.as_view()),
]
    
