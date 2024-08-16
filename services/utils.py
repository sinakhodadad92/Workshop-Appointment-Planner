import re
from datetime import datetime, timedelta
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
    print("\nAdmin Panel")
    print("1. Display All Appointments")
    print("2. Display Free Time Slots")
    print("3. Calculate Average Appointments")
    print("4. Send Reminders")
    print("5. Back to Main Menu")
    print("")

def get_user_input(prompt, valid_options=None, validation_func=None):
    """
    Continuously prompt the user for input until valid input is provided.

    Args:
        prompt (str): The message to display when asking for input.
        valid_options (list, optional): A list of valid options. If provided, input must match one of these options.
        validation_func (function, optional): A function to validate the input. Should raise ValueError if validation fails.

    Returns:
        str: The valid input provided by the user.
    """
    while True:
        # Ask the user for input
        user_input = input(prompt).strip()
        
        # If valid options are provided, check if the input is among them
        if valid_options and user_input not in valid_options:
            print(f"Invalid input. Please choose from {valid_options}.")
            continue
        
        # If a validation function is provided, use it to validate the input
        if validation_func:
            try:
                validation_func(user_input)
            except ValueError as e:
                # If validation fails, inform the user and prompt again
                print(f"Invalid input: {e}")
                continue

        # If input passes all checks, return it
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
    """
    Calculate the average number of appointments per day over a given period.

    Args:
        start_date_str (str): The start date of the period (format: YYYY-MM-DD).
        end_date_str (str): The end date of the period (format: YYYY-MM-DD).
        appointments (list): A list of Appointment objects to calculate the average from.

    Returns:
        float: The average number of appointments per day during the specified period.

    Raises:
        ValueError: If the start date is after the end date.
    """
    # Convert the start and end date strings to date objects
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    
    # Ensure the start date is not after the end date
    if start_date > end_date:
        raise ValueError("The start date must be before or the same as the end date.")
    
    # Calculate the total number of days in the period
    num_days = (end_date - start_date).days + 1
    print(f'This is num_days {num_days}')

    num_slots = num_days * 4
    
    # Count the number of appointments that fall within the date range
    num_appointments = sum(1 for appt in appointments if start_date <= appt.appointment_date <= end_date)
    print(f'This is num_appointments {num_appointments}')
    
    # Calculate and return the average number of appointments per day
    return num_appointments / num_slots if num_days > 0 else 0.0

def list_emails_for_date(self, date: str) -> list:
    """
    List all emails associated with appointments for a specific date.

    Args:
        date (str): The date for which to list emails (format: YYYY-MM-DD).

    Returns:
        list: A list of tuples containing the email and appointment details.
    """
    date_obj = Appointment._validate_date(None, date)
    emails = [(appt.email, appt) for appt in self.appointments if appt.appointment_date == date_obj and appt.email]
    return emails
