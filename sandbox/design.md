# Appointment Management System Design

## Overview
This design outlines a simple appointment management system for a medical clinic. It will include backend functionality to manage appointments, frontend functionality to provide a user interface for booking and viewing appointments, and unit tests to ensure the system works correctly.

### Modules and Classes

#### Backend Module - `backend.py`
This module will handle the logic related to appointments, including booking, viewing, and canceling appointments. 

1. **Class: `Appointment`**
   - **Attributes:**
     - `patient_name: str`
     - `doctor_name: str`
     - `time_slot: str`
   - **Methods:**
     - `__init__(self, patient_name: str, doctor_name: str, time_slot: str)`
     - `__str__(self) -> str`
  
2. **Class: `AppointmentManager`**
   - **Attributes:**
     - `appointments: List[Appointment]`
     - `doctors: List[str]`
   - **Methods:**
     - `__init__(self)`
     - `book_appointment(self, patient_name: str, doctor_name: str, time_slot: str) -> bool`
     - `view_appointments(self, doctor_name: str) -> List[Appointment]`
     - `cancel_appointment(self, patient_name: str, doctor_name: str, time_slot: str) -> bool`
     - `list_doctors(self) -> List[str]`

3. **Function: `is_time_slot_available(doctor_name: str, time_slot: str) -> bool`**
   - Checks if the given time slot is available for the specified doctor.

4. **Function: `current_appointments(self) -> List[Appointment]`**
   - Returns a list of current appointments.

#### Frontend Module - `app.py`
This module will handle the user interface for the appointment management system using Gradio.

1. **Function: `book_appointment_interface(patient_name: str, doctor_name: str, time_slot: str) -> str`**
   - Input: `patient_name: str`, `doctor_name: str`, `time_slot: str`
   - Output: Confirmation message (booked or error message).

2. **Function: `view_appointments_interface(doctor_name: str) -> List[str]`**
   - Input: `doctor_name: str`
   - Output: List of appointments for the specified doctor.

3. **Function: `cancel_appointment_interface(patient_name: str, doctor_name: str, time_slot: str) -> str`**
   - Input: `patient_name: str`, `doctor_name: str`, `time_slot: str`
   - Output: Confirmation of cancellation.

4. **Function: `list_doctors_interface() -> List[str]`**
   - Output: List of available doctors.

5. **Gradio Interface Setup:**
   - `gr.Interface(...)` to bind the above functions to the user interface.

### Test Module - Unit Tests
The test engineer will create a separate test file for unit tests.

#### Test Cases in a Module (e.g., `test_backend.py`)
1. **Test: `test_book_appointment()`**
   - Ensure that booking an appointment works correctly and prevents double-booking.

2. **Test: `test_view_appointments()`**
   - Verify that viewing appointments returns expected results for a given doctor.

3. **Test: `test_cancel_appointment()`**
   - Check that canceling an appointment works correctly.

4. **Test: `test_list_doctors()`**
   - Ensure that the list of doctors is returned correctly.

### Engineer Assignments
- **Backend Engineer:**
  - File: `backend.py`
  - Responsibilities: Implement `Appointment`, `AppointmentManager` classes and the related functions for booking, viewing, and cancelling appointments.

- **Frontend Engineer:**
  - File: `app.py`
  - Responsibilities: Implement user interface functions using Gradio, ensuring proper inputs/outputs and integrating with the backend functionality.

- **Test Engineer:**
  - File: `test_backend.py`
  - Responsibilities: Write unit tests for the backend functionalities to ensure correctness and robustness.