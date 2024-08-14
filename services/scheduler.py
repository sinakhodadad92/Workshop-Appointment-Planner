from datetime import datetime, timedelta
from services.file_handler import FileHandler
from models.appointment import Appointment

class Scheduler:
    def __init__(self, file_path: str, opening_hours=("08:00", "17:00"), lunch_break=("12:00", "13:00")):
        self.file_handler = FileHandler(file_path)
        self.appointments = self.file_handler.load_appointments()
        self.time_slots = [
            ("08:00", "10:00"),
            ("10:00", "12:00"),
            ("13:00", "15:00"),
            ("15:00", "17:00")
        ]
        self.lunch_break = (self._convert_to_time(lunch_break[0]), self._convert_to_time(lunch_break[1]))

    def _convert_to_time(self, time_str: str) -> datetime.time:
        """Convert a time string to a time object."""
        return datetime.strptime(time_str, "%H:%M").time()
    
    def _is_within_opening_hours(self, appointment: Appointment) -> bool:
        """Check if the appointment is within the defined time slots and not during the lunch break."""
        appointment_time_str = appointment.appointment_time.strftime("%H:%M")
        
        for slot_start, slot_end in self.time_slots:
            if slot_start <= appointment_time_str < slot_end:
                return True

        return False
    
    def check_availability(self, new_appointment: Appointment) -> bool:
        """Check if the time slot for the new appointment is already booked."""
        new_appointment_time_str = new_appointment.appointment_time.strftime("%H:%M")
        
        for appointment in self.appointments:
            appointment_time_str = appointment.appointment_time.strftime("%H:%M")
            if (appointment.appointment_date == new_appointment.appointment_date and
                appointment_time_str == new_appointment_time_str):
                return True  
        return False  

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

    def edit_appointment(self, email: str, new_date: str, new_time: str, new_maintenance_type: str) -> bool:
        """Edit an existing appointment by searching with the user's email and updating the date, time, and maintenance type."""
        for appointment in self.appointments:
            if appointment.email == email:
                # Update the appointment date, time, and maintenance type
                appointment.appointment_date = appointment._validate_date(new_date)
                appointment.appointment_time = appointment._validate_time(new_time)
                appointment.maintenance_type = new_maintenance_type

                # Re-check availability if the time was changed
                if not self._is_within_opening_hours(appointment) or self.check_availability(appointment):
                    return False
                
                self.file_handler.save_appointments(self.appointments)  
                return True
        return False
    
    def remove_appointment(self, email: str) -> bool:
        """Remove an appointment by the user's email."""
        for i, appointment in enumerate(self.appointments):
            if appointment.email == email:
                del self.appointments[i]
                self.file_handler.save_appointments(self.appointments)  # Save after removing
                return True
        return False
    
    


    # def list_appointments(self, date: str) -> list:
    #     """List all appointments for a specific day."""
    #     date_obj = Appointment._validate_date(None, date)
    #     return [appointment for appointment in self.appointments if appointment.appointment_date == date_obj]

    def list_free_slots(self, date: str) -> list:
        """List all available time slots for a specific day."""
        date_obj = Appointment._validate_date(None, date)
        free_slots = []

        for slot_start, slot_end in self.time_slots:
            slot_appointments = [
                appt for appt in self.appointments 
                if appt.appointment_date == date_obj and slot_start <= appt.appointment_time.strftime("%H:%M") < slot_end
            ]
            if not slot_appointments:
                free_slots.append(f"{slot_start} - {slot_end}")

        return free_slots
