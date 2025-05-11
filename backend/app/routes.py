from flask import Blueprint, request, jsonify, send_file
from .models import db, User,Campaign,AdRequest
from .schemas import user_schema, users_schema, campaign_schema, campaigns_schema, ad_request_schema, ad_requests_schema
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_, and_,func,case
from datetime import datetime
from marshmallow import ValidationError
auth = Blueprint('auth', __name__)


def is_admin():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    return current_user.role == 'admin'

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    errors = user_schema.validate(data)
    if errors:
        print('Error:',errors)
        return jsonify(errors), 400

    user = user_schema.load(data)
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@auth.route('/login', methods=['POST'])
def login():
    print("Login route hit")
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()

    if user and user.check_password(data.get('password')):
        if user.is_flagged == 1:
            return jsonify({'message': 'You have been flagged by the admin, you cannot access this platform'}), 403
        
        access_token = create_access_token(identity=user.id)
        print("username :",user.username," request_status: ",user.request_status)
        return jsonify({'message':'Success','access_token': access_token, 'user': {'id': user.id, 'role': user.role,'username':user.username,'request_status':user.request_status}}), 200

    return jsonify({'message': 'Invalid credentials'}), 401


@auth.route('/admin/campaigns', methods=['GET'])
@jwt_required()
def get_all_campaigns():
    campaigns = db.session.query(
        Campaign.id,
        Campaign.name,
        Campaign.description,
        Campaign.start_date,
        Campaign.end_date,
        Campaign.budget,
        Campaign.amount_spent,
        Campaign.visibility,
        Campaign.sponsor_id,
        User.company_name,
        User.industry,
        User.net_worth
    ).join(User, User.id == Campaign.sponsor_id).all()

    result = [{
        'id': campaign.id,
        'name': campaign.name,
        'description': campaign.description,
        'start_date': campaign.start_date.strftime('%Y-%m-%d'),
        'end_date': campaign.end_date.strftime('%Y-%m-%d'),
        'budget': campaign.budget,
        'amount_spent': campaign.amount_spent,
        'visibility': campaign.visibility,
        'sponsor_id': campaign.sponsor_id,
        'company_name': campaign.company_name,
        'industry': campaign.industry,
        'net_worth': campaign.net_worth
    } for campaign in campaigns]

    return jsonify(result), 200



@auth.route('/admin/flagged', methods=['GET'])
@jwt_required()
def get_flagged_items():
    flagged_campaigns = db.session.query(
        Campaign.id,
        Campaign.name,
        Campaign.description,
        Campaign.start_date,
        Campaign.end_date,
        Campaign.budget,
        Campaign.amount_spent,
        Campaign.visibility,
        Campaign.sponsor_id,
        User.company_name,
        User.industry,
        User.net_worth
    ).join(User, User.id == Campaign.sponsor_id).filter(Campaign.is_flagged == 1).all()

    flagged_users = db.session.query(
        User.id,
        User.username,
        User.role,
        User.company_name,
        User.industry,
        User.net_worth,
        User.category,
        User.earnings,
        User.niche,
        User.reach
    ).filter(User.is_flagged == 1).all()

    result = [{
        'id': campaign.id,
        'name': campaign.name,
        'description': campaign.description,
        'start_date': campaign.start_date.strftime('%Y-%m-%d'),
        'end_date': campaign.end_date.strftime('%Y-%m-%d'),
        'budget': campaign.budget,
        'amount_spent': campaign.amount_spent,
        'visibility': campaign.visibility,
        'sponsor_id': campaign.sponsor_id,
        'company_name': campaign.company_name,
        'industry': campaign.industry,
        'net_worth': campaign.net_worth,
        'type': 'campaign'
    } for campaign in flagged_campaigns]

    result += [{
        'id': user.id,
        'name': user.username,
        'role': user.role,
        'company_name': user.company_name,
        'industry': user.industry,
        'net_worth': user.net_worth,
        'category': user.category,
        'earnings': user.earnings,
        'niche': user.niche,
        'reach': user.reach,
        'type': 'user'
    } for user in flagged_users]

    return jsonify(result), 200

