import smtplib
from datetime import datetime, timedelta
from services.file_handler import FileHandler
from models.appointment import Appointment
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

    def add_appointment(self, appointment: Appointment) -> bool:
        """Add an appointment if the time slot is available and within working hours."""
        if self._is_within_opening_hours(appointment) and not self.check_availability(appointment):
            self.appointments.append(appointment)
            self.appointments.sort()
            self.file_handler.save_appointments(self.appointments)  # Save after adding
            return True
        return False

    def _is_within_opening_hours(self, appointment: Appointment) -> bool:
        """Check if the appointment is within the defined time slots and not during the lunch break."""
        for slot_start, slot_end in self.time_slots:
            if slot_start <= appointment.appointment_time.strftime("%H:%M") < slot_end:
                return True
        return False

    def check_availability(self, new_appointment: Appointment) -> bool:
        """Check if the time slot for the new appointment is already booked."""
        for slot_start, slot_end in self.time_slots:
            if slot_start <= new_appointment.appointment_time.strftime("%H:%M") < slot_end:
                for appointment in self.appointments:
                    if (appointment.appointment_date == new_appointment.appointment_date and
                        slot_start <= appointment.appointment_time.strftime("%H:%M") < slot_end):
                        return True
        return False

    def remove_appointment(self, appointment_id: str) -> bool:
        """Remove an appointment by its ID."""
        for i, appointment in enumerate(self.appointments):
            if appointment.appointment_id == appointment_id:
                del self.appointments[i]
                self.file_handler.save_appointments(self.appointments)  # Save after removing
                return True
        return False
    
    def send_email(self, to_email, subject, body):
        """Send an email to the specified address."""
        from_email = "sinamd443@gmail.com"  
        password = "Faeze1372<>"  

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_email, password)
            text = msg.as_string()
            server.sendmail(from_email, to_email, text)
            server.quit()
            print(f"Confirmation email sent to {to_email}")
        except Exception as e:
            print(f"Failed to send email to {to_email}: {e}")

    def add_appointment(self, appointment: Appointment) -> bool:
        """Add an appointment if the time slot is available and within working hours."""
        if self._is_within_opening_hours(appointment) and not self.check_availability(appointment):
            self.appointments.append(appointment)
            self.appointments.sort()
            self.file_handler.save_appointments(self.appointments)  

            # Send confirmation email
            if appointment.email:
                subject = "Appointment Confirmation"
                body = (f"Dear {appointment.customer_name},\n\n"
                        f"Your appointment has been successfully scheduled for {appointment.appointment_date} at {appointment.appointment_time}.\n"
                        f"Type of Maintenance: {appointment.maintenance_type}\n\n"
                        "We look forward to serving you.\n\nBest regards,\nAutoSchmiede")
                self.send_email(appointment.email, subject, body)

            return True
        return False

    def send_reminders(self, hours_before=24):
        """Generate and send reminders for upcoming appointments."""
        now = datetime.now()
        reminder_time = now + timedelta(hours=hours_before)
        reminders = []
        
        for appointment in self.appointments:
            appointment_datetime = datetime.combine(appointment.appointment_date, appointment.appointment_time)
            if now <= appointment_datetime <= reminder_time and appointment.email:
                subject = "Appointment Reminder"
                body = f"Dear {appointment.customer_name},\n\nThis is a reminder for your upcoming appointment on {appointment.appointment_date} at {appointment.appointment_time}.\n\nBest regards,\nAutoSchmiede"
                self.send_email(appointment.email, subject, body)
                reminders.append(f"Reminder sent to {appointment.email} for {appointment.customer_name}'s appointment on {appointment.appointment_date} at {appointment.appointment_time}.")
        
        return reminders

    def edit_appointment(self, appointment_id: str, **kwargs) -> bool:
        """Edit an existing appointment."""
        for appointment in self.appointments:
            if appointment.appointment_id == appointment_id:
                if 'customer_name' in kwargs:
                    appointment.customer_name = kwargs['customer_name']
                if 'vehicle_type' in kwargs:
                    appointment.vehicle_type = kwargs['vehicle_type']
                if 'appointment_date' in kwargs:
                    appointment.appointment_date = appointment._validate_date(kwargs['appointment_date'])
                if 'appointment_time' in kwargs:
                    appointment.appointment_time = appointment._validate_time(kwargs['appointment_time'])
                if 'maintenance_type' in kwargs:
                    appointment.maintenance_type = kwargs['maintenance_type']

                if 'appointment_date' in kwargs or 'appointment_time' in kwargs:
                    if not self._is_within_opening_hours(appointment) or self.check_availability(appointment):
                        return False
                self.file_handler.save_appointments(self.appointments)  
                return True
        return False

    def list_appointments(self, date: str) -> list:
        """List all appointments for a specific day."""
        date_obj = Appointment._validate_date(None, date)
        return [appointment for appointment in self.appointments if appointment.appointment_date == date_obj]

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
