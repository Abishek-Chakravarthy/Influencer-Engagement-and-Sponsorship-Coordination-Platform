from app import create_app
from app.celery import celery

app = create_app()
app.app_context().push()

# Import the tasks to ensure they are registered with Celery
from app.celery import send_daily_reminders, send_monthly_report, export_campaigns_to_csv

if __name__ == '__main__':
    celery.start()