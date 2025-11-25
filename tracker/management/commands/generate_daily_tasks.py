"""
Django management command to generate daily tasks for all users.
This should be run daily (e.g., via cron job) to automatically generate tasks.

Usage:
    python manage.py generate_daily_tasks
    python manage.py generate_daily_tasks --date 2024-01-15  # For a specific date
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from datetime import date, timedelta
from tracker.utils import generate_daily_tasks_for_user


class Command(BaseCommand):
    help = 'Generate daily tasks for all users based on their habits'

    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            type=str,
            help='Date to generate tasks for (YYYY-MM-DD). Defaults to today.',
        )
        parser.add_argument(
            '--days-back',
            type=int,
            default=0,
            help='Also generate tasks for the last N days if missing',
        )

    def handle(self, *args, **options):
        target_date_str = options.get('date')
        days_back = options.get('days_back', 0)
        
        if target_date_str:
            try:
                target_date = date.fromisoformat(target_date_str)
            except ValueError:
                self.stdout.write(
                    self.style.ERROR(f'Invalid date format: {target_date_str}. Use YYYY-MM-DD')
                )
                return
        else:
            target_date = date.today()
        
        users = User.objects.all()
        total_tasks = 0
        
        for user in users:
            # Generate tasks for the target date
            generate_daily_tasks_for_user(user, target_date)
            habits_count = user.habits.count()
            total_tasks += habits_count
            
            # If days_back is specified, also generate for past days
            if days_back > 0:
                for i in range(1, days_back + 1):
                    past_date = target_date - timedelta(days=i)
                    generate_daily_tasks_for_user(user, past_date)
                    total_tasks += habits_count
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully generated tasks for {users.count()} users '
                f'({total_tasks} total tasks) for date {target_date}'
            )
        )

