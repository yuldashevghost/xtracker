from datetime import date, timedelta
from .models import Habit, DailyTask


def generate_daily_tasks_for_user(user, target_date=None):
    """Generate daily tasks for a user based on their habits"""
    if target_date is None:
        target_date = date.today()
    
    habits = Habit.objects.filter(user=user)
    
    for habit in habits:
        DailyTask.objects.get_or_create(
            habit=habit,
            date=target_date,
            user=user,
            defaults={'is_done': False}
        )


def generate_tasks_for_date_range(user, start_date, end_date):
    """Generate tasks for a range of dates"""
    current_date = start_date
    while current_date <= end_date:
        generate_daily_tasks_for_user(user, current_date)
        current_date += timedelta(days=1)

