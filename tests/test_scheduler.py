import pytest
from datetime import datetime
from models.appointment import Appointment
from services.scheduler import Scheduler

# Assuming a mock file path for testing
file_path = "test_appointments.json"

@pytest.fixture
def scheduler():
    """Fixture to initialize the Scheduler."""
    return Scheduler(file_path)

# Test 1: Adding an Appointment Outside Opening Hours
def test_adding_appointment_outside_opening_hours(scheduler):
    appointment = Appointment("John Doe", "Sedan", "2024-09-30", "18:00", "Oil Change", email="john.doe@example.com")
    assert scheduler.add_appointment(appointment) is False

# Test 2: Adding an Appointment During Lunch Break
def test_adding_appointment_during_lunch_break(scheduler):
    appointment = Appointment("John Doe", "Sedan", "2024-09-30", "12:30", "Oil Change", email="john.doe@example.com")
    assert scheduler.add_appointment(appointment) is False

# Test 3: Adding an Appointment in an Already Booked Time Slot
def test_adding_appointment_in_booked_slot(scheduler):
    appointment1 = Appointment("John Doe", "Sedan", "2024-09-30", "10:00", "Oil Change", email="john.doe@example.com")
    appointment2 = Appointment("Jane Doe", "SUV", "2024-09-30", "10:00", "Brake Check", email="jane.doe@example.com")
    scheduler.add_appointment(appointment1)
    assert scheduler.add_appointment(appointment2) is False

# Test 4: Removing a Non-Existing Appointment by Email
def test_removing_non_existing_appointment_by_email(scheduler):
    # This email should not exist in the appointments
    assert scheduler.remove_appointment("non-existent-email@example.com") is False

# Test 5: Editing an Appointment's Date and Time to a Free Slot
def test_editing_appointment_date_time_to_free_slot(scheduler):
    appointment = scheduler.appointments[0]  # Get the first appointment for testing
    result = scheduler.edit_appointment_in_place(appointment, "2024-09-30", "08:00", "Brake Check")
    assert result is True
    assert scheduler.appointments[0].appointment_time.strftime("%H:%M") == "08:00"
    assert scheduler.appointments[0].maintenance_type == "Brake Check"

# Test 6: Editing an Appointment's Date and Time to a Booked Slot
def test_editing_appointment_date_time_to_booked_slot(scheduler):
    appointment1 = Appointment("John Doe", "Sedan", "2024-09-30", "08:00", "Oil Change", email="john.doe@example.com")
    scheduler.add_appointment(appointment1)
    result = scheduler.edit_appointment_in_place(appointment1, "2024-09-30", "10:00", "Tire Rotation")
    assert result is False


# Test 7: Listing Free Time Slots for a Date
def test_listing_free_time_slots_for_date(scheduler):
    free_slots = scheduler.list_free_slots("2024-09-30")
    assert "10:00 - 12:00" not in free_slots  # Assuming "10:00 - 12:00" is booked

# Test 8: Listing Free Time Slots Excluding Lunch and Reserved Times
def test_listing_free_time_slots_excluding_lunch_reserved_times(scheduler):
    appointment = Appointment("John Doe", "Sedan", "2024-09-30", "12:30", "Oil Change", email="john.doe@example.com")
    scheduler.add_appointment(appointment)
    free_slots = scheduler.list_free_slots("2024-09-30")
    assert "12:00 - 13:00" not in free_slots
