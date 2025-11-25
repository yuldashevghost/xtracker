from django.contrib import admin
from .models import Habit, DailyTask


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'time', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('title', 'user__username')


@admin.register(DailyTask)
class DailyTaskAdmin(admin.ModelAdmin):
    list_display = ('habit', 'user', 'date', 'is_done', 'created_at')
    list_filter = ('is_done', 'date', 'user')
    search_fields = ('habit__title', 'user__username')
    date_hierarchy = 'date'
