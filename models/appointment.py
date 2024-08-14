import uuid
from datetime import datetime

class Appointment:
    def __init__(self, customer_name: str, vehicle_type: str, appointment_date: str, appointment_time: str, maintenance_type: str, is_emergency: bool = False, email: str = None):
        self.customer_name = customer_name
        self.vehicle_type = vehicle_type
        self.appointment_date = self._validate_date(appointment_date)
        self.appointment_time = self._validate_time(appointment_time)
        self.maintenance_type = maintenance_type
        self.appointment_id = str(uuid.uuid4())  
        self.is_emergency = is_emergency  
        self.email = email  

    def _validate_date(self, date_str: str) -> datetime.date:
        """Validate and convert the date string to a date object."""
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

    def _validate_time(self, time_str: str) -> datetime.time:
        """Validate and convert the time string to a time object."""
        try:
            return datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            raise ValueError("Invalid time format. Please use HH:MM.")

    def __str__(self):
        return (f"Appointment({self.customer_name}, {self.vehicle_type}, "
                f"{self.appointment_date}, {self.appointment_time}, {self.maintenance_type}, "
                f"Emergency: {self.is_emergency}, Email: {self.email})")

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        """Compare appointments by their unique ID."""
        if isinstance(other, Appointment):
            return self.appointment_id == other.appointment_id
        return False

    def __lt__(self, other):
        """Compare appointments by date and time."""
        if isinstance(other, Appointment):
            return (self.appointment_date, self.appointment_time) < (other.appointment_date, other.appointment_time)
        return NotImplemented
