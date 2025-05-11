# /backend/trigger_tasks.py
from app import create_app
from app.celery import send_daily_reminders, send_monthly_report, export_campaigns_to_csv

app = create_app()

with app.app_context():
    print("Triggering send_daily_reminders task...")
    send_daily_reminders.apply_async()
    
    print("Triggering send_monthly_report task...")
    send_monthly_report.apply_async()
    
    # Replace `sponsor_id` with an actual sponsor ID from your database
    sponsor_ids = [3]
    for i in sponsor_ids:
        print("Triggering export_campaigns_to_csv task for sponsor_id:", i)
        export_campaigns_to_csv.apply_async(args=[i])
    
    print("Tasks have been triggered.")
