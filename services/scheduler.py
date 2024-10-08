from datetime import datetime, timedelta
from services.file_handler import FileHandler
from models.appointment import Appointment
import smtplib
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Scheduler:
    def __init__(self, file_path: str, opening_hours=("08:00", "17:00"), lunch_break=("12:00", "13:00")):
        
        # Initialize the file handler
        self.file_handler = FileHandler(file_path)
        
        # Load existing appointments from the file
        self.appointments = self.file_handler.load_appointments()
        
        self.time_slots = [
            ("08:00", "10:00"),
            ("10:00", "12:00"),
            ("13:00", "15:00"),
            ("15:00", "17:00")
        ]
        
        # Convert lunch break times to time objects
        self.lunch_break = (self._convert_to_time(lunch_break[0]), self._convert_to_time(lunch_break[1]))

    def _convert_to_time(self, time_str: str) -> datetime.time:
        """Convert a time string to a time object."""
        return datetime.strptime(time_str, "%H:%M").time()
    
    def _is_within_opening_hours(self, appointment: Appointment) -> bool:
        """Check if the appointment is within the defined time slots and not during the lunch break."""
        
        # Convert appointment time to a string in "HH:MM" format
        appointment_time_str = appointment.appointment_time.strftime("%H:%M")
        
        # Loop through defined time slots to check if the appointment time fits
        for slot_start, slot_end in self.time_slots:
            if slot_start <= appointment_time_str < slot_end:
                return True

        return False
    
    def check_availability(self, new_appointment: Appointment) -> bool:
        """Check if the time slot for the new appointment is already booked, excluding the current appointment being edited."""
        
        # Loop through all existing appointments
        for appointment in self.appointments:
            # Check if another appointment exists at the same date and time, excluding the current one being edited
            if (appointment.appointment_date == new_appointment.appointment_date and
                appointment.appointment_time == new_appointment.appointment_time and
                appointment.appointment_id != new_appointment.appointment_id):  
                return True  # The time slot is already booked
        
        return False  # The time slot is available
    
    

    def add_appointment(self, appointment: Appointment) -> bool:
        """Add an appointment if the time slot is available and within working hours."""
        if self._is_within_opening_hours(appointment) and not self.check_availability(appointment):
            self.appointments.append(appointment)
            self.appointments.sort()
            self.file_handler.save_appointments(self.appointments)  # Save after adding

            # Send confirmation email
            if appointment.email:
                subject = "Appointment Confirmation"
                body = (f"Dear {appointment.customer_name},\n\n"
                        f"Your appointment has been successfully scheduled for {appointment.appointment_date} at {appointment.appointment_time}.\n"
                        f"Type of Maintenance: {appointment.maintenance_type}\n\n"
                        "We look forward to serving you.\n\nBest regards,\nAutoSchmiede")
                # self.send_email(appointment.email, subject, body)

            return True
        return False
    
    def edit_appointment_in_place(self, appointment: Appointment, new_date: str, new_time: str, new_maintenance_type: str):
        """Edit an existing appointment in place."""
        # Validate and update the date and time
        appointment.appointment_date = appointment._validate_date(new_date)
        appointment.appointment_time = appointment._validate_time(new_time)
        appointment.maintenance_type = new_maintenance_type

        # Check availability for the new date and time
        if not self._is_within_opening_hours(appointment) or self.check_availability(appointment):
            print("Failed to update appointment. The time slot may be unavailable.")
            return False
        
        self.file_handler.save_appointments(self.appointments)  # Save after editing
        return True
    
    def remove_appointment(self, email: str) -> bool:
        """Remove an appointment by the user's email."""
        found = False  # Flag to check if an appointment was found and removed
        
        # Iterate over the appointments list to find and remove the matching appointment
        for i, appointment in enumerate(self.appointments):
            if appointment.email == email:
                del self.appointments[i]
                found = True
                break  # Exit the loop once the appointment is found and removed

        if found:
            self.file_handler.save_appointments(self.appointments)  # Save after removing
            return True
        else:
            return False  # Return False if no appointment was found with the given email
    

    def list_appointments(self, date: str) -> list:
        """List all appointments for a specific day."""
        date_obj = Appointment._validate_date(None, date)
        return [appointment for appointment in self.appointments if appointment.appointment_date == date_obj]

    def list_free_slots(self, date: str) -> list:
        """
        List all available time slots for a specific day.

        Args:
            date (str): The date for which to check the available time slots (format: YYYY-MM-DD).

        Returns:
            list: A list of strings, where each string represents a free time slot (e.g., "08:00 - 10:00").
        """
        # Convert the provided date string to a date object
        date_obj = Appointment._validate_date(None, date)
        
        # Initialize a list to hold the free time slots
        free_slots = []

        # Check each time slot to see if it is free
        for slot_start, slot_end in self.time_slots:
            # Find any appointments that fall within the current time slot
            slot_appointments = [
                appt for appt in self.appointments 
                if appt.appointment_date == date_obj and slot_start <= appt.appointment_time.strftime("%H:%M") < slot_end
            ]
            # If no appointments are found, the slot is free
            if not slot_appointments:
                free_slots.append(f"{slot_start} - {slot_end}")

        return free_slots

    
    def list_all_slots_with_status(self, date: str) -> list:
        """
        List all time slots for a specific day, indicating whether each slot is 'free' or 'booked'.

        Args:
            date (str): The date for which to check the time slots (format: YYYY-MM-DD).

        Returns:
            list: A list of tuples, where each tuple contains the time slot (e.g., "08:00 - 10:00") 
                and its status ('free' or 'booked').
        """
        # Convert the provided date string to a date object
        date_obj = Appointment._validate_date(None, date)
        
        # Initialize a list to hold the status of all time slots
        all_slots_with_status = []

        # Check each time slot for availability
        for slot_start, slot_end in self.time_slots:
            slot_status = 'free'  # Assume the slot is free by default

            # Check if the current slot is booked
            for appt in self.appointments:
                if appt.appointment_date == date_obj and appt.appointment_time.strftime("%H:%M") == slot_start:
                    slot_status = 'booked'  # Mark the slot as booked
                    break
            
            # Add the slot and its status to the list
            all_slots_with_status.append((f"{slot_start} - {slot_end}", slot_status))

        return all_slots_with_status
    
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

    
    def send_reminder_email(self, appointment: Appointment):
        """
        Send a reminder email for an appointment using the pre-configured sender email.

        Args:
            appointment (Appointment): The appointment for which to send a reminder.
        """
        sender_email = "sinamd443@gmail.com"
        receiver_email = appointment.email
        subject = "Appointment Reminder"
        message = (f"Dear {appointment.customer_name},\n\n"
                f"This is a reminder for your upcoming appointment on {appointment.appointment_date} at {appointment.appointment_time}.\n\n"
                "Best regards,\nAutoSchmiede")

        # Prepare the email text
        email_text = f"Subject: {subject}\n\n{message}"

        # Get the password from the environment variable
        email_password = os.getenv("EMAIL_PASSWORD")


        try:
            # Set up the SMTP server connection
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, email_password)  
            server.sendmail(sender_email, receiver_email, email_text)
            print(f"Reminder sent to {receiver_email}.")
        except Exception as e:
            print(f"Failed to send email to {receiver_email}: {e}")

    
    def shift_appointment(self, date: str, current_slot: str) -> str:
        """
        Shift a booked appointment to the next available time slot.
        If no slots are available later on the same day, shift to the first available slot on subsequent days.

        Returns:
            A string representing the new appointment time and date (e.g., "09:00 on 2023-08-15") if successful,
            or None if shifting failed.
        """
        # Parse the provided date and time
        appointment_date = datetime.strptime(date, "%Y-%m-%d").date()
        current_start_time_str = current_slot.split(" - ")[0]
        current_start_time = datetime.strptime(current_start_time_str, "%H:%M").time()

        # Identify the appointment to be shifted
        for appointment in self.appointments:
            if (appointment.appointment_date == appointment_date and
                appointment.appointment_time == current_start_time):
                
                # First, attempt to find a later slot on the same day
                for slot_start_str, _ in self.time_slots:
                    slot_start_time = datetime.strptime(slot_start_str, "%H:%M").time()
                    
                    if slot_start_time > current_start_time:
                        # Check if this slot is free
                        if not any(a.appointment_date == appointment_date and a.appointment_time == slot_start_time
                                for a in self.appointments):
                            # Update the appointment to the new time
                            appointment.appointment_time = slot_start_time
                            self.file_handler.save_appointments(self.appointments)
                            return f"{slot_start_str} on {appointment_date.strftime('%Y-%m-%d')}"
                
                # If no later slots are free on the same day, move to the next day
                next_day = appointment_date + timedelta(days=1)
                while True:
                    # Check each slot on the next day
                    for slot_start_str, _ in self.time_slots:
                        slot_start_time = datetime.strptime(slot_start_str, "%H:%M").time()
                        
                        if not any(a.appointment_date == next_day and a.appointment_time == slot_start_time
                                for a in self.appointments):
                            # Update the appointment to the new date and time
                            appointment.appointment_date = next_day
                            appointment.appointment_time = slot_start_time
                            self.file_handler.save_appointments(self.appointments)
                            return f"{slot_start_str} on {next_day.strftime('%Y-%m-%d')}"
                    
                    # Move to the next day
                    next_day += timedelta(days=1)
        
        # If the appointment to be shifted was not found or no slots are available
        return None
    




