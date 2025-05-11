# /backend/app/tasks.py
from app import celery
from flask_mail import Mail, Message

from datetime import datetime
import csv
from flask import current_app

mail = Mail(current_app)

@celery.task(name="app.tasks.send_daily_reminders")
def send_daily_reminders():
    with current_app as current_app:
        from .models import User, Campaign, AdRequest
        influencers = User.query.filter_by(role='influencer').all()
        for influencer in influencers:
            pending_requests = AdRequest.query.filter_by(influencer_id=influencer.id, status='pending').all()
            for request in pending_requests:
                campaign = Campaign.query.get(request.campaign_id)
                sponsor = User.query.get(campaign.sponsor_id)
                msg = Message(
                    'Daily Reminder: Pending Ad Request',
                    sender=current_app.config['MAIL_USERNAME'],
                    recipients=[influencer.email]
                )
                msg.body = f"""
                You have received an Ad Request called {request.ad_name} from the company {sponsor.company_name} for the campaign {campaign.name}. The payment amount offered is {request.payment_amount}.

                Login to your Account in the Influencer Engagement & Sponsorship Coordination Platform to view the full details.
                """
                mail.send(msg)

@celery.task(name="app.tasks.send_monthly_report")
def send_monthly_report():
    with current_app as current_app:
        from .models import User, Campaign, AdRequest
        sponsors = User.query.filter_by(role='sponsor').all()
        for sponsor in sponsors:
            campaigns = Campaign.query.filter_by(sponsor_id=sponsor.id).all()
            report = f"Monthly Report for {sponsor.company_name} from the Influencer Engagement & Sponsorship Coordination Platform\n\n"
            for campaign in campaigns:
                report += f"Campaign name: {campaign.name}\n"
                if campaign.description:
                    report += f"Campaign desc: {campaign.description}\n"
                report += f"Start date: {campaign.start_date}\n"
                report += f"End date: {campaign.end_date}\n"
                report += f"Budget: {campaign.budget}\n"
                report += f"Amount Spent: {campaign.amount_spent}\n"
                report += f"Visibility: {campaign.visibility}\n"
                
                accepted_influencers = AdRequest.query.filter_by(campaign_id=campaign.id, status='accepted').all()
                if accepted_influencers:
                    report += "Influencers currently part of campaign: "
                    report += ", ".join([User.query.get(req.influencer_id).username for req in accepted_influencers])
                    report += "\n"
                else:
                    report += "Influencers currently part of campaign: None\n"

                pending_by_sponsor = AdRequest.query.filter_by(campaign_id=campaign.id, status='pending', req_by='sponsor').all()
                if pending_by_sponsor:
                    report += "Influencers requested to be part of campaign: "
                    report += ", ".join([User.query.get(req.influencer_id).username for req in pending_by_sponsor])
                    report += "\n"
                else:
                    report += "Influencers requested to be part of campaign: None\n"

                pending_by_influencer = AdRequest.query.filter_by(campaign_id=campaign.id, status='pending', req_by='influencer').all()
                if pending_by_influencer:
                    report += "Influencers who have requested to be part of campaign: "
                    report += ", ".join([User.query.get(req.influencer_id).username for req in pending_by_influencer])
                    report += "\n"
                else:
                    report += "Influencers who have requested to be part of campaign: None\n"

                report += "\n"

            msg = Message(
                'Monthly Activity Report',
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[sponsor.email]
            )
            msg.body = report
            mail.send(msg)

@celery.task(name="app.tasks.export_campaigns_to_csv")
def export_campaigns_to_csv(sponsor_id):
    with current_app as current_app:
        from .models import User, Campaign, AdRequest
        sponsor = User.query.get(sponsor_id)
        campaigns = Campaign.query.filter_by(sponsor_id=sponsor.id).all()
        filename = f"{sponsor.company_name}_campaigns_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        with open(filename, 'w') as csvfile:
            fieldnames = ['name', 'description', 'start_date', 'end_date', 'budget', 'visibility', 'goals', 'accepted_influencers', 'requested_influencers', 'pending_influencers']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for campaign in campaigns:
                accepted_influencers = AdRequest.query.filter_by(campaign_id=campaign.id, status='accepted').all()
                accepted_influencers_names = ", ".join([User.query.get(req.influencer_id).username for req in accepted_influencers])

                pending_by_sponsor = AdRequest.query.filter_by(campaign_id=campaign.id, status='pending', req_by='sponsor').all()
                requested_influencers_names = ", ".join([User.query.get(req.influencer_id).username for req in pending_by_sponsor])

                pending_by_influencer = AdRequest.query.filter_by(campaign_id=campaign.id, status='pending', req_by='influencer').all()
                pending_influencers_names = ", ".join([User.query.get(req.influencer_id).username for req in pending_by_influencer])

                writer.writerow({
                    'name': campaign.name,
                    'description': campaign.description,
                    'start_date': campaign.start_date,
                    'end_date': campaign.end_date,
                    'budget': campaign.budget,
                    'visibility': campaign.visibility,
                    'goals': campaign.goals,
                    'accepted_influencers': accepted_influencers_names,
                    'requested_influencers': requested_influencers_names,
                    'pending_influencers': pending_influencers_names
                })
        
        return filename
