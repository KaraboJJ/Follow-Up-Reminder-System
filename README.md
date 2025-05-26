# Follow-Up-Reminder-System

# 🏥 Healthtech: Follow-Up Reminder System

A lightweight backend system for clinics and private doctors to automatically send appointment follow-up reminders via SMS using Twilio.

# 📋 Features

Manage patients, doctors, and appointments

Automatically send SMS reminders 24 hours before appointments

REST API for scheduling and retrieving appointments

Hourly reminder job powered by APScheduler

Built with Flask, SQLAlchemy, PostgreSQL, and Twilio

# 🔧 Requirements

Python 3.8+

PostgreSQL

Twilio account (for sending SMS)

# 🚀 Getting Started

1. Clone the Repository

git clone https://github.com/KaraboJJ/Follow-Up-Reminder-System.git
cd Follow-Up-Reminder-System

2. Install Dependencies

pip install Flask Flask-SQLAlchemy twilio psycopg2-binary APScheduler

3. Set Environment Variables
   
Create a .env file or export in your shell:

export TWILIO_ACCOUNT_SID='your_twilio_sid'
export TWILIO_AUTH_TOKEN='your_twilio_auth_token'
export TWILIO_PHONE_NUMBER='your_twilio_number'

4. Configure PostgreSQL
Update your connection string in the code if needed:

python

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost:5432/healthtech_db'
Create the database and tables:

flask shell
>>> from app import db
>>> db.create_all()
🖥️ Running the App

flask run
The app will start on http://127.0.0.1:5000/.

Reminders will be automatically checked and sent every hour by APScheduler.

# 📬 API Endpoints

# ➕ Create Appointment

http

POST /appointments
Content-Type: application/json
Request JSON:

json

{
  "patient_id": 1,
  "doctor_id": 2,
  "appointment_time": "2025-06-01 14:30:00"
}

# 📄 Get All Appointments

GET /appointments
Response JSON:

json

[
  {
    "id": 1,
    "patient": {
      "id": 1,
      "name": "John Doe",
      "phone_number": "+1234567890"
    },
    "doctor": {
      "id": 2,
      "name": "Dr. Smith",
      "phone_number": "+1987654321"
    },
    "appointment_time": "2025-06-01 14:30:00",
    "notified": false
  }
]

# 🔁 Reminder Logic
The system runs a background scheduler that checks every hour for appointments within the next 24 hours.

If any are found and not yet notified, it sends an SMS to both the patient and the doctor.

# 🛠 Future Improvements

Add WhatsApp and Email notification channels

User authentication and role-based access

Admin dashboard for appointment management

Dockerize the application for deployment

# 👨‍⚕️ Who It’s For

Small to mid-sized clinics

Private practitioners

Health service providers looking to automate communication
