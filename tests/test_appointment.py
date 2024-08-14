import pytest
from datetime import datetime
from models.appointment import Appointment

# Test Scenario 1: Test Appointment Creation with Valid Data
def test_appointment_creation_with_valid_data():
    customer_name = "John Doe"
    vehicle_type = "Sedan"
    appointment_date = "2024-09-30"
    appointment_time = "10:00"
    maintenance_type = "Oil Change"
    email = "john.doe@example.com"
    
    appointment = Appointment(customer_name, vehicle_type, appointment_date, appointment_time, maintenance_type, email=email)
    
    assert appointment.customer_name == customer_name
    assert appointment.vehicle_type == vehicle_type
    assert appointment.appointment_date == datetime.strptime(appointment_date, "%Y-%m-%d").date()
    assert appointment.appointment_time == datetime.strptime(appointment_time, "%H:%M").time()
    assert appointment.maintenance_type == maintenance_type
    assert appointment.email == email
    assert isinstance(appointment.appointment_id, str)

# Test Scenario 2: Test Appointment Creation with Invalid Date Format
def test_appointment_creation_with_invalid_date_format():
    with pytest.raises(ValueError, match="Invalid date format"):
        Appointment("John Doe", "Sedan", "09-30-2024", "10:00", "Oil Change")

# Test Scenario 3: Test Appointment Creation with Invalid Date (Today or Past Date)
def test_appointment_creation_with_invalid_date():
    today = datetime.now().strftime("%Y-%m-%d")
    past_date = "2023-09-30"
    
    # Test with today's date
    with pytest.raises(ValueError, match="The date must be from tomorrow onwards"):
        Appointment("John Doe", "Sedan", today, "10:00", "Oil Change")
    
    # Test with a past date
    with pytest.raises(ValueError, match="The date must be from tomorrow onwards"):
        Appointment("John Doe", "Sedan", past_date, "10:00", "Oil Change")


# Test Scenario 4: Test Appointment Creation with Invalid Time Format
def test_appointment_creation_with_invalid_time_format():
    with pytest.raises(ValueError, match="Invalid time format"):
        Appointment("John Doe", "Sedan", "2024-09-30", "10am", "Oil Change")

# Test Scenario 5: Test Equality of Two Appointments with Same ID
def test_equality_of_two_appointments_with_same_id():
    appointment1 = Appointment("John Doe", "Sedan", "2024-09-30", "10:00", "Oil Change")
    appointment2 = Appointment("Jane Doe", "SUV", "2024-09-30", "10:00", "Brake Check")
    
    appointment2.appointment_id = appointment1.appointment_id
    
    assert appointment1 == appointment2

# Test Scenario 6: Test Inequality of Two Appointments with Different IDs
def test_inequality_of_two_appointments_with_different_ids():
    appointment1 = Appointment("John Doe", "Sedan", "2024-09-30", "10:00", "Oil Change")
    appointment2 = Appointment("Jane Doe", "SUV", "2024-09-30", "10:00", "Brake Check")
    
    assert appointment1 != appointment2

# Test Scenario 7: Test Appointment String Representation
def test_appointment_string_representation():
    appointment = Appointment("John Doe", "Sedan", "2024-09-30", "10:00", "Oil Change", email="john.doe@example.com")
    expected_str = "Appointment(John Doe, Sedan, 2024-09-30, 10:00:00, Oil Change, Emergency: False, Email: john.doe@example.com)"
    
    assert str(appointment) == expected_str

# Test Scenario 8: Test Appointment Sorting by Date and Time
def test_appointment_sorting_by_date_and_time():
    appointment1 = Appointment("John Doe", "Sedan", "2024-09-30", "10:00", "Oil Change")
    appointment2 = Appointment("Jane Doe", "SUV", "2024-09-30", "08:00", "Brake Check")
    
    appointments = [appointment1, appointment2]
    appointments.sort()
    
    assert appointments == [appointment2, appointment1]  # Sorted by time

# Test Scenario 9: Test Emergency Appointment Flag Setting
def test_emergency_appointment_flag_setting():
    appointment = Appointment("John Doe", "Sedan", "2024-09-30", "10:00", "Oil Change", is_emergency=True)
    
    assert appointment.is_emergency is True

# Test Scenario 10: Test Appointment Creation with Email
def test_appointment_creation_with_email():
    email = "john.doe@example.com"
    appointment = Appointment("John Doe", "Sedan", "2024-09-30", "10:00", "Oil Change", email=email)
    
    assert appointment.email == email
