# /backend/app/celery_config.py
from celery.schedules import crontab

broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Asia/Kolkata'
enable_utc = True

beat_schedule = {
    'send-daily-reminders': {
        'task': 'app.tasks.send_daily_reminders',
        'schedule': crontab(hour=15, minute=40),
    },
    'send-monthly-report': {
        'task': 'app.tasks.send_monthly_report',
        'schedule': crontab(day_of_month=7, hour=15, minute=40),
    },
}
