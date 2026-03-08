# Project Overview
This project is a GPS-based faculty attendance system designed to automate and streamline the attendance process for educational institutions. The application leverages GPS technology to accurately track faculty attendance, ensuring accountability and transparency.

# Faculty Features
- View attendance records
- Mark attendance using GPS tracking
- Notification for attendance status

# Admin Features
- Manage faculty profiles and attendance records
- Generate reports based on attendance data
- Set attendance policies and rules

# Technology Stack
- **Frontend:** HTML, CSS
- **Backend:** Flask (Python)
- **Database:** MySQL

# Installation Guide
1. Clone the repository:
   ```
   git clone https://github.com/YASHWANTHKRISHNA11/ProfGPS-Flask.git
   ```
2. Navigate to the project directory:
   ```
   cd ProfGPS-Flask
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
4. Set up the MySQL database and update the configuration files.
5. Run the application:
   ```
   python app.py
   ```

# Database Schema
The database consists of the following main tables:
- `users`: Stores faculty and admin user information
- `attendance`: Records attendance with timestamps and GPS coordinates

# GPS Attendance Mechanism with Haversine Formula
The application uses the Haversine formula to calculate the distance between the faculty's location and the specified coordinates for attendance marking. This ensures that attendance is recorded only when the faculty is within a certain radius of the institution.

# API Routes Documentation
- `GET /api/attendance`: Retrieve attendance records
- `POST /api/mark-attendance`: Mark attendance using GPS coordinates

# Security Features
- User authentication and authorization
- Data encryption and secure database connections
- Input validation to prevent SQL injection and other attacks

# Troubleshooting Guide
- **Issue:** Unable to connect to the database
  - **Solution:** Check the database configurations and ensure the MySQL service is running.
- **Issue:** GPS not accurate
  - **Solution:** Ensure that location services are enabled on the device.

# Future Enhancements
- Implement facial recognition for attendance marking.
- Integrate with learning management systems (LMS).
- Add mobile application for easier attendance management.
