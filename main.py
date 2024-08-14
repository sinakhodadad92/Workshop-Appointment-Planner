from models.appointment import Appointment
from services.scheduler import Scheduler
from services.utils import display_admin_menu, display_menu, get_user_input, validate_date, validate_email, calculate_average_appointments
from datetime import datetime, timedelta

ADMIN_PASSWORD = "adminpassword"

def main():
    scheduler = Scheduler("appointments.json")

    while True:
        display_menu()
        choice = get_user_input("Choose an option (1-6): ", valid_options=[str(i) for i in range(1, 7)])

        if choice == "1":
            # Add Appointment logic
            email = get_user_input("Enter your email address: ", validation_func=validate_email)
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

                appointment = Appointment(customer_name, vehicle_type, appointment_date, appointment_time, maintenance_type, is_emergency, email)
                if scheduler.add_appointment(appointment):
                    print("Appointment added successfully.")
                else:
                    print("Failed to add appointment. Time slot may be unavailable.")
        
        elif choice == "2":  # Edit Appointment
            email = get_user_input("Enter the email associated with the appointment to edit: ", validation_func=validate_email)

            user_appointments = [appt for appt in scheduler.appointments if appt.email == email]

            if not user_appointments:
                print("No appointments found for this email.")
            else:
                print("Here are the appointments associated with this email:")
                for i, appointment in enumerate(user_appointments, 1):
                    print(f"{i}. {appointment}")

                appointment_choice = int(get_user_input(f"Enter the number of the appointment you want to edit (1-{len(user_appointments)}): ", valid_options=[str(i) for i in range(1, len(user_appointments) + 1)]))

                selected_appointment = user_appointments[appointment_choice - 1]

                print(f"You have selected: {selected_appointment}")
                confirm_edit = get_user_input("Do you want to edit this appointment? (yes/no): ", valid_options=["yes", "no"])

                if confirm_edit == "yes":
                    new_date = get_user_input("Enter new appointment date (YYYY-MM-DD): ", validation_func=validate_date)
                    free_slots = scheduler.list_free_slots(new_date)
                    
                    if free_slots:
                        print("Available time slots (each slot represents 2 hours):")
                        for i, slot in enumerate(free_slots, 1):
                            print(f"{i}. {slot}")
                        
                        slot_choice = int(get_user_input("Choose a time slot by number: ", valid_options=[str(i) for i in range(1, len(free_slots) + 1)]))
                        new_time = free_slots[slot_choice - 1].split(" - ")[0]  
                        
                        new_maintenance_type = get_user_input("Enter new type of maintenance: ")

                        if scheduler.edit_appointment_in_place(selected_appointment, new_date, new_time, new_maintenance_type):
                            print("Appointment updated successfully.")
                        else:
                            print("Failed to update appointment. The time slot may be unavailable.")
                    else:
                        print("No available time slots for this date. Please try a different date.")
                else:
                    print("Edit operation cancelled.")

        elif choice == "3":  # Delete Appointment
            email = get_user_input("Enter the email associated with the appointment to delete: ", validation_func=validate_email)

            user_appointments = [appt for appt in scheduler.appointments if appt.email == email]

            if not user_appointments:
                print("No appointments found for this email.")
            else:
                print("Here are the appointments associated with this email:")
                for i, appointment in enumerate(user_appointments, 1):
                    print(f"{i}. {appointment}")

                appointment_choice = int(get_user_input(f"Enter the number of the appointment you want to delete (1-{len(user_appointments)}): ", valid_options=[str(i) for i in range(1, len(user_appointments) + 1)]))

                selected_appointment = user_appointments[appointment_choice - 1]

                confirm_delete = get_user_input(f"Are you sure you want to delete the appointment: {selected_appointment}? (yes/no): ", valid_options=["yes", "no"])

                if confirm_delete == "yes":
                    if scheduler.remove_appointment(selected_appointment.email):
                        print(f"Appointment associated with {selected_appointment.email} deleted successfully.")
                    else:
                        print(f"Failed to delete appointment. The appointment may have already been removed.")
                else:
                    print("Deletion operation cancelled.")

        elif choice == "4":
            date = get_user_input("Enter date to list free slots (YYYY-MM-DD): ")
            free_slots = scheduler.list_free_slots(date)
            if free_slots:
                print("Available time slots:")
                for slot in free_slots:
                    print(slot)
            else:
                print("No free time slots available.")

        elif choice == "5":  # Admin Panel
            admin_password = get_user_input("Enter admin password: ")
            if admin_password == ADMIN_PASSWORD:
                while True:
                    display_admin_menu()
                    admin_choice = get_user_input("Choose an option (1-4): ", valid_options=["1", "2", "3", "4"])

                    if admin_choice == "1":  # Display all appointments
                        date_or_week = get_user_input("Enter 'day' or 'week' to view appointments: ", valid_options=["day", "week"])
                        if date_or_week == "day":
                            date = get_user_input("Enter date (YYYY-MM-DD) to view appointments: ", validation_func=validate_date)
                            appointments = scheduler.list_appointments(date)
                        else:
                            start_date = get_user_input("Enter start date (YYYY-MM-DD) of the week: ", validation_func=validate_date)
                            appointments = []
                            for i in range(7):
                                day = datetime.strptime(start_date, "%Y-%m-%d").date() + timedelta(days=i)
                                appointments.extend(scheduler.list_appointments(day.strftime("%Y-%m-%d")))
                        
                        if appointments:
                            for appt in appointments:
                                print(appt)
                        else:
                            print("No appointments found.")

                    elif admin_choice == "2":  # Display free time slots
                        date = get_user_input("Enter date (YYYY-MM-DD) to view free slots: ", validation_func=validate_date)
                        free_slots = scheduler.list_free_slots(date)
                        if free_slots:
                            print("Available time slots:")
                            for slot in free_slots:
                                print(slot)
                        else:
                            print("No free time slots available.")

                    elif admin_choice == "3":  # Calculate average number of appointments per day
                        start_date = get_user_input("Enter the start date (YYYY-MM-DD): ", validation_func=validate_date)
                        end_date = get_user_input("Enter the end date (YYYY-MM-DD): ", validation_func=validate_date)
                        
                        try:
                            average = calculate_average_appointments(start_date, end_date, scheduler.appointments)
                            print(f"Average number of appointments per day from {start_date} to {end_date}: {average:.2f}")
                        except ValueError as e:
                            print(f"Error: {e}")
                    
                    elif admin_choice == "4":  # Back to main menu
                        break
            else:
                print("Incorrect admin password. Access denied.")

        elif choice == "6":
            print("Exiting the program.")
            break

if __name__ == "__main__":
    main()