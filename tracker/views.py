from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import date, timedelta
from .models import Habit, DailyTask
from .utils import generate_daily_tasks_for_user, generate_tasks_for_date_range


def home(request):
    """Homepage with login/register buttons"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'base.html')


def register_view(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'auth/login.html')


@login_required
def dashboard(request):
    """Main dashboard with daily tasks"""
    today = date.today()
    
    # Get tasks grouped by date (no automatic generation)
    tasks = DailyTask.objects.filter(user=request.user).order_by('-date', 'habit__time')
    
    # Group tasks by date
    tasks_by_date = {}
    for task in tasks:
        date_str = task.date.strftime('%Y-%m-%d')
        if date_str not in tasks_by_date:
            tasks_by_date[date_str] = []
        tasks_by_date[date_str].append(task)
    
    # Get today's tasks
    today_tasks = DailyTask.objects.filter(user=request.user, date=today).order_by('habit__time')
    
    context = {
        'today_tasks': today_tasks,
        'tasks_by_date': tasks_by_date,
        'today': today,
    }
    return render(request, 'dashboard/index.html', context)


@login_required
def habits_view(request):
    """View and manage habits"""
    habits = Habit.objects.filter(user=request.user).order_by('time', 'title')
    return render(request, 'dashboard/habits.html', {'habits': habits})


@login_required
def add_habit(request):
    """Add a new habit"""
    if request.method == 'POST':
        title = request.POST.get('title')
        time_str = request.POST.get('time', '07:00')
        
        try:
            from datetime import datetime
            time_obj = datetime.strptime(time_str, '%H:%M').time()
        except:
            from datetime import time
            time_obj = time(7, 0)
        
        if title:
            habit = Habit.objects.create(
                title=title,
                time=time_obj,
                user=request.user
            )
            messages.success(request, 'Habit added successfully!')
        else:
            messages.error(request, 'Title is required.')
    
    return redirect('habits')


@login_required
def edit_habit(request, habit_id):
    """Edit an existing habit"""
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        time_str = request.POST.get('time', '07:00')
        
        try:
            from datetime import datetime
            time_obj = datetime.strptime(time_str, '%H:%M').time()
        except:
            # If parsing fails, keep the existing time
            time_obj = habit.time
        
        if title:
            habit.title = title
            habit.time = time_obj
            habit.save()
            messages.success(request, 'Habit updated successfully!')
        else:
            messages.error(request, 'Title is required.')
    
    return redirect('habits')


@login_required
def delete_habit(request, habit_id):
    """Delete a habit"""
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    habit.delete()
    messages.success(request, 'Habit deleted successfully!')
    return redirect('habits')


@login_required
@require_POST
def toggle_task(request, task_id):
    """Toggle task completion status"""
    task = get_object_or_404(DailyTask, id=task_id, user=request.user)
    task.is_done = not task.is_done
    task.save()
    return JsonResponse({'is_done': task.is_done})


@login_required
def edit_task(request, task_id):
    """Edit a task - redirects to edit the underlying habit"""
    task = get_object_or_404(DailyTask, id=task_id, user=request.user)
    # Tasks are auto-generated from habits, so redirect to edit the habit
    messages.info(request, 'Tasks are generated from habits. Edit the habit to change task details.')
    return redirect('edit_habit', habit_id=task.habit.id)


@login_required
def delete_task(request, task_id):
    """Delete a task"""
    task = get_object_or_404(DailyTask, id=task_id, user=request.user)
    task.delete()
    messages.success(request, 'Task deleted successfully!')
    return redirect('dashboard')


@login_required
def generate_tasks(request):
    """Manually generate tasks for a specific date"""
    if request.method == 'POST':
        date_str = request.POST.get('date')
        if date_str:
            try:
                target_date = date.fromisoformat(date_str)
                generate_daily_tasks_for_user(request.user, target_date)
                messages.success(request, f'Tasks generated successfully for {target_date.strftime("%B %d, %Y")}!')
            except ValueError:
                messages.error(request, 'Invalid date format. Please use YYYY-MM-DD.')
        else:
            messages.error(request, 'Please select a date.')
    
    return redirect('dashboard')


@login_required
def stats_view(request):
    """Performance/Statistics page"""
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    
    # Today's stats
    today_tasks = DailyTask.objects.filter(user=request.user, date=today)
    today_total = today_tasks.count()
    today_completed = today_tasks.filter(is_done=True).count()
    today_percentage = (today_completed / today_total * 100) if today_total > 0 else 0
    
    # Week's stats
    week_tasks = DailyTask.objects.filter(
        user=request.user,
        date__gte=week_start,
        date__lte=today
    )
    week_total = week_tasks.count()
    week_completed = week_tasks.filter(is_done=True).count()
    week_percentage = (week_completed / week_total * 100) if week_total > 0 else 0
    
    # Month's stats
    month_tasks = DailyTask.objects.filter(
        user=request.user,
        date__gte=month_start,
        date__lte=today
    )
    month_total = month_tasks.count()
    month_completed = month_tasks.filter(is_done=True).count()
    month_percentage = (month_completed / month_total * 100) if month_total > 0 else 0
    
    # Weekly progress (last 7 days)
    weekly_progress = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_tasks = DailyTask.objects.filter(user=request.user, date=day)
        day_total = day_tasks.count()
        day_completed = day_tasks.filter(is_done=True).count()
        day_percentage = (day_completed / day_total * 100) if day_total > 0 else 0
        weekly_progress.append({
            'date': day,
            'total': day_total,
            'completed': day_completed,
            'percentage': day_percentage
        })
    
    context = {
        'today_total': today_total,
        'today_completed': today_completed,
        'today_percentage': round(today_percentage, 1),
        'week_total': week_total,
        'week_completed': week_completed,
        'week_percentage': round(week_percentage, 1),
        'month_total': month_total,
        'month_completed': month_completed,
        'month_percentage': round(month_percentage, 1),
        'weekly_progress': weekly_progress,
    }
    return render(request, 'dashboard/stats.html', context)
