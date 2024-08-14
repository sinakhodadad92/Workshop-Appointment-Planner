from models.appointment import Appointment
from services.scheduler import Scheduler
from services.utils import display_menu, get_user_input, validate_date, validate_email, create_appointment

def main():
    scheduler = Scheduler("appointments.json")

    while True:
        display_menu()
        choice = get_user_input("Choose an option (1-5): ", valid_options=[str(i) for i in range(1, 6)])
        if choice == "1":
            # Add Appointment logic using create_appointment function
            email = get_user_input("Enter your email address: ", validation_func=validate_email)
            create_appointment(scheduler, email)

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
                confirm_edit = get_user_input("Do you want to edit this appointment? (yes/no): Proceeding with yes will delete your current appointment. ", valid_options=["yes", "no"])

                if confirm_edit == "yes":
                    # Remove the old appointment
                    scheduler.remove_appointment(selected_appointment.email)

                    # Now proceed to add a new appointment using the create_appointment function
                    print("Your previous appointment deleted. Please enter the new details for the appointment:")
                    create_appointment(scheduler, email, is_edit=True)
                else:
                    print("Edit operation cancelled.")

        elif choice == "3":  # Delete Appointment
            email = get_user_input("Enter the email associated with the appointment to delete: ", validation_func=validate_email)

            if scheduler.remove_appointment(email):
                print(f"Appointment associated with {email} deleted successfully.")
            else:
                print(f"Failed to delete appointment. No appointment found with the email {email}.")

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
