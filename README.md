# ProfGPS

## Project Overview
ProfGPS is a Flask-based web application designed to help users track and plan their academic activities effectively. The application provides features for managing schedules, courses, and assignments.

## Features
- **User Authentication**: Secure login and registration for users.
- **Course Management**: Add, edit, and delete courses from your schedule.
- **Assignment Tracking**: Keep track of assignments and their due dates.
- **Notifications**: Get reminders for upcoming assignments and deadlines.
- **Responsive Design**: Accessible on both desktop and mobile devices.

## Technology Stack
- **Backend**: Flask, SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite or PostgreSQL
- **Deployment**: Docker

## Installation
To set up the project locally, follow these steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/YASHWANTHKRISHNA11/ProfGPS-Flask.git
   ```
2. Navigate into the project directory:
   ```bash
   cd ProfGPS-Flask
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the database:
   ```bash
   python -m flask db upgrade
   ```
5. Run the application:
   ```bash
   flask run
   ```

## Usage
- Visit `http://localhost:5000` in your web browser to access the application.
- Create an account or log in if you already have one.
- Start managing your academic activities through the provided features.

## Contributing
Contributions are welcome! Please create a pull request for any changes you'd like to propose.

## License
This project is licensed under the MIT License.