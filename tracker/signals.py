from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Habit
from datetime import time


@receiver(post_save, sender=User)
def create_default_habits(sender, instance, created, **kwargs):
    """Create default habits for new users"""
    if created:
        default_habits = [
            {'title': 'Wake up at a specific morning time', 'time': time(7, 0)},
            {'title': 'Running / Exercise', 'time': time(8, 0)},
            {'title': 'Reading a book', 'time': time(19, 0)},
            {'title': 'Working / Studying', 'time': time(9, 0)},
        ]
        
        for habit_data in default_habits:
            Habit.objects.create(
                title=habit_data['title'],
                time=habit_data['time'],
                user=instance
            )

