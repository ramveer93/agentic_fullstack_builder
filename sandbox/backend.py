from typing import List, Optional

class Appointment:
    def __init__(self, patient_name: str, doctor_name: str, time_slot: str):
        self.patient_name = patient_name
        self.doctor_name = doctor_name
        self.time_slot = time_slot

    def __str__(self) -> str:
        return f'Appointment(Patient: {self.patient_name}, Doctor: {self.doctor_name}, Time: {self.time_slot})'

class AppointmentManager:
    def __init__(self):
        self.appointments: List[Appointment] = []
        self.doctors: List[str] = ['Dr. Smith', 'Dr. Jones', 'Dr. Brown']

    def book_appointment(self, patient_name: str, doctor_name: str, time_slot: str) -> bool:
        if not self.is_time_slot_available(doctor_name, time_slot):
            return False
        new_appointment = Appointment(patient_name, doctor_name, time_slot)
        self.appointments.append(new_appointment)
        return True

    def view_appointments(self, doctor_name: str) -> List[Appointment]:
        return [appointment for appointment in self.appointments if appointment.doctor_name == doctor_name]

    def cancel_appointment(self, patient_name: str, doctor_name: str, time_slot: str) -> bool:
        for appointment in self.appointments:
            if (appointment.patient_name == patient_name and 
                appointment.doctor_name == doctor_name and 
                appointment.time_slot == time_slot):
                self.appointments.remove(appointment)
                return True
        return False

    def list_doctors(self) -> List[str]:
        return self.doctors

    def is_time_slot_available(self, doctor_name: str, time_slot: str) -> bool:
        for appointment in self.appointments:
            if appointment.doctor_name == doctor_name and appointment.time_slot == time_slot:
                return False
        return True

    def current_appointments(self) -> List[Appointment]:
        return self.appointments