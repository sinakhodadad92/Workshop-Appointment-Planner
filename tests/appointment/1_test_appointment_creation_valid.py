import pytest
from models.appointment import Appointment

def test_appointment_creation_with_valid_data():
    # Valid appointment details
    customer_name = "John Doe"
    vehicle_type = "Sedan"
    appointment_date = "2024-08-15"
    appointment_time = "10:00"
    maintenance_type = "Oil Change"
    email = "john.doe@example.com"

    # Create an appointment
    appointment = Appointment(
        customer_name=customer_name,
        vehicle_type=vehicle_type,
        appointment_date=appointment_date,
        appointment_time=appointment_time,
        maintenance_type=maintenance_type,
        email=email
    )

    # Assertions to check if the appointment was created correctly
    assert appointment.customer_name == customer_name
    assert appointment.vehicle_type == vehicle_type
    assert appointment.appointment_date.strftime('%Y-%m-%d') == appointment_date
    assert appointment.appointment_time.strftime('%H:%M') == appointment_time
    assert appointment.maintenance_type == maintenance_type
    assert appointment.email == email
    assert appointment.appointment_id is not None  
