from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from twilio.rest import Client
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import os

app = Flask("Follow-Up Health App")

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost:5432/healthtech_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Twilio credentials (set these as environment variables for security)
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Models
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    appointment_time = db.Column(db.DateTime, nullable=False)
    notified = db.Column(db.Boolean, default=False)

    patient = db.relationship('Patient')
    doctor = db.relationship('Doctor')

# Helper function to send message
def send_reminder(to, message):
    client.messages.create(
        to=to,
        from_=TWILIO_PHONE_NUMBER,
        body=message
    )

# Reminder job function
def send_reminders():
    now = datetime.now()
    upcoming_appointments = Appointment.query.filter(
        Appointment.appointment_time <= now + timedelta(hours=24),
        Appointment.appointment_time > now,
        Appointment.notified == False
    ).all()

    for appt in upcoming_appointments:
        patient_msg = f"Reminder: You have an appointment with Dr. {appt.doctor.name} at {appt.appointment_time}."
        doctor_msg = f"Reminder: You have an appointment with {appt.patient.name} at {appt.appointment_time}."
        send_reminder(appt.patient.phone_number, patient_msg)
        send_reminder(appt.doctor.phone_number, doctor_msg)
        appt.notified = True
        db.session.commit()

    if upcoming_appointments:
        print(f"Sent {len(upcoming_appointments)} reminders.")

# API endpoint to schedule appointment
@app.route('/appointments', methods=['POST'])
def create_appointment():
    data = request.get_json()
    new_appointment = Appointment(
        patient_id=data['patient_id'],
        doctor_id=data['doctor_id'],
        appointment_time=datetime.strptime(data['appointment_time'], '%Y-%m-%d %H:%M:%S')
    )
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment created successfully.'}), 201

# API endpoint to get all appointments
@app.route('/appointments', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.all()
    result = []
    for appt in appointments:
        result.append({
            'id': appt.id,
            'patient': {
                'id': appt.patient.id,
                'name': appt.patient.name,
                'phone_number': appt.patient.phone_number
            },
            'doctor': {
                'id': appt.doctor.id,
                'name': appt.doctor.name,
                'phone_number': appt.doctor.phone_number
            },
            'appointment_time': appt.appointment_time.strftime('%Y-%m-%d %H:%M:%S'),
            'notified': appt.notified
        })
    return jsonify(result)

# Scheduler setup
scheduler = BackgroundScheduler()
scheduler.add_job(func=send_reminders, trigger="interval", hours=1)
scheduler.start()

# Shutdown scheduler when exiting the app
import atexit
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    app.run(debug=True)
