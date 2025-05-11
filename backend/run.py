from app import create_app, db,celery
from app.models import User  # Import the User model
from werkzeug.security import generate_password_hash


app = create_app()

def add_default_admin():
    # Check if the admin user already exists
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        # Create the admin user if it doesn't exist
        admin_user = User(
            username='admin',
            password=generate_password_hash('admin123'),  # Hash the password
            role='admin'
        )
        db.session.add(admin_user)
        db.session.commit()
        print('Default admin user added.')
    else:
        print('Admin user already exists.')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        add_default_admin()  # Add the default admin user after creating the database tables
    app.run(debug=True)

celery = celery
