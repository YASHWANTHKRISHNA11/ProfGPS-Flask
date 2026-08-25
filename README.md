# ProfGPS - GPS-Based Faculty Attendance System

## Overview

ProfGPS is a Flask-based web application designed to automate and streamline faculty attendance tracking using GPS verification. The system allows faculty members to mark attendance when they are within a geographically defined boundary set by administrators. This ensures accurate and tamper-resistant attendance management for educational institutions.

**Key Feature:** Faculty can only mark attendance when their GPS coordinates are within an admin-defined radius around a specified location, using the Haversine formula for distance calculation.

---

## Technology Stack

- **Frontend:** HTML5, CSS3
- **Backend:** Flask (Python)
- **Database:** MySQL
- **Primary Libraries:** 
  - `flask` - Web framework
  - `mysql-connector-python` - MySQL database connector
  - `math` - Haversine formula calculations for GPS distance

---

## Project Structure

```
ProfGPS-Flask/
├── app.py                 # Main Flask application with all routes and business logic
├── db_config.py           # Database connection configuration
├── static/
│   ├── style.css          # Application styling
│   └── LOGO.png           # Application logo
├── templates/
│   ├── index.html                 # Home page
│   ├── faculty-login.html         # Faculty login form
│   ├── faculty-dashboard.html     # Faculty dashboard and attendance history
│   ├── mark-attendance.html       # GPS-based attendance marking page
│   ├── attendance-success.html    # Attendance confirmation page
│   ├── admin-login.html           # Admin login form
│   ├── admin-dashboard.html       # Admin dashboard with summaries
│   ├── admin-faculty-list.html    # Faculty management interface
│   ├── add-faculty.html           # Add new faculty form
│   ├── edit-faculty.html          # Edit faculty information
│   ├── gps-boundary.html          # GPS boundary configuration for admins
│   ├── admin-attendance-list.html # Attendance record management
│   └── edit-attendance.html       # Edit attendance records
└── README.md              # This file

```

### How It Works

**Flow:**
1. Faculty login with their ID and password → redirects to dashboard
2. Faculty clicks "Mark Attendance" → browser requests current GPS coordinates
3. Faculty's GPS location is verified against admin-set boundary using Haversine formula
4. If within boundary: attendance is recorded in database with timestamp and coordinates
5. If outside boundary: attendance request is rejected
6. Admins can set/update GPS boundaries, manage faculty profiles, and view/edit attendance records

**GPS Verification:** The application uses the Haversine formula to calculate the great-circle distance between the faculty's current GPS coordinates and the admin-defined boundary center point. Attendance is only recorded if the distance is less than or equal to the specified radius (in meters).

---

## Database Schema

### Tables

- **`faculty`** - Stores faculty member information
  - `id`, `faculty_id`, `name`, `email`, `phone`, `password`, `department`, `designation`

- **`admin`** - Stores admin user credentials
  - `id`, `username`, `password`

- **`attendance`** - Records attendance entries
  - `id`, `faculty_id`, `timestamp`, `location` (latitude, longitude)

- **`gps_boundary`** - Stores the authorized attendance region
  - `id`, `latitude`, `longitude`, `radius` (in meters)

---

## Installation & Setup

### Prerequisites
- Python 3.7+
- MySQL Server
- A modern web browser with geolocation support

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YASHWANTHKRISHNA11/ProfGPS-Flask.git
   cd ProfGPS-Flask
   ```

2. **Set up MySQL Database:**
   ```sql
   CREATE DATABASE profgps;
   USE profgps;

   CREATE TABLE faculty (
       id INT AUTO_INCREMENT PRIMARY KEY,
       faculty_id VARCHAR(50) UNIQUE,
       name VARCHAR(100),
       email VARCHAR(100),
       phone VARCHAR(20),
       password VARCHAR(100),
       department VARCHAR(50),
       designation VARCHAR(50)
   );

   CREATE TABLE admin (
       id INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(50) UNIQUE,
       password VARCHAR(100)
   );

   CREATE TABLE gps_boundary (
       id INT AUTO_INCREMENT PRIMARY KEY,
       latitude DECIMAL(10, 8),
       longitude DECIMAL(11, 8),
       radius INT
   );

   CREATE TABLE attendance (
       id INT AUTO_INCREMENT PRIMARY KEY,
       faculty_id INT,
       timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
       location VARCHAR(50),
       FOREIGN KEY (faculty_id) REFERENCES faculty(id)
   );
   ```

3. **Update database configuration:**
   Edit `db_config.py` with your MySQL credentials:
   ```python
   return mysql.connector.connect(
       host="localhost",
       user="your_mysql_user",
       password="your_mysql_password",
       database="profgps"
   )
   ```

4. **Install Python dependencies:**
   ```bash
   pip install flask mysql-connector-python
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```
   The application will start on `http://localhost:5000`

