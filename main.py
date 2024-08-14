from models.appointment import Appointment
from services.scheduler import Scheduler
from datetime import datetime

def display_menu():
    print("\nWorkshop Appointment Planner")
    print("1. Add Appointment")
    print("2. View Appointments")
    print("3. Edit Appointment")
    print("4. Delete Appointment")
    print("5. List Free Time Slots")
    print("6. Send Reminders")
    print("7. View Statistics")
    print("8. Exit")
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

def main():
    scheduler = Scheduler("appointments.json")

    while True:
        display_menu()
        choice = get_user_input("Choose an option (1-8): ", valid_options=[str(i) for i in range(1, 9)])

        if choice == "1":
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
                appointment_time = free_slots[slot_choice - 1].split(" - ")[0]  # Use the start time of the selected slot
                
                customer_name = get_user_input("Enter customer name: ")
                vehicle_type = get_user_input("Enter vehicle type: ")
                maintenance_type = get_user_input("Enter type of maintenance: ")
                email = get_user_input("Enter your email address (optional, for reminders): ")
                is_emergency = get_user_input("Is this an emergency? (yes/no): ", valid_options=["yes", "no"]) == "yes"

                appointment = Appointment(customer_name, vehicle_type, appointment_date, appointment_time, maintenance_type, is_emergency, email)
                if scheduler.add_appointment(appointment):
                    print("Appointment added successfully.")
                else:
                    print("Failed to add appointment. Time slot may be unavailable.")
            else:
                print("No available time slots for this date.")
        

        elif choice == "2":
            date = get_user_input("Enter date to view appointments (YYYY-MM-DD): ", validation_func=validate_date)
            appointments = scheduler.list_appointments(date)
            if appointments:
                for appt in appointments:
                    print(appt)
            else:
                print("No appointments found.")


        elif choice == "3":
            appointment_id = get_user_input("Enter appointment ID to edit: ")
            customer_name = get_user_input("Enter new customer name (leave blank to keep current): ")
            vehicle_type = get_user_input("Enter new vehicle type (leave blank to keep current): ")
            appointment_date = get_user_input("Enter new appointment date (YYYY-MM-DD, leave blank to keep current): ")
            appointment_time = get_user_input("Enter new appointment time (HH:MM, leave blank to keep current): ")
            maintenance_type = get_user_input("Enter new type of maintenance (leave blank to keep current): ")

            updates = {}
            if customer_name:
                updates['customer_name'] = customer_name
            if vehicle_type:
                updates['vehicle_type'] = vehicle_type
            if appointment_date:
                updates['appointment_date'] = appointment_date
            if appointment_time:
                updates['appointment_time'] = appointment_time
            if maintenance_type:
                updates['maintenance_type'] = maintenance_type

            if scheduler.edit_appointment(appointment_id, **updates):
                print("Appointment updated successfully.")
            else:
                print("Failed to update appointment. Please check the details and try again.")

        elif choice == "4":
            appointment_id = get_user_input("Enter appointment ID to delete: ")
            if scheduler.remove_appointment(appointment_id):
                print("Appointment deleted successfully.")
            else:
                print("Failed to delete appointment. Please check the ID and try again.")

        elif choice == "5":
            date = get_user_input("Enter date to list free slots (YYYY-MM-DD): ")
            free_slots = scheduler.list_free_slots(date)
            if free_slots:
                print("Available time slots:")
                for slot in free_slots:
                    print(slot)
            else:
                print("No free time slots available.")

        elif choice == "6":
            reminders = scheduler.send_reminders()
            if reminders:
                print("Reminders:")
                for reminder in reminders:
                    print(reminder)
            else:
                print("No reminders to send.")

        elif choice == "7":
            stats = scheduler.calculate_statistics()
            print("Statistics:")
            print(f"Average appointments per day: {stats['average_appointments_per_day']}")
            print(f"Total days with appointments: {stats['total_days_with_appointments']}")
            print(f"Total appointments: {stats['total_appointments']}")

        elif choice == "8":
            print("Exiting the program.")
            break

if __name__ == "__main__":
    main()
