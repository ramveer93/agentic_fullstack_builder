import gradio as gr
from backend import AppointmentManager

# Initialize AppointmentManager instance
manager = AppointmentManager()

# Function to book an appointment

def book_appointment_interface(patient_name: str, doctor_name: str, time_slot: str) -> str:
    success = manager.book_appointment(patient_name, doctor_name, time_slot)
    return "Appointment booked!" if success else "Time slot is not available."

# Function to view appointments for a specific doctor

def view_appointments_interface(doctor_name: str) -> list:
    appointments = manager.view_appointments(doctor_name)
    return [str(appointment) for appointment in appointments]

# Function to cancel an existing appointment

def cancel_appointment_interface(patient_name: str, doctor_name: str, time_slot: str) -> str:
    success = manager.cancel_appointment(patient_name, doctor_name, time_slot)
    return "Appointment canceled!" if success else "No appointment found to cancel."

# Function to list all available doctors

def list_doctors_interface() -> list:
    return manager.list_doctors()

# Define the Gradio interface
app = gr.Blocks()

with app:
    gr.Markdown("# Appointment Management System")
    with gr.Row():
        with gr.Column():
            gr.Markdown("## Book an Appointment")
            patient_name = gr.Textbox(label="Patient Name")
            doctor_name = gr.Dropdown(choices=manager.list_doctors(), label="Doctor Name")
            time_slot = gr.Textbox(label="Time Slot (e.g. '2024-10-15 10:00 AM')")
            book_button = gr.Button("Book Appointment")
            book_output = gr.Textbox(label="Booking Status")
            book_button.click(book_appointment_interface, inputs=[patient_name, doctor_name, time_slot], outputs=book_output)
            
            gr.Markdown("## View Appointments")
            view_doctor = gr.Dropdown(choices=manager.list_doctors(), label="Select Doctor")
            view_button = gr.Button("View Appointments")
            view_output = gr.Textbox(label="Appointments")
            view_button.click(view_appointments_interface, inputs=view_doctor, outputs=view_output)

            gr.Markdown("## Cancel an Appointment")
            cancel_patient_name = gr.Textbox(label="Patient Name")
            cancel_doctor_name = gr.Dropdown(choices=manager.list_doctors(), label="Doctor Name")
            cancel_time_slot = gr.Textbox(label="Time Slot (e.g. '2024-10-15 10:00 AM')")
            cancel_button = gr.Button("Cancel Appointment")
            cancel_output = gr.Textbox(label="Cancellation Status")
            cancel_button.click(cancel_appointment_interface, inputs=[cancel_patient_name, cancel_doctor_name, cancel_time_slot], outputs=cancel_output)

            gr.Markdown("## List of Doctors")
            list_doctors_button = gr.Button("List Doctors")
            list_doctors_output = gr.Textbox(label="Doctors")
            list_doctors_button.click(list_doctors_interface, outputs=list_doctors_output)

# Launch the app
if __name__ == '__main__':
    app.launch()