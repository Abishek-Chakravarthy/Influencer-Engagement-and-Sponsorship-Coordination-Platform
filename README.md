
# Influencer Engagement & Sponsorship Coordination Platform

## Project Overview

The Influencer Engagement & Sponsorship Coordination Platform is an application designed to provide a user-friendly interface for sponsors to host campaigns and for influencers to collaborate with sponsors through ad-requests. The platform streamlines the interaction between sponsors and influencers, making it easier to manage and track campaigns.

## Approach

1. **User Roles and Attributes:** 
   - The platform features different user roles (e.g., Admin, Sponsor, Influencer). The attributes associated with each role were defined to ensure users are uniquely identifiable.

2. **Backend Development:**
   - The backend of the platform is built using **Flask**, providing APIs for user management, campaign creation, and other functionalities.
   - **Flask-JWT-Extended** is used for secure user authentication and authorization via JWT tokens.
   - **SQLAlchemy** is used for managing the database and interacting with models representing users, campaigns, and ad requests.
   - **Redis** is used to manage caching and **Celery** is used for handling asynchronous tasks, such as sending notifications or handling large batch jobs.

3. **Frontend Development:**
   - The frontend is built using **Vue.js**, a modern JavaScript framework. It is designed to be responsive, using **BootstrapVue** for UI components.
   - **Vuex** is used for state management and **Vue Router** is used to manage navigation across different components of the platform.
   - **Axios** is used to make HTTP requests to the backend, ensuring smooth communication between the frontend and backend.
   - **Chart.js** is used for data visualization, enabling users to track campaign performance and statistics.

4. **Asynchronous Jobs:** 
   - **Celery** is used to manage asynchronous tasks such as sending bulk emails, notifications, and processing large data sets.

## Libraries Used

- **Flask**: A lightweight Python web framework used to build the backend API.
- **Flask-JWT-Extended**: A library used to handle JSON Web Token (JWT) authentication and authorization.
- **SQLAlchemy**: An ORM for database interaction and management.
- **Flask-CORS**: A package to handle Cross-Origin Resource Sharing (CORS) for enabling requests from different origins.
- **Marshmallow**: For serializing and deserializing objects for API communication.
- **Celery**: An asynchronous task queue used for handling long-running or background tasks.
- **Vue.js**: A progressive JavaScript framework used for building user interfaces.
- **Vuex**: State management for Vue.js applications.
- **Vue Router**: For managing navigation and routing in the frontend application.
- **Axios**: For making HTTP requests to the backend API.
- **BootstrapVue**: A responsive UI framework for Vue.js.
- **Chart.js**: A charting library used for visualizing campaign data and performance metrics.

## Getting Started

1. **Clone the Repository:**
   - Clone the repository to your local machine:

   ```bash
   git clone https://github.com/Abishek-Chakravarthy/Influencer-Engagement-and-Sponsorship-Coordination-Platform.git
   cd Influencer-Engagement-and-Sponsorship-Coordination-Platform
   ```

2. **Set up the Backend:**
   - Install the necessary backend dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   - Set up environment variables, especially for mail configuration and database connection (refer to `config.py`).
   - Run the Flask application:

   ```bash
   flask run
   ```

3. **Set up the Frontend:**
   - Navigate to the `frontend` directory:

   ```bash
   cd frontend
   ```

   - Install the frontend dependencies:

   ```bash
   npm install
   ```

   - Run the frontend application:

   ```bash
   npm run serve
   ```

4. **Asynchronous Jobs (Celery):**
   - Start the Redis server and Celery worker for asynchronous tasks:

   ```bash
   celery -A your_app_name.celery worker --loglevel=info
   ```

5. **Access the Platform:**
   - The platform can be accessed at `http://localhost:5000` (for the backend) and `http://localhost:8080` (for the frontend).

## Conclusion

This platform provides a seamless and efficient way for sponsors and influencers to engage and collaborate. It allows for managing campaigns, tracking performance, and facilitating communication. With the backend and frontend working together, this application ensures smooth interaction between different user roles, improving the overall user experience.

