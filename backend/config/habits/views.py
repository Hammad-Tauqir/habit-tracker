from django.shortcuts import render
from rest_framework import generics,permissions,status
from .models import Habit,HabitCompletion
from .serializers import HabitSerializer,HabitCompletionSerializer
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import timedelta



class HabitListCreateView(generics.ListCreateAPIView):
    serializer_class=HabitSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)
    
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)



class HabitDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=HabitSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)
    


class CompleteHabitView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def post(self,request,pk):
        try:
            habit=Habit.objects.get(
                id=pk,
                user=request.user
            )
        except Habit.DoesNotExist:
            return Response(
                {"error":"Habit not found"},
                status=status.HTTP_404_NOT_FOUND
            )    
        today=now().date()

        if HabitCompletion.objects.filter(
            habit=habit,
            completed_at=today
        ).exists():
            
            return Response(
                {"message": "Habit already completed today"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        HabitCompletion.objects.create(
            habit=habit,
            completed_at=today
        )


        yesterday=today-timedelta(days=1)

        completed_yesterday=HabitCompletion.objects.filter(
            habit=habit,
            completed_at=yesterday

        ).exists()

        if completed_yesterday:
            habit.current_streak+=1
        else:
            habit.current_streak=1

        if habit.current_streak > habit.longest_streak:
            habit.longest_streak=habit.current_streak

        habit.save()

        return Response({
            "message":"Habit completed successfully",
            "current_streak": habit.current_streak,
            "longest_streak":habit.longest_streak
        })            
    
class DashBoardView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):
        user=request.user
        today=now().date()

        total_habits=Habit.objects.filter(user=user).count()

        completed_today=HabitCompletion.objects.filter(
            habit_user=user,
            completed_today=today

        ).count()

        active_streaks=Habit.objects.filter(
            user=user,
            current_streak__gt=0
        ).count()

        longest_streak = Habit.objects.filter(
            user=user
        ).order_by('-longest_streak').first()

        return Response({
            "total_habits": total_habits,
            "completed_today": completed_today,
            "active_streaks": active_streaks,
            "longest_streak": longest_streak.longest_streak if longest_streak else 0
        })
    

class WeeklyProgressView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request,pk):
        user=request.user

        try:
            habit=Habit.objects.get(id=pk,user=user)
        except Habit.DoesNotExist:
            return Response({"error":"Habit Not Found"}, status=404)

        today=now().date()

        start_of_week=today-timedelta(days=today.weekday())

        week_date=[]

        for i in range(7):
            day=start_of_week+timedelta(days=i)
            completed=HabitCompletion.objects.filter(
                habit=habit,
                completed_at=day

            ).exists()
            
            week_date.append({
                "day":day,
                "completed":completed
            })
        return Response({
            "habit":habit.name,
            "week":week_date
        })