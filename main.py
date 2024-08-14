from models.appointment import Appointment
from services.scheduler import Scheduler
from services.utils import display_menu, get_user_input, validate_date, validate_email

def main():
    scheduler = Scheduler("appointments.json")

    while True:
        display_menu()
        choice = get_user_input("Choose an option (1-5): ", valid_options=[str(i) for i in range(1, 6)])

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

            # Fetch appointments for this email
            user_appointments = [appt for appt in scheduler.appointments if appt.email == email]

            if not user_appointments:
                print("No appointments found for this email.")
            else:
                # List all appointments for this email
                print("Here are the appointments associated with this email:")
                for i, appointment in enumerate(user_appointments, 1):
                    print(f"{i}. {appointment}")

                # Ask the user which appointment they want to edit
                appointment_choice = int(get_user_input(f"Enter the number of the appointment you want to edit (1-{len(user_appointments)}): ", valid_options=[str(i) for i in range(1, len(user_appointments) + 1)]))

                selected_appointment = user_appointments[appointment_choice - 1]

                print(f"You have selected: {selected_appointment}")
                confirm_edit = get_user_input("Do you want to edit this appointment? (yes/no): ", valid_options=["yes", "no"])

                if confirm_edit == "yes":
                    # Get new details
                    new_date = get_user_input("Enter new appointment date (YYYY-MM-DD): ", validation_func=validate_date)
                    free_slots = scheduler.list_free_slots(new_date)
                    
                    if free_slots:
                        print("Available time slots (each slot represents 2 hours):")
                        for i, slot in enumerate(free_slots, 1):
                            print(f"{i}. {slot}")
                        
                        slot_choice = int(get_user_input("Choose a time slot by number: ", valid_options=[str(i) for i in range(1, len(free_slots) + 1)]))
                        new_time = free_slots[slot_choice - 1].split(" - ")[0]  
                        
                        new_maintenance_type = get_user_input("Enter new type of maintenance: ")

                        # Edit the appointment in place
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

            # Fetch appointments for this email
            user_appointments = [appt for appt in scheduler.appointments if appt.email == email]

            if not user_appointments:
                print("No appointments found for this email.")
            else:
                # List all appointments for this email
                print("Here are the appointments associated with this email:")
                for i, appointment in enumerate(user_appointments, 1):
                    print(f"{i}. {appointment}")

                # Ask the user which appointment they want to delete
                appointment_choice = int(get_user_input(f"Enter the number of the appointment you want to delete (1-{len(user_appointments)}): ", valid_options=[str(i) for i in range(1, len(user_appointments) + 1)]))

                selected_appointment = user_appointments[appointment_choice - 1]

                # Confirm deletion
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

        elif choice == "5":
            print("Exiting the program.")
            break

if __name__ == "__main__":
    main()