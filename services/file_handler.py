import json
from models.appointment import Appointment

class FileHandler:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save_appointments(self, appointments_list):
        """
        Save the list of appointments to a JSON file.
        
        Args:
            appointments_list (list): A list of appointment objects to save.
        """
        # Create an empty list to hold the appointment dictionaries
        json_data = []
        
        # Convert each appointment object to a dictionary and add it to the list
        for appointment in appointments_list:
            appointment_dict = self._appointment_to_dict(appointment)
            json_data.append(appointment_dict)
        
        # Open the JSON file for writing
        with open(self.file_path, 'w') as json_file:
            # Write the list of appointment dictionaries to the JSON file
            json.dump(json_data, json_file, indent=4)


    def load_appointments(self) -> list:
        """
        Load appointments from a JSON file.
        
        Returns:
            list: A list of appointment objects.
        """
        try:
            # Open the JSON file for reading
            with open(self.file_path, 'r') as json_file:
                # Load the data from the JSON file
                appointments_data = json.load(json_file)
                
                # Create an empty list to hold the appointment objects
                appointments_list = []
                
                # Convert each dictionary in the loaded data to an appointment object
                for appt_data in appointments_data:
                    appointment = self._dict_to_appointment(appt_data)
                    appointments_list.append(appointment)
                    
                return appointments_list

        # If the file doesn't exist, return an empty list
        except FileNotFoundError:
            return []

        # If the file is corrupted or contains invalid JSON, return an empty list
        except json.JSONDecodeError:
            return []


    def _appointment_to_dict(self, appointment: Appointment) -> dict:
        """
        Convert an Appointment object to a dictionary.

        Returns:
            dict: A dictionary of appointment details.
        """
        return {
            'customer_name': appointment.customer_name,
            'vehicle_type': appointment.vehicle_type,
            'appointment_date': appointment.appointment_date.strftime('%Y-%m-%d'),
            'appointment_time': appointment.appointment_time.strftime('%H:%M'),
            'maintenance_type': appointment.maintenance_type,
            'appointment_id': appointment.appointment_id,
            'is_emergency': appointment.is_emergency,
            'email': appointment.email  
        }

    def _dict_to_appointment(self, data: dict) -> Appointment:
        """Convert a dictionary to an Appointment object."""
        appointment = Appointment(
            customer_name=data['customer_name'],
            vehicle_type=data['vehicle_type'],
            appointment_date=data['appointment_date'],
            appointment_time=data['appointment_time'],
            maintenance_type=data['maintenance_type'],
            is_emergency=data.get('is_emergency', False),
            email=data.get('email')  
        )
        appointment.appointment_id = data['appointment_id']  
        return appointment
