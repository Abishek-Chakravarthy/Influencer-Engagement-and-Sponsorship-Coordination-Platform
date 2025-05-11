from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
'''from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()'''

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # Example roles: 'admin', 'sponsor', 'influencer'
    company_name = db.Column(db.String(120), nullable=True)
    industry = db.Column(db.String(120), nullable=True)
    net_worth = db.Column(db.Float, nullable=True)
    name = db.Column(db.String(120), nullable=True)
    category = db.Column(db.String(120), nullable=True)
    niche = db.Column(db.String(120), nullable=True)
    reach = db.Column(db.Integer, nullable=True)
    earnings=db.Column(db.Integer,default=0,nullable=True)
    request_status = db.Column(db.String(10), default='pending', nullable=True)  # New field for approval status
    request_date = db.Column(db.DateTime, default=datetime.utcnow)  # Track when the request was made
    is_flagged=db.Column(db.Integer,default=0)
    email = db.Column(db.Text, nullable=True)
    campaigns = db.relationship('Campaign', backref='sponsor', lazy=True)
    ad_requests = db.relationship('AdRequest', backref='influencer', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Campaign(db.Model):
    __tablename__ = 'campaigns'
    id = db.Column(db.Integer, primary_key=True)
    name = db   .Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Float, nullable=False)  # Total budget allocated for the campaign
    amount_spent = db.Column(db.Float, default=0.0, nullable=False)  # Cumulative amount spent on the campaign
    visibility = db.Column(db.String(10), nullable=False)  # Public or private visibility of the campaign
    goals = db.Column(db.Text, nullable=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_flagged = db.Column(db.Integer, default=0)  # Indicator if the campaign is flagged for review

    ad_requests = db.relationship('AdRequest', backref='campaign', lazy=True)

    def update_amount_spent(self, amount):
        """Update the amount spent on the campaign and ensure it does not exceed the budget."""
        if self.amount_spent + amount <= self.budget:
            self.amount_spent += amount
            db.session.commit()
            return True
        return False  # Optionally handle cases where the budget is exceeded
    def to_dict(self):
        sponsor = User.query.get(self.sponsor_id)
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date.strftime('%Y-%m-%d'),
            'end_date': self.end_date.strftime('%Y-%m-%d'),
            'budget': self.budget,
            'amount_spent': self.amount_spent,
            'visibility': self.visibility,
            'goals': self.goals,
            'sponsor_id': self.sponsor_id,
            'is_flagged': self.is_flagged,
            'company_name': sponsor.company_name,
            'company_industry': sponsor.industry,
            'company_net_worth': sponsor.net_worth
        }
    
class AdRequest(db.Model):
    __tablename__ = 'ad_requests'
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    messages = db.Column(db.Text, nullable=True)
    requirements = db.Column(db.Text, nullable=True)
    payment_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(10), nullable=False)
    ad_name = db.Column(db.Text, nullable=True)  # Name of the advertisement
    ad_desc = db.Column(db.Text, nullable=True)  # Description of the advertisement
    ad_terms = db.Column(db.Text, nullable=True)  # Terms and conditions for the advertisement
    req_by=db.Column(db.Text,nullable=False,default='admin')
    payment_date = db.Column(db.DateTime)
    def __repr__(self):
        return f'<AdRequest {self.id} - Campaign: {self.campaign_id}>'
    
    def to_dict(self):
        influencer = User.query.get(self.influencer_id)
        return {
            'id': self.id,
            'influencer_id': self.influencer_id,
            'influencerName': influencer.username,  # Assuming the user model has a username field
            'campaign_id': self.campaign_id,
            'ad_name': self.ad_name,
            'ad_desc': self.ad_desc,
            'ad_terms': self.ad_terms,
            'payment_amount': self.payment_amount,
            'requirements': self.requirements,
            'messages': self.messages,
            'status': self.status
        }

