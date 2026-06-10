from django.urls import path
from .views import HabitListCreateView,HabitDetailView,CompleteHabitView

urlpatterns=[
    path('habits/',HabitListCreateView.as_view()),
    path('habits/<int:pk>/',HabitDetailView.as_view()),
    path('habits/<int:pk>/complete/',CompleteHabitView.as_view()),
    
]