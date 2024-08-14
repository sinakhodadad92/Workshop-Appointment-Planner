import re
from datetime import datetime
from models.appointment import Appointment

def display_menu():
    print("\nWorkshop Appointment Planner")
    print("1. Add Appointment")
    print("2. Edit Appointment")
    print("3. Delete Appointment")
    print("4. List Free Time Slots")
    print("5. Admin Panel")
    print("6. Exit")
    print("")

def display_admin_menu():
    """Display the admin panel menu."""
    print("\nAdmin Panel")
    print("1. Display all appointments (by day or week)")
    print("2. Display free time slots")
    print("3. Calculate average number of appointments per day")
    print("4. Back to main menu")
    print("")

def get_user_input(prompt, valid_options=None, validation_func=None):
    while True:
        user_input = input(prompt).strip()
        
        if valid_options and user_input not in valid_options:
            print(f"Invalid input. Please choose from {valid_options}.")
            continue
        
        if validation_func:
            try:
                validation_func(user_input)
            except ValueError as e:
                print(f"Invalid input: {e}")
                continue

        return user_input

def validate_date(date_str):
    """Validate the date format YYYY-MM-DD and ensure it is after today."""
    try:
        entered_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        today = datetime.now().date()
        
        if entered_date <= today:
            raise ValueError("The date must be from tomorrow onwards.")
        
    except ValueError as e:
        raise ValueError(f"Invalid date: {e}")
    
def validate_email(email_str):
    """Validate the email format using a regular expression."""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email_str):
        raise ValueError("Invalid email format. Please enter a valid email address.")

def create_appointment(scheduler, email, is_edit=False):
    """Function to create an appointment, can be used for both add and edit functionalities."""
    appointment_date = get_user_input(
        "Enter appointment date (YYYY-MM-DD, must be from tomorrow onwards): ",
        validation_func=validate_date
    )
    free_slots = scheduler.list_free_slots(appointment_date)
    
    if free_slots:
        print("Available time slots (each slot represents 2 hours):")
        for i, slot in enumerate(free_slots, 1):
            print(f"{i}. {slot}")
        
        slot_choice = int(get_user_input("Choose a time slot by number: ", valid_options=[str(i) for i in range(1, len(free_slots) + 1)]))
        appointment_time = free_slots[slot_choice - 1].split(" - ")[0]  
        
        customer_name = get_user_input("Enter customer name: ")
        vehicle_type = get_user_input("Enter vehicle type: ")
        maintenance_type = get_user_input("Enter type of maintenance: ")
        is_emergency = get_user_input("Is this an emergency? (yes/no): ", valid_options=["yes", "no"]) == "yes"

        # Create a new appointment with the updated details
        new_appointment = Appointment(customer_name, vehicle_type, appointment_date, appointment_time, maintenance_type, is_emergency, email)
        
        if scheduler.add_appointment(new_appointment):
            if is_edit:
                print("Appointment updated successfully.")
            else:
                print("Appointment added successfully.")
        else:
            print("Failed to process appointment. The time slot may be unavailable.")
    else:
        print("No available time slots for this date. Please try a different date.")


def calculate_average_appointments(start_date_str: str, end_date_str: str, appointments: list) -> float:
    """Calculate the average number of appointments per day over a given period."""
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

    if start_date > end_date:
        raise ValueError("The start date must be before or the same as the end date.")
    
    num_days = (end_date - start_date).days + 1
    num_appointments = sum(1 for appt in appointments if start_date <= appt.appointment_date <= end_date)
    
    return num_appointments / num_days if num_days > 0 else 0.0