---

## Features

### Faculty Features
- **Login:** Secure login with faculty ID and password
- **Mark Attendance:** GPS-based attendance marking with location verification
- **View History:** See complete attendance record with timestamps and GPS coordinates
- **Dashboard:** Personal dashboard showing profile and attendance history

### Admin Features
- **Admin Login:** Secure admin authentication
- **Faculty Management:** Add, edit, and delete faculty profiles
- **GPS Boundary Configuration:** Set the attendance region (center coordinates and radius)
- **Attendance Management:** View, edit, and delete attendance records
- **View Statistics:** Dashboard showing all faculty and attendance records

---

## Application Routes

### Public Routes
- `GET /` - Home page
- `GET/POST /login` - Faculty login
- `GET/POST /admin-login` - Admin login
- `GET /logout` - Logout (clears session)

### Faculty Routes (requires login)
- `GET /dashboard` - Faculty dashboard with attendance history
- `GET/POST /mark-attendance` - Mark attendance via GPS
- `GET /attendance-success` - Attendance confirmation page

### Admin Routes (requires admin login)
- `GET /admin-dashboard` - Admin dashboard
- `GET /admin/faculty` - List all faculty
- `GET/POST /admin/faculty/add` - Add new faculty
- `GET/POST /admin/faculty/edit/<id>` - Edit faculty information
- `GET /admin/faculty/delete/<id>` - Delete faculty
- `GET/POST /gps-boundary` - Configure GPS attendance boundary
- `GET /admin/attendance` - List all attendance records
- `GET/POST /admin/attendance/edit/<id>` - Edit attendance record
- `GET /admin/attendance/delete/<id>` - Delete attendance record

---

## Current Limitations & Security Notes

⚠️ **Important:** This is an educational project with known security limitations:

1. **Passwords stored in plain text** - Passwords are NOT hashed. Do NOT use with real sensitive data.
2. **No input validation** - Vulnerable to SQL injection. Implement proper input validation before production use.
3. **Basic session management** - Uses Flask sessions without additional security measures.
4. **No role-based access control** - Limited authorization checks.
5. **GPS spoofing risk** - Browser geolocation can be spoofed; implement server-side GPS verification for production.
6. **No HTTPS enforcement** - Should use HTTPS in production.
7. **Debug mode enabled** - `app.run(debug=True)` should be disabled in production.

---

## Future Enhancements (Planned)

- [ ] Implement password hashing (bcrypt)
- [ ] Add input validation and SQL injection prevention
- [ ] Implement real-time GPS verification
- [ ] Add facial recognition for additional security
- [ ] Mobile-responsive design improvements
- [ ] Integration with Learning Management Systems (LMS)
- [ ] Email notifications for attendance events
- [ ] Attendance analytics and reporting
- [ ] Mobile app version (iOS/Android)

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **Database connection error** | Ensure MySQL is running and credentials in `db_config.py` are correct |
| **"Attendance region is not set by admin"** | Admin must log in and configure GPS boundary first via /gps-boundary |
| **GPS location not detected** | Ensure browser has location permission; use HTTPS (required for geolocation in production) |
| **"You are outside the attendance boundary"** | Faculty must be within the configured radius to mark attendance |
| **Faculty can't login** | Verify faculty credentials in the database and ensure password matches exactly |
| **Port 5000 already in use** | Change port in `app.py`: `app.run(debug=True, port=5001)` |

---

## Contributing

This is an educational project. Contributions and improvements are welcome. Please ensure:
- Code follows PEP 8 style guidelines
- Security improvements are prioritized
- Database operations use parameterized queries
- All changes are tested before submission

---

## License

This project is open source and available for educational purposes.

---

## Author

**YASHWANTHKRISHNA11**  
Created: July 2025

---

## Disclaimer

This application is designed for educational purposes. It demonstrates basic web development concepts including Flask, MySQL integration, and GPS-based geolocation. Due to the security limitations noted above, it should NOT be used in a production environment without significant security hardening.
