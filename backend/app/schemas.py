from marshmallow import Schema, fields, validates, ValidationError, pre_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from .models import User, Campaign, AdRequest
from . import db

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True

    id = auto_field(dump_only=True)
    username = auto_field(required=True)
    password = auto_field(load_only=True)
    role = auto_field(required=True)
    company_name = auto_field()
    industry = auto_field()
    net_worth = auto_field()
    name = auto_field()
    category = auto_field()
    earnings=auto_field()
    niche = auto_field()
    reach = auto_field()
    is_flagged=auto_field()
    email=auto_field()
    @validates('username')
    def validate_username(self, value):
        if User.query.filter(User.username == value).first():
            raise ValidationError('Username is already in use.')

class CampaignSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Campaign
        sqla_session = db.session
        load_instance = True

    id = auto_field(dump_only=True)
    name = auto_field(required=True)
    description = auto_field()
    start_date = auto_field(required=True)
    end_date = auto_field(required=True)
    budget = auto_field(required=True)
    visibility = auto_field(required=True)
    goals = auto_field()
    sponsor_id = auto_field(required=True)
    is_flagged=auto_field()

class AdRequestSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = AdRequest
        sqla_session = db.session
        load_instance = True  # Optional: True means model instances are returned by load()

    id = auto_field(dump_only=True)
    campaign_id = auto_field(required=True)
    influencer_id = auto_field(required=True)
    messages = auto_field()
    requirements = auto_field()
    payment_amount = auto_field(required=True)
    status = auto_field(required=True)
    ad_name = auto_field()  # Field for the name of the advertisement
    ad_desc = auto_field()  # Field for the description of the advertisement
    req_by=auto_field(required=True)
    payment_date=auto_field()
    ad_terms = auto_field()  # Field for the terms and conditions of the advertisement
# Instantiate schemas for easy use throughout your application
user_schema = UserSchema()
users_schema = UserSchema(many=True)
campaign_schema = CampaignSchema()
campaigns_schema = CampaignSchema(many=True)
ad_request_schema = AdRequestSchema()
ad_requests_schema = AdRequestSchema(many=True)