@auth.route('/admin/remove-flag/campaign/<int:campaign_id>', methods=['POST'])
@jwt_required()
def remove_flag_campaign(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if not campaign:
        return jsonify({'success': False, 'message': 'Campaign not found'}), 404

    campaign.is_flagged = 0
    db.session.commit()
    return jsonify({'success': True, 'message': 'Flag removed from campaign'}), 200

@auth.route('/admin/remove-flag/user/<int:user_id>', methods=['POST'])
@jwt_required()
def remove_flag_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404

    user.is_flagged = 0
    db.session.commit()
    return jsonify({'success': True, 'message': 'Flag removed from user'}), 200

@auth.route('/admin/all', methods=['GET'])
@jwt_required()
def get_all_users_and_campaigns():
    users = User.query.all()
    campaigns = Campaign.query.all()

    users_result = [{
        'id': user.id,
        'name': user.username,
        'role': user.role,
        'company_name': user.company_name,
        'industry': user.industry,
        'net_worth': user.net_worth,
        'category': user.category,
        'earnings': user.earnings,
        'niche': user.niche,
        'reach': user.reach
    } for user in users]

    campaigns_result = [{
        'id': campaign.id,
        'name': campaign.name,
        'description': campaign.description,
        'start_date': campaign.start_date.strftime('%Y-%m-%d'),
        'end_date': campaign.end_date.strftime('%Y-%m-%d'),
        'budget': campaign.budget,
        'amount_spent': campaign.amount_spent,
        'visibility': campaign.visibility,
        'company_name': campaign.sponsor.company_name,
        'industry': campaign.sponsor.industry,
        'net_worth': campaign.sponsor.net_worth
    } for campaign in campaigns]

    return jsonify({'users': users_result, 'campaigns': campaigns_result}), 200

@auth.route('/admin/find', methods=['GET'])
@jwt_required()
def admin_find():
    search_type = request.args.get('type')
    attribute = request.args.get('attribute')
    query = request.args.get('query')

    if search_type == 'campaign':
        if attribute == 'Campaign name':
            campaigns = Campaign.query.filter(Campaign.name.ilike(f'%{query}%')).all()
        elif attribute == 'Campaign Company':
            campaigns = db.session.query(Campaign).join(User, User.id == Campaign.sponsor_id).filter(User.company_name.ilike(f'%{query}%')).all()
        elif attribute == 'Campaign budget':
            campaigns = Campaign.query.filter(Campaign.budget > float(query)).all()
        elif attribute == 'Campaign start date':
            try:
                start_date = datetime.strptime(query, '%d/%m/%Y').date()
                campaigns = Campaign.query.filter(Campaign.start_date > start_date).all()
            except ValueError:
                return jsonify({'message': 'Invalid date format. Please use dd/mm/yyyy.'}), 400
        elif attribute == 'Campaign end date':
            try:
                end_date = datetime.strptime(query, '%d/%m/%Y').date()
                campaigns = Campaign.query.filter(Campaign.end_date < end_date).all()
            except ValueError:
                return jsonify({'message': 'Invalid date format. Please use dd/mm/yyyy.'}), 400
        elif attribute == 'Campaign visibility':
            campaigns = Campaign.query.filter(Campaign.visibility.ilike(f'%{query}%')).all()
        result = [{
            'id': campaign.id,
            'name': campaign.name,
            'description': campaign.description,
            'start_date': campaign.start_date.strftime('%Y-%m-%d'),
            'end_date': campaign.end_date.strftime('%Y-%m-%d'),
            'budget': campaign.budget,
            'amount_spent': campaign.amount_spent,
            'visibility': campaign.visibility,
            'company_name': campaign.sponsor.company_name,
            'industry': campaign.sponsor.industry,
            'net_worth': campaign.sponsor.net_worth
        } for campaign in campaigns]
        return jsonify(result), 200

    elif search_type == 'sponsor':
        if attribute == 'Sponsor name':
            users = User.query.filter(User.role == 'sponsor', User.username.ilike(f'%{query}%')).all()
        elif attribute == 'Sponsor company':
            users = User.query.filter(User.role == 'sponsor', User.company_name.ilike(f'%{query}%')).all()
        elif attribute == 'Sponsor industry':
            users = User.query.filter(User.role == 'sponsor', User.industry.ilike(f'%{query}%')).all()
        elif attribute == 'Sponsor net worth':
            users = User.query.filter(User.role == 'sponsor', User.net_worth > float(query)).all()
        result = [{
            'id': user.id,
            'name': user.username,
            'role': user.role,
            'company_name': user.company_name,
            'industry': user.industry,
            'net_worth': user.net_worth
        } for user in users]
        return jsonify(result), 200

    elif search_type == 'influencer':
        if attribute == 'Influencer name':
            users = User.query.filter(User.role == 'influencer', User.username.ilike(f'%{query}%')).all()
        elif attribute == 'Influencer category':
            users = User.query.filter(User.role == 'influencer', User.category.ilike(f'%{query}%')).all()
        elif attribute == 'Influencer niche':
            users = User.query.filter(User.role == 'influencer', User.niche.ilike(f'%{query}%')).all()
        elif attribute == 'Influencer reach':
            users = User.query.filter(User.role == 'influencer', User.reach > float(query)).all()
        elif attribute == 'Influencer earnings':
            users = User.query.filter(User.role == 'influencer', User.earnings > float(query)).all()
        result = [{
            'id': user.id,
            'name': user.username,
            'role': user.role,
            'category': user.category,
            'niche': user.niche,
            'reach': user.reach,
            'earnings': user.earnings
        } for user in users]
        return jsonify(result), 200

@auth.route('/admin/flag/user/<int:user_id>', methods=['POST'])
@jwt_required()
def flag_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user.is_flagged = 1
    db.session.commit()
    return jsonify({'message': 'User flagged successfully'}), 200

@auth.route('/admin/flag/campaign/<int:campaign_id>', methods=['POST'])
@jwt_required()
def flag_campaign(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if not campaign:
        return jsonify({'message': 'Campaign not found'}), 404

    campaign.is_flagged = 1
    db.session.commit()
    return jsonify({'message': 'Campaign flagged successfully'}), 200

@auth.route('/admin/stats/user-distribution', methods=['GET'])
def get_user_distribution():
    total_influencers = User.query.filter_by(role='influencer').count()
    flagged_influencers = User.query.filter_by(role='influencer', is_flagged=1).count()
    total_sponsors = User.query.filter_by(role='sponsor').count()
    flagged_sponsors = User.query.filter_by(role='sponsor', is_flagged=1).count()

    data = {
        "total_influencers": total_influencers,
        "flagged_influencers": flagged_influencers,
        "total_sponsors": total_sponsors,
        "flagged_sponsors": flagged_sponsors
    }
    return jsonify(data), 200



@auth.route('/admin/stats/revenue-analysis', methods=['GET'])
@jwt_required()
def revenue_analysis():
    attribute = request.args.get('attribute', 'username')
    if attribute not in ['username', 'category', 'niche']:
        return jsonify({'message': 'Invalid attribute'}), 400
    
    if attribute == 'username':
        data = db.session.query(
            User.username.label('label'),
            db.func.sum(AdRequest.payment_amount).label('total_earnings')
        ).join(AdRequest, User.id == AdRequest.influencer_id) \
         .filter(User.role == 'influencer') \
         .group_by(User.username).order_by(db.func.sum(AdRequest.payment_amount).desc()).limit(10).all()
    elif attribute == 'category':
        data = db.session.query(
            User.category.label('label'),
            db.func.sum(AdRequest.payment_amount).label('total_earnings')
        ).join(AdRequest, User.id == AdRequest.influencer_id) \
         .filter(User.role == 'influencer') \
         .group_by(User.category).order_by(db.func.sum(AdRequest.payment_amount).desc()).limit(10).all()
    elif attribute == 'niche':
        data = db.session.query(
            User.niche.label('label'),
            db.func.sum(AdRequest.payment_amount).label('total_earnings')
        ).join(AdRequest, User.id == AdRequest.influencer_id) \
         .filter(User.role == 'influencer') \
         .group_by(User.niche).order_by(db.func.sum(AdRequest.payment_amount).desc()).limit(10).all()
    
    return jsonify([{'label': row.label, 'total_earnings': row.total_earnings} for row in data])

@auth.route('/admin/stats/campaign-statistics', methods=['GET'])
@jwt_required()
def campaign_statistics():
    data = db.session.query(
        Campaign.name,
        Campaign.budget,
        Campaign.amount_spent
    ).all()
    
    return jsonify([{
        'name': row.name,
        'budget': row.budget,
        'amount_spent': row.amount_spent
    } for row in data])

@auth.route('/admin/stats/active-companies', methods=['GET'])
@jwt_required()
def active_companies():
    attribute = request.args.get('attribute', 'company_name')
    if attribute not in ['company_name', 'industry']:
        return jsonify({'message': 'Invalid attribute'}), 400
    
    if attribute == 'company_name':
        data = db.session.query(
            User.company_name.label('label'),
            db.func.count(AdRequest.id).label('count')
        ).join(Campaign, User.id == Campaign.sponsor_id) \
         .join(AdRequest, Campaign.id == AdRequest.campaign_id) \
         .filter(AdRequest.status == 'accepted') \
         .group_by(User.company_name).order_by(db.func.count(AdRequest.id).desc()).limit(10).all()
    elif attribute == 'industry':
        data = db.session.query(
            User.industry.label('label'),
            db.func.count(AdRequest.id).label('count')
        ).join(Campaign, User.id == Campaign.sponsor_id) \
         .join(AdRequest, Campaign.id == AdRequest.campaign_id) \
         .filter(AdRequest.status == 'accepted') \
         .group_by(User.industry).order_by(db.func.count(AdRequest.id).desc()).limit(10).all()
    
    return jsonify([{'label': row.label, 'count': row.count} for row in data])

@auth.route('/admin/stats/company-ad-requests', methods=['GET'])
@jwt_required()
def company_ad_request_statistics():
    data = db.session.query(
        User.company_name.label('company_name'),
        db.func.count(db.case((AdRequest.status == 'accepted', 1))).label('accepted'),
        db.func.count(db.case((AdRequest.status == 'pending', 1))).label('pending'),
        db.func.count(db.case((AdRequest.status == 'negotiated', 1))).label('negotiated')
    ).join(Campaign, User.id == Campaign.sponsor_id) \
     .join(AdRequest, Campaign.id == AdRequest.campaign_id) \
     .group_by(User.company_name).all()
    
    return jsonify([{
        'company_name': row.company_name,
        'accepted': row.accepted,
        'pending': row.pending,
        'negotiated': row.negotiated
    } for row in data])


@auth.route('/admin/stats/total-ad-requests', methods=['GET'])
@jwt_required()
def total_ad_request_statistics():
    data = db.session.query(
        db.func.count(db.case((AdRequest.status == 'accepted', 1))).label('accepted'),
        db.func.count(db.case((AdRequest.status == 'pending', 1))).label('pending'),
        db.func.count(db.case((AdRequest.status == 'negotiated', 1))).label('negotiated')
    ).one()
    
    return jsonify({
        'accepted': data.accepted,
        'pending': data.pending,
        'negotiated': data.negotiated
    })

@auth.route('/sponsor-requests', methods=['GET'])
@jwt_required()
def get_sponsor_requests():
    if not is_admin():  # Ensure only admins can access this route
        return jsonify({'message': 'Unauthorized access'}), 403
    sponsors = User.query.filter_by(role='sponsor', request_status='pending').order_by(User.request_date).all()
    return jsonify(users_schema.dump(sponsors)), 200


@auth.route('/update-sponsor-status/<int:user_id>', methods=['POST'])
@jwt_required()
def update_sponsor_status(user_id):
    if not is_admin():
        return jsonify({'message': 'Unauthorized access'}), 403
    data = request.get_json()
    status = data.get('status')
    if status not in ['accepted', 'rejected']:
        return jsonify({'message': 'Invalid status'}), 400
    user = User.query.get(user_id)
    if user and user.role == 'sponsor':
        user.request_status = status
        db.session.commit()
        return jsonify({'message': f"Sponsor status updated to {status}."}), 200
    return jsonify({'message': 'User not found or not a sponsor'}), 404

@auth.route('/influencer/campaigns', methods=['GET'])
@jwt_required()
def get_influencer_campaigns():
    influencer_id = get_jwt_identity()
    # Join tables and fetch necessary fields
    results = db.session.query(
        Campaign.name.label('campaign_name'),
        User.company_name,
        User.industry,
        AdRequest.ad_name,
        AdRequest.ad_desc,
        AdRequest.ad_terms,
        AdRequest.requirements,
        AdRequest.messages,
        AdRequest.payment_amount,
        AdRequest.status
    ).join(AdRequest, AdRequest.campaign_id == Campaign.id) \
      .join(User, User.id == Campaign.sponsor_id) \
      .filter(
        AdRequest.influencer_id == influencer_id,
        AdRequest.status == 'accepted',
        Campaign.is_flagged==0,
        User.is_flagged==0
    ).all()

    # Format results for JSON serialization
    campaigns = [{
        'campaign_name': ad.campaign_name,
        'company_name': ad.company_name,
        'industry': ad.industry,
        'ad_name': ad.ad_name,
        'ad_desc': ad.ad_desc,
        'ad_terms': ad.ad_terms,
        'requirements': ad.requirements,
        'messages': ad.messages,
        'payment_amount': ad.payment_amount,
        'status': ad.status
    } for ad in results]

    return jsonify(campaigns)


@auth.route('/influencer/ad-requests', methods=['GET'])
@jwt_required()
def get_influencer_ad_requests():
    influencer_id = get_jwt_identity()
    ad_requests = db.session.query(
        AdRequest.id,
        Campaign.name.label('campaign_name'),
        User.company_name
    ).select_from(AdRequest) \
      .join(Campaign, AdRequest.campaign_id == Campaign.id) \
      .join(User, User.id == Campaign.sponsor_id) \
      .filter(
        AdRequest.influencer_id == influencer_id,
        or_(AdRequest.status == 'pending', AdRequest.status == 'negotiated'),
        AdRequest.req_by=='sponsor',
        User.is_flagged == 0,
        Campaign.is_flagged == 0
    ).all()

    results = [{
        'id': req.id,
        'campaign_name': req.campaign_name,
        'company_name': req.company_name
    } for req in ad_requests]
    print(results)
    return jsonify(results)


@auth.route('/influencer/ad-request/accept/<int:request_id>', methods=['POST'])
@jwt_required()
def accept_ad_request_influencer(request_id):
    influencer_id = get_jwt_identity()
    ad_request = AdRequest.query.filter_by(id=request_id, influencer_id=influencer_id).first()
    print("Accept function arrived")
    if not ad_request:
            return jsonify({'message': 'Ad request not found'}), 404
    if ad_request.campaign.amount_spent + ad_request.payment_amount > ad_request.campaign.budget:
        return jsonify({'message': 'Sponsor cannot afford this ad'}), 400


    influencer = User.query.get(ad_request.influencer_id)
    influencer.earnings += ad_request.payment_amount
    
    ad_request.status = 'accepted'
    ad_request.req_by='sponsor'
    ad_request.campaign.amount_spent += ad_request.payment_amount
    ad_request.payment_date = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Ad request accepted'}), 200

@auth.route('/influencer/ad-request/reject/<int:request_id>', methods=['DELETE'])
@jwt_required()
def reject_ad_request_influencer(request_id):
    influencer_id = get_jwt_identity()
    ad_request = AdRequest.query.filter_by(id=request_id, influencer_id=influencer_id).first()
    
    if not ad_request:
        return jsonify({'message': 'Ad request not found'}), 404
    
    db.session.delete(ad_request)
    db.session.commit()
    return jsonify({'message': 'Ad request rejected and removed successfully'}), 200

@auth.route('/influencer/ad-request/negotiate/<int:request_id>', methods=['POST'])
@jwt_required()
def influencer_negotiate_ad_request(request_id):
    influencer_id = get_jwt_identity()
    ad_request = AdRequest.query.filter_by(id=request_id, influencer_id=influencer_id).first()
    
    if not ad_request:
        return jsonify({'message': 'Ad request not found'}), 404
    
    data = request.get_json()
    ad_request.payment_amount = data.get('payment_amount', ad_request.payment_amount)
    ad_request.messages = data.get('messages', ad_request.messages)
    ad_request.status = 'negotiated'
    ad_request.req_by='influencer'
    try:
        db.session.commit()
        return jsonify({'message': 'Ad request renegotiation submitted'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Database error', 'error': str(e)}), 500



@auth.route('/ad-request/update/<int:id>', methods=['POST'])
@jwt_required()
def update_ad_request_status(id):
    data = request.get_json()
    ad_request = AdRequest.query.get(id)
    if ad_request and ad_request.influencer_id == get_jwt_identity():
        ad_request.status = data['status']
        db.session.commit()
        return jsonify({'message': 'Request status updated successfully'}), 200
    return jsonify({'message': 'Request not found'}), 404

@auth.route('/influencer/profile', methods=['GET'])
@jwt_required()
def get_influencer_profile():
    user_id = get_jwt_identity()
    print("Required function hit")
    user = User.query.get(user_id)
    print(f"Fetching profile for user ID: {user_id}")  # Debug print
    if user and user.role == 'influencer':
        print("User found, returning profile.")
        return jsonify(user_schema.dump(user)), 200
    else:
        print("User not found or not an influencer.")
        return jsonify({'message': 'User not found'}), 404



@auth.route('/influencer/update-profile', methods=['POST'])
@jwt_required()
def update_influencer_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user and user.role == 'influencer':
        data = request.get_json()
        user.name = data.get('name', user.name)
        user.category = data.get('category', user.category)
        user.niche = data.get('niche', user.niche)
        user.reach = data.get('reach', user.reach)
        if data.get('password'):
            user.password = generate_password_hash(data['password'])
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'}), 200
    return jsonify({'message': 'User not found'}), 404

@auth.route('/influencer/stats/revenue-analysis', methods=['GET'])
@jwt_required()
def influencer_revenue_analysis():
    influencer_id = get_jwt_identity()
    ad_requests = db.session.query(
        AdRequest.payment_date,
        func.sum(AdRequest.payment_amount).over(order_by=AdRequest.payment_date).label('total_earnings')
    ).filter(
        AdRequest.influencer_id == influencer_id,
        AdRequest.status == 'accepted'
    ).order_by(AdRequest.payment_date).all()

    result = [{'payment_date': req.payment_date.strftime('%Y-%m-%d %H:%M:%S'), 'total_earnings': req.total_earnings} for req in ad_requests]
    return jsonify(result), 200

@auth.route('/influencer/stats/trending-campaigns', methods=['GET'])
@jwt_required()
def influencer_trending_campaigns():
    ad_requests = db.session.query(
        Campaign.name.label('campaign_name'),
        func.count(AdRequest.id).label('ad_request_count')
    ).join(Campaign, AdRequest.campaign_id == Campaign.id
    ).filter(
        or_(AdRequest.status == 'accepted',
            (AdRequest.status.in_(['pending', 'negotiated']) & (AdRequest.req_by == 'influencer')))
    ).group_by(Campaign.name).all()

    result = [{'campaign_name': req.campaign_name, 'ad_request_count': req.ad_request_count} for req in ad_requests]
    return jsonify(result), 200

@auth.route('/influencer/stats/company-avg-ad-pay', methods=['GET'])
@jwt_required()
def influencer_company_avg_ad_pay():
    attribute = request.args.get('attribute', 'company_name')
    if attribute not in ['company_name', 'industry']:
        return jsonify({'message': 'Invalid attribute'}), 400

    if attribute == 'company_name':
        ad_requests = db.session.query(
            User.company_name.label('label'),
            func.avg(AdRequest.payment_amount).label('avg_payment_amount')
        ).join(Campaign, AdRequest.campaign_id == Campaign.id
        ).join(User, Campaign.sponsor_id == User.id
        ).group_by(User.company_name).all()
    elif attribute == 'industry':
        ad_requests = db.session.query(
            User.industry.label('label'),
            func.avg(AdRequest.payment_amount).label('avg_payment_amount')
        ).join(Campaign, AdRequest.campaign_id == Campaign.id
        ).join(User, Campaign.sponsor_id == User.id
        ).group_by(User.industry).all()

    result = [{'label': req.label, 'avg_payment_amount': req.avg_payment_amount} for req in ad_requests]
    return jsonify(result), 200

@auth.route('/influencer/stats/most-active-influencers', methods=['GET'])
@jwt_required()
def influencer_most_active():
    ad_requests = db.session.query(
        User.name.label('influencer_name'),
        func.count(AdRequest.id).label('ad_request_count')
    ).join(User, AdRequest.influencer_id == User.id
    ).filter(
        or_(AdRequest.status == 'accepted',
            (AdRequest.status.in_(['pending', 'negotiated']) & (AdRequest.req_by == 'sponsor')))
    ).group_by(User.name).all()

    result = [{'influencer_name': req.influencer_name, 'ad_request_count': req.ad_request_count} for req in ad_requests]
    return jsonify(result), 200

@auth.route('/sponsor/campaigns', methods=['GET'])
@jwt_required()
def get_sponsor_campaigns():
    sponsor_id = get_jwt_identity()
    campaigns = Campaign.query.filter_by(sponsor_id=sponsor_id,is_flagged = 0).all()
    return jsonify([campaign.to_dict() for campaign in campaigns])

@auth.route('/campaigns', methods=['GET'])
@jwt_required()
def get_campaigns():
    sponsor_id = get_jwt_identity()
    sponsor = User.query.get(sponsor_id)
    if sponsor.role != 'sponsor':
        return jsonify({"message": "Unauthorized"}), 403
    campaigns = Campaign.query.filter_by(sponsor_id=sponsor.id).all()
    return jsonify([campaign.to_dict() for campaign in campaigns])

@auth.route('/campaigns/<int:campaign_id>', methods=['PUT'])
@jwt_required()
def update_campaign(campaign_id):
    sponsor_id = get_jwt_identity()
    sponsor = User.query.get(sponsor_id)
    if sponsor.role != 'sponsor':
        return jsonify({"message": "Unauthorized"}), 403
    data = request.get_json()
    campaign = Campaign.query.get(campaign_id)
    if campaign.sponsor_id != sponsor.id:
        return jsonify({"message": "Unauthorized"}), 403
    campaign.name = data['name']
    campaign.description = data['description']
    campaign.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
    campaign.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
    campaign.budget = data['budget']
    campaign.visibility = data['visibility']
    db.session.commit()
    return jsonify(campaign.to_dict())

@auth.route('/campaigns/<int:campaign_id>', methods=['DELETE'])
@jwt_required()
def delete_campaign(campaign_id):
    sponsor_id = get_jwt_identity()
    sponsor = User.query.get(sponsor_id)
    if sponsor.role != 'sponsor':
        return jsonify({"message": "Unauthorized"}), 403
    campaign = Campaign.query.get(campaign_id)
    if campaign.sponsor_id != sponsor.id:
        return jsonify({"message": "Unauthorized"}), 403
    AdRequest.query.filter_by(campaign_id=campaign.id).delete()
    db.session.delete(campaign)
    db.session.commit()
    return jsonify({"message": "Campaign deleted"})

@auth.route('/sponsor/ad-requests', methods=['GET'])
@jwt_required()
def get_sponsor_ad_requests():
    sponsor_id = get_jwt_identity()
    #print('Ad searching commenced')
    
    # Correctly applying the or_ function to combine conditions
    ad_requests = db.session.query(
        AdRequest.id,
        AdRequest.requirements,
        AdRequest.messages,
        AdRequest.payment_amount,
        AdRequest.status,
        Campaign.name.label('campaign_name'),
        User.username.label('influencer_name')
    ).join(Campaign, Campaign.id == AdRequest.campaign_id
    ).join(User, User.id == AdRequest.influencer_id
    ).filter(
        Campaign.sponsor_id == sponsor_id,
        or_(AdRequest.status == 'pending', AdRequest.status == 'negotiated'),
        AdRequest.req_by == 'influencer',
        User.is_flagged == 0
    ).all()

    # Prepare the data for JSON response
    results = [{
        'id': req.id,
        'requirements': req.requirements,
        'messages': req.messages,
        'payment_amount': req.payment_amount,
        'status': req.status,
        'campaign_name': req.campaign_name,
        'influencer_name': req.influencer_name
    } for req in ad_requests]

    #print(results)
    return jsonify(results)    

@auth.route('/sponsor/ad-request/accept/<int:request_id>', methods=['POST'])
@jwt_required()
def accept_ad_request(request_id):
    sponsor_id = get_jwt_identity()
    ad_request = AdRequest.query.filter_by(id=request_id).first()
    
    if ad_request is None:
        return jsonify({'message': 'Ad request not found'}), 404

    if ad_request.campaign.sponsor_id != sponsor_id:
        return jsonify({'message': 'Unauthorized access'}), 403

    data = request.get_json()
    ad_request.ad_name = data.get('ad_name')
    ad_request.ad_desc = data.get('ad_desc')
    ad_request.ad_terms = data.get('ad_terms')
    
    if ad_request.campaign.amount_spent + ad_request.payment_amount > ad_request.campaign.budget:
        return jsonify({'message': 'Budget exceeded'}), 400

    ad_request.status = 'accepted'
    ad_request.req_by='influencer'
    ad_request.payment_date = datetime.utcnow()
    ad_request.campaign.amount_spent += ad_request.payment_amount
    influencer = User.query.get(ad_request.influencer_id)
    influencer.earnings += ad_request.payment_amount

    db.session.commit()
    return jsonify({'message': 'Ad request accepted and campaign updated successfully'}), 200

@auth.route('/sponsor/ad-request/reject/<int:request_id>', methods=['DELETE'])
@jwt_required()
def reject_ad_request(request_id):
    sponsor_id = get_jwt_identity()
    ad_request = AdRequest.query.filter_by(id=request_id).first()
    
    if ad_request is None:
        return jsonify({'message': 'Ad request not found'}), 404
    
    try:
        db.session.delete(ad_request)
        db.session.commit()
        return jsonify({'message': 'Ad request rejected and removed successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Database error', 'error': str(e)}), 500
    
@auth.route('/sponsor/ad-request/negotiate/<int:request_id>', methods=['POST'])
@jwt_required()
def sponsor_negotiate_ad_request(request_id):
    sponsor_id = get_jwt_identity()
    ad_request = AdRequest.query.join(Campaign, AdRequest.campaign_id == Campaign.id) \
                                .filter(AdRequest.id == request_id, Campaign.sponsor_id == sponsor_id).first()
    
    if not ad_request:
        return jsonify({'message': 'Ad request not found'}), 404
    
    data = request.get_json()
    ad_request.payment_amount = data.get('payment_amount', ad_request.payment_amount)
    ad_request.messages = data.get('messages', ad_request.messages)
    ad_request.status = 'negotiated'
    ad_request.req_by='sponsor'
    try:
        db.session.commit()
        return jsonify({'message': 'Ad request successfully renegotiated'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Database error', 'error': str(e)}), 500

    
@auth.route('/sponsor/profile', methods=['GET'])
@jwt_required()
def get_sponsor_profile():
    sponsor_id = get_jwt_identity()
    sponsor = User.query.get(sponsor_id)
    if sponsor and sponsor.role == 'sponsor':
        return jsonify({
            'username': sponsor.username,
            'company_name': sponsor.company_name,
            'industry': sponsor.industry,
            'net_worth': sponsor.net_worth
        }), 200
    return jsonify({'message': 'Sponsor not found'}), 404

@auth.route('/sponsor/update-profile', methods=['POST'])
@jwt_required()
def update_sponsor_profile():
    sponsor_id = get_jwt_identity()
    sponsor = User.query.get(sponsor_id)
    if sponsor and sponsor.role == 'sponsor':
        data = request.get_json()
        if 'password' in data and data['password']:
            sponsor.password = generate_password_hash(data['password'])
        sponsor.company_name = data.get('company_name', sponsor.company_name)
        sponsor.industry = data.get('industry', sponsor.industry)
        sponsor.net_worth = data.get('net_worth', sponsor.net_worth)
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'}), 200
    return jsonify({'message': 'Sponsor not found'}), 404


@auth.route('/sponsor/campaigns', methods=['POST'])
@jwt_required()
def add_sponsor_campaign():
    sponsor_id = get_jwt_identity()
    data = request.get_json()
    try:
        # Convert date strings to date objects
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date() if data['start_date'] else None
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data['end_date'] else None
    except ValueError:
        return jsonify({'message': 'Invalid date format, expected YYYY-MM-DD'}), 400
    new_campaign = Campaign(
        name=data['name'],
        description=data['description'],
        start_date=start_date,
        end_date=end_date,
        budget=data['budget'],
        amount_spent=0,  # Default to 0 as per the spec
        visibility=data['visibility'],
        goals=data['goals'],
        sponsor_id=sponsor_id,  # Set the sponsor ID based on the current user
        is_flagged=0  # Default to False
    )
    db.session.add(new_campaign)
    try:
        db.session.commit()
        return jsonify({'message': 'Campaign created successfully'}), 201
    except Exception as e:
        print("Error:",str(e))
        db.session.rollback()
        return jsonify({'message': 'Error creating campaign', 'error': str(e)}), 500

@auth.route('/campaigns/public', methods=['GET'])
def get_public_campaigns():
    attribute = request.args.get('attribute', 'name')
    query = request.args.get('query', '')

    # Prepare a base query
    base_query = db.session.query(
    Campaign.id,
    Campaign.name,
    Campaign.description,
    Campaign.start_date,
    Campaign.end_date,
    Campaign.budget,
    User.company_name,
    User.industry,
    User.net_worth
).join(User, User.id == Campaign.sponsor_id).filter(
    or_(Campaign.visibility == 'Public', Campaign.visibility.ilike('public')),
    Campaign.is_flagged == 0,
    User.is_flagged == 0
)

    # Dynamically adjust query based on the attribute and query string
    if attribute in ['name', 'company', 'industry']:
        like_clause = f"%{query}%"
        conditions = {
            'name': Campaign.name.like(like_clause),
            'company': User.company_name.like(like_clause),
            'industry': User.industry.like(like_clause)
        }
        base_query = base_query.filter(conditions[attribute])
    elif attribute == 'budget':
        try:
            budget_threshold = float(query)
            base_query = base_query.filter(Campaign.budget >= budget_threshold)
        except ValueError:
            return jsonify({"error": "Invalid budget value"}), 400

    # Execute the query
    campaigns = base_query.all()

    # Serialize the data for JSON response
    campaigns_data = [{
        'id': c.id,
        'name': c.name,
        'company_name': c.company_name,
        'company_industry': c.industry,
        'company_net_worth': c.net_worth,
        'description': c.description,
        'start_date': c.start_date.strftime('%Y-%m-%d') if c.start_date else None,
        'end_date': c.end_date.strftime('%Y-%m-%d') if c.end_date else None,
        'budget': c.budget
    } for c in campaigns]

    return jsonify(campaigns_data)

@auth.route('/influencer/create-ad-request', methods=['POST'])
@jwt_required()
def create_ad_request():
    data = request.get_json()
    new_request = AdRequest(
        campaign_id=data['campaign_id'],
        influencer_id=get_jwt_identity(),  # This assumes the influencer's ID is stored in JWT token
        messages=data['messages'],
        payment_amount=data['payment_amount'],
        status='pending',
        req_by='influencer'
    )
    db.session.add(new_request)
    try:
        db.session.commit()
        return jsonify({'message': 'Request created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to create request', 'error': str(e)}), 500

@auth.route('/sponsor/create-ad-request', methods=['POST'])
@jwt_required()
def create_sponsor_ad_request():
    data = request.get_json()
    sponsor_id = get_jwt_identity()  # Assumes sponsor's ID is stored in JWT token

    # Create a new AdRequest instance
    new_request = AdRequest(
        campaign_id=data['campaign_id'],
        influencer_id=data['influencer_id'],  # ID of the influencer to whom the request is being made
        requirements=data['requirements'],  # Requirements specified by the sponsor
        payment_amount=data['payment_amount'],  # Proposed payment amount
        status='pending',  # Initial status of the ad request
        req_by='sponsor'
    )
    
    db.session.add(new_request)
    try:
        db.session.commit()
        return jsonify({'message': 'Ad request created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to create ad request', 'error': str(e)}), 500

@auth.route('/sponsor/search', methods=['GET'])
@jwt_required()
def search_items():
    attribute = request.args.get('attribute', 'name')
    query = request.args.get('query', '')
    query_type = request.args.get('type', 'campaign')

    if query_type not in ['campaign', 'influencer']:
        return jsonify({'message': 'Invalid search type'}), 400

    if query_type == 'campaign':
        base_query = db.session.query(
            Campaign.id.label('id'),
            Campaign.name.label('name'),
            Campaign.description.label('description'),
            Campaign.start_date.label('start_date'),
            Campaign.end_date.label('end_date'),
            Campaign.budget.label('budget'),
            User.company_name.label('company_name'),
            User.industry.label('industry')
        ).join(User, User.id == Campaign.sponsor_id).filter(
            Campaign.visibility == 'Public',
            Campaign.is_flagged == 0
        )

        if attribute == 'name':
            base_query = base_query.filter(Campaign.name.like(f'%{query}%'))
        elif attribute == 'company':
            base_query = base_query.filter(User.company_name.like(f'%{query}%'))
        elif attribute == 'industry':
            base_query = base_query.filter(User.industry.like(f'%{query}%'))
        elif attribute == 'budget':
            base_query = base_query.filter(Campaign.budget >= float(query))

        results = base_query.all()
        return jsonify([{
            'id': result.id,
            'name': result.name,
            'description': result.description,
            'start_date': result.start_date.strftime('%Y-%m-%d') if result.start_date else None,
            'end_date': result.end_date.strftime('%Y-%m-%d') if result.end_date else None,
            'budget': result.budget,
            'company_name': result.company_name,
            'industry': result.industry
        } for result in results])

    elif query_type == 'influencer':
        base_query = User.query.filter(User.role == 'influencer', User.is_flagged == 0)

        if attribute == 'name':
            base_query = base_query.filter(User.name.like(f'%{query}%'))
        elif attribute == 'category':
            base_query = base_query.filter(User.category.like(f'%{query}%'))
        elif attribute == 'niche':
            base_query = base_query.filter(User.niche.like(f'%{query}%'))
        elif attribute == 'reach':
            base_query = base_query.filter(User.reach >= int(query))

        results = base_query.all()
        return jsonify([{
            'id': user.id,
            'name': user.name,
            'category': user.category,
            'niche': user.niche,
            'reach': user.reach
        } for user in results])

    return jsonify({'message': 'No results found'}), 404

    

@auth.route('/influencers/public', methods=['GET'])
def get_public_influencers():
    try:
        # Fetch all users where role is 'influencer'
        influencers = User.query.filter_by(role='influencer', is_flagged=0).all()
        # Serialize the data for JSON response
        return jsonify(users_schema.dump(influencers)), 200
    except Exception as e:
        # Handle any errors that occur during the query
        return jsonify({'message': 'Failed to fetch influencers', 'error': str(e)}), 500

@auth.route('/campaigns/<int:campaign_id>', methods=['GET'])
def get_campaign_details(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if campaign and campaign.visibility.lower() == 'public':
        return jsonify(campaign.to_dict()), 200
    return jsonify({'message': 'Campaign not found'}), 404

@auth.route('/influencers/<int:influencer_id>', methods=['GET'])
def get_influencer_details(influencer_id):
    influencer = User.query.filter_by(id=influencer_id, role='influencer').first()
    if influencer:
        return jsonify(user_schema.dump(influencer)), 200
    return jsonify({'message': 'Influencer not found'}), 404

@auth.route('/campaign_info/<int:campaign_id>', methods=['GET'])
def get_campaign(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if campaign:
        campaign_details = {
            'id': campaign.id,
            'name': campaign.name,
            'description': campaign.description,
            'start_date': campaign.start_date.strftime('%Y-%m-%d') if campaign.start_date else None,
            'end_date': campaign.end_date.strftime('%Y-%m-%d') if campaign.end_date else None,
            'budget': campaign.budget
        }
        return jsonify(campaign_details), 200
    return jsonify({'message': 'Campaign not found'}), 404

@auth.route('/ad-requests/<int:campaign_id>', methods=['GET'])
def get_ad_requests_for_campaign(campaign_id):
    print("Arrived here")
    ad_requests = db.session.query(
        AdRequest.id,
        AdRequest.requirements,
        AdRequest.messages,
        AdRequest.payment_amount,
        AdRequest.status,
        User.name
    ).join(User, User.id == AdRequest.influencer_id) \
    .filter(
        AdRequest.campaign_id == campaign_id,
        User.is_flagged == 0
    ).all()

    results = [{
        'id': ad.id,
        'requirements': ad.requirements,
        'message': ad.messages if ad.messages else "",
        'paymentAmount': ad.payment_amount,
        'status': ad.status,
        'influencerName': ad.name
    } for ad in ad_requests]
    #print(results)
    return jsonify(results), 200

@auth.route('/ad-requests/<int:ad_request_id>', methods=['PUT'])
@jwt_required()
def update_ad_request(ad_request_id):
    sponsor_id = get_jwt_identity()
    ad_request = AdRequest.query.get(ad_request_id)
    campaign = Campaign.query.get(ad_request.campaign_id)
    if campaign.sponsor_id != sponsor_id:
        return jsonify({"message": "Unauthorized"}), 403
    data = request.get_json()
    if ad_request.status in ['pending', 'negotiated']:
        influencer = User.query.filter_by(username=data['influencer_name'], role='influencer').first()
        if not influencer:
            return jsonify({"message": "Influencer not found"}), 404
        ad_request.influencer_id = influencer.id
        ad_request.payment_amount = data['payment_amount']
        ad_request.ad_name = data['ad_name']
        ad_request.ad_desc = data['ad_desc']
        ad_request.ad_terms = data['ad_terms']
    ad_request.requirements = data['requirements']
    ad_request.messages = data['message']
    ad_request.req_by='sponsor'
    db.session.commit()
    return jsonify(ad_request.to_dict())

@auth.route('/ad-requests/<int:ad_request_id>', methods=['DELETE'])
@jwt_required()
def delete_ad_request(ad_request_id):
    sponsor_id = get_jwt_identity()
    ad_request = AdRequest.query.get(ad_request_id)
    campaign = Campaign.query.get(ad_request.campaign_id)
    if campaign.sponsor_id != sponsor_id:
        return jsonify({"message": "Unauthorized"}), 403
    db.session.delete(ad_request)
    db.session.commit()
    return jsonify({"message": "Ad request deleted successfully"})

@auth.route('/influencers/by-niche', methods=['GET'])
@jwt_required()
def get_influencers_by_niche():
    niche = request.args.get('niche', type=str)
    if not niche:
        return jsonify({'message': 'Niche parameter is required'}), 400
    
    influencers = User.query.filter(User.role == 'influencer', User.is_flagged == 0, User.niche.like(f'%{niche}%')).all()
    if not influencers:
        return jsonify([]), 200
    
    return jsonify([{
        'id': influencer.id,
        'username': influencer.username
    } for influencer in influencers]), 200

@auth.route('/ad-requests', methods=['POST'])
@jwt_required()
def sponsor_create_ad_request():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    # Validate and deserialize data using the instantiated schema
    try:
        new_ad_request = ad_request_schema.load(data)
    except ValidationError as err:
        print('Validation Error:', err.messages)
        return jsonify(err.messages), 400

    # Fetch the associated Campaign to check budget constraints
    campaign = Campaign.query.get(new_ad_request.campaign_id)
    if not campaign:
        return jsonify({'message': 'Campaign not found'}), 404

    # Check if adding this ad request exceeds the campaign's budget
    projected_amount_spent = campaign.amount_spent + new_ad_request.payment_amount
    if projected_amount_spent > campaign.budget:
        return jsonify({'message': 'The cost of this ad and the amount spent on the campaign exceeds the budget of the campaign'}), 400

    try:
        # Update the amount spent on the campaign
        campaign.amount_spent = projected_amount_spent
        new_ad_request.status = 'pending'
        db.session.add(new_ad_request)
        db.session.add(campaign)  # Ensure the campaign update is committed
        db.session.commit()
        return jsonify({'message': 'Ad request created successfully', 'id': new_ad_request.id}), 201
    except Exception as e:
        db.session.rollback()
        print("Error:", str(e))
        return jsonify({'message': 'Failed to create ad request', 'error': str(e)}), 500
    
@auth.route('/ad-requests-details/<int:request_id>', methods=['GET'])
@jwt_required()
def get_ad_request_details(request_id):
    print("Request ID Received:", request_id)
    # This query joins the necessary tables and fetches the correct fields.
    query = db.session.query(
        AdRequest, 
        User.username.label('influencer_name'),
        User.category,
        User.niche,
        User.reach,
        Campaign.name.label('campaign_name'),
        Campaign.sponsor_id
    ).join(User, User.id == AdRequest.influencer_id
    ).join(Campaign, Campaign.id == AdRequest.campaign_id
    ).filter(AdRequest.id == request_id
    ).first()

    if query:
        ad_request, influencer_name, category, niche, reach, campaign_name, sponsor_id = query
        
        # Fetch sponsor details using sponsor_id
        sponsor = User.query.filter_by(id=sponsor_id).first()
        if sponsor:
            details = {
                'campaign_name': campaign_name,
                'influencer_name': influencer_name,
                'category': category,
                'niche': niche,
                'reach': reach,
                'messages': ad_request.messages,
                'payment_amount': ad_request.payment_amount,
                'ad_name': ad_request.ad_name,
                'ad_desc': ad_request.ad_desc,
                'ad_terms': ad_request.ad_terms,
                'company_name': sponsor.company_name,
                'industry': sponsor.industry,
                'net_worth': sponsor.net_worth
            }
            return jsonify(details), 200
        else:
            return jsonify({'message': 'Sponsor not found'}), 404
    else:
        return jsonify({'message': 'Ad request not found'}), 404

@auth.route('/sponsor/stats/total-amount-spent', methods=['GET'])
@jwt_required()
def total_amount_spent():
    sponsor_id = get_jwt_identity()
    ad_requests = db.session.query(
        AdRequest.payment_date,
        func.sum(AdRequest.payment_amount).over(order_by=AdRequest.payment_date).label('total_amount')
    ).filter(
        AdRequest.campaign.has(sponsor_id=sponsor_id),
        AdRequest.status == 'accepted'
    ).all()

    result = {'dates': [str(req.payment_date) for req in ad_requests], 'amounts': [req.total_amount for req in ad_requests]}
    return jsonify(result), 200

@auth.route('/sponsor/stats/my-campaigns', methods=['GET'])
@jwt_required()
def my_campaigns():
    sponsor_id = get_jwt_identity()
    campaigns = Campaign.query.filter_by(sponsor_id=sponsor_id).all()
    result = [{
        'name': c.name,
        'budget': c.budget,
        'amount_spent': c.amount_spent
    } for c in campaigns]
    return jsonify(result), 200

@auth.route('/sponsor/stats/most-active-companies', methods=['GET'])
@jwt_required()
def most_active_companies():
    attribute = request.args.get('attribute', 'company_name')

    if attribute == 'company_name':
        label_case = User.company_name
    else:
        label_case = User.industry

    ad_requests = db.session.query(
        label_case.label('label'),
        func.count(AdRequest.id).label('ad_request_count')
    ).join(Campaign, AdRequest.campaign_id == Campaign.id
    ).join(User, Campaign.sponsor_id == User.id
    ).filter(
        AdRequest.status == 'accepted'
    ).group_by(label_case).all()

    result = [{'label': req.label, 'ad_request_count': req.ad_request_count} for req in ad_requests]
    return jsonify(result), 200

@auth.route('/sponsor/stats/most-active-influencers', methods=['GET'])
@jwt_required()
def most_active_influencers():
    sponsor_id = get_jwt_identity()
    ad_requests = db.session.query(
        User.username,
        func.count(AdRequest.id).label('ad_request_count')
    ).join(Campaign, AdRequest.campaign_id == Campaign.id
    ).join(User, AdRequest.influencer_id == User.id
    ).filter(
        ((AdRequest.status == 'accepted') | ((AdRequest.status.in_(['pending', 'negotiated'])) & (AdRequest.req_by == 'sponsor')))
    ).group_by(User.username).all()

    result = [{'username': req.username, 'ad_request_count': req.ad_request_count} for req in ad_requests]
    return jsonify(result), 200

@auth.route('/sponsor/export-report', methods=['GET'])
@jwt_required()
def export_report():
    sponsor_id = get_jwt_identity()
    sponsor = User.query.get(sponsor_id)
    if sponsor.role != 'sponsor':
        return jsonify({"message": "Unauthorized"}), 403
    
    from .celery import export_campaigns_to_csv  # Delayed import

    filepath = export_campaigns_to_csv(sponsor_id)
    print("Received filepath:",filepath)
    return send_file(filepath, as_attachment=True, download_name=os.path.basename(filepath))