from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, time


class Habit(models.Model):
    title = models.CharField(max_length=200)
    time = models.TimeField(default=time(7, 0))  # Default 07:00
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    class Meta:
        ordering = ['time', 'title']


class DailyTask(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='daily_tasks')
    date = models.DateField(default=date.today)
    is_done = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_tasks')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.habit.title} - {self.date}"

    class Meta:
        unique_together = ['habit', 'date']
        ordering = ['date', 'habit__time']
