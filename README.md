# Hospital Management System

## Overview
Hospital Management System is a web-based application built with Flask to streamline hospital operations. It enables patients to book appointments, doctors to manage consultations, and administrators to oversee system-wide operations. 

## Features
- **User Authentication**: Secure login system for patients, doctors, and administrators.
- **Appointment Scheduling**: Patients can book, modify, or cancel appointments.
- **Doctor & Patient Management**: Admins can add, update, and remove doctors and patient records.
- **Database Integration**: Supports PostgreSQL and MySQL for data persistence.
- **Role-Based Access Control**: Different permissions for patients, doctors, and administrators.
- **Responsive Design**: Uses Bootstrap and Flask templates for a user-friendly interface.

## Project Structure
```
hospital_management/
│── static/             # CSS, JavaScript, images
│── templates/          # HTML templates (Jinja2)
│── app.py              # Main Flask application file
│── myenv/              # Python virtual environment (optional)
│── README.md           # Project documentation
│── LICENSE             # Licensing information
```

## Installation
### Prerequisites
Ensure you have the following installed:
- **Python 3.8+**
- **pip** (Python package manager)
- **Flask** (Python web framework)
- **PostgreSQL or MySQL** (Database support)

### Setup Instructions
1. **Clone the repository**:
   ```sh
   git clone https://github.com/balcicekmustafa/HospitalAppointmentSystem.git
   ```
2. **Navigate to the project directory**:
   ```sh
   cd hospital_management
   ```
3. **Create and activate a virtual environment**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
4. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```
5. **Configure the database**:
   - Create a database (e.g., `hospital_db`).
   - Update the `app.py` file with database credentials.
6. **Run the application**:
   ```sh
   flask run
   ```

## Usage
1. **Open the application** in a web browser at `http://127.0.0.1:5000`.
2. **User Roles**:
   - **Patients**: Register, log in, book, cancel, and view their appointments.
   - **Doctors**: Log in, view their assigned patients, manage reports, and prescriptions.
   - **Admins**: Manage doctors, patients, and appointment scheduling.
3. **Key Functionalities**:
   - Secure user authentication system with session management.
   - Patients can book, reschedule, or cancel their appointments.
   - Doctors can update appointment statuses, issue reports, and prescriptions.
   - Admins have full control over hospital management operations.

## Technologies Used
- **Python 3.8+**: Core programming language
- **Flask**: Web framework
- **Jinja2**: Templating engine
- **SQLAlchemy**: ORM for database interactions
- **Flask-WTF**: Form validation and security
- **PostgreSQL/MySQL**: Database management
- **Bootstrap**: Frontend framework for styling

## Contribution
Contributions are encouraged! To contribute:
1. Fork the repository.
2. Create a new branch (`feature-branch-name`).
3. Commit your changes.
4. Push to your branch and create a pull request.

## License
This project is licensed under the MIT License. See `LICENSE` for more details.

## Contact
For issues or inquiries, please reach out to the repository owner [balcicekmustafa](https://github.com/balcicekmustafa).
