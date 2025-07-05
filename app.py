# app.py
from flask import Flask, render_template, request, redirect, url_for, session , flash
from flask import jsonify
import db_config
import math
from datetime import datetime
from db_config import get_connection

app = Flask(__name__)
app.secret_key = 'profgps-secret'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        faculty_id = request.form['faculty_id']
        password = request.form['password']

        conn = db_config.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM faculty WHERE faculty_id=%s AND password=%s", (faculty_id, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['faculty_id'] = faculty_id
            return redirect(url_for('dashboard'))
        else:
            return render_template('faculty-login.html', error='Invalid credentials')

    return render_template('faculty-login.html')

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = db_config.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
        admin = cursor.fetchone()
        conn.close()

        if admin:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin-login.html', error='Invalid credentials')

    return render_template('admin-login.html')

@app.route('/dashboard')
def dashboard():
    if 'faculty_id' not in session:
        return redirect(url_for('login'))

    faculty_id = session['faculty_id']
    conn = db_config.get_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch faculty profile
    cursor.execute("SELECT * FROM faculty WHERE faculty_id=%s", (faculty_id,))
    profile = cursor.fetchone()

    # Fetch attendance history
    cursor.execute("SELECT * FROM attendance WHERE faculty_id=%s ORDER BY timestamp DESC", (faculty_id,))
    attendance_records = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('faculty-dashboard.html', profile=profile, attendance=attendance_records)

@app.route('/admin/faculty')
def admin_faculty_list():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM faculty')
    faculty_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admin-faculty-list.html', faculty_list=faculty_list)

@app.route('/admin/faculty/add', methods=['GET', 'POST'])
def add_faculty():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']  # You may hash this later
        department = request.form['department']
        designation = request.form['designation']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO faculty (name, email, phone, password, department, designation)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (name, email, phone, password, department, designation))
        conn.commit()
        cursor.close()
        conn.close()
        flash('New faculty added successfully.')
        return redirect(url_for('admin_faculty_list'))

    return render_template('add-faculty.html')

@app.route('/admin/faculty/edit/<int:faculty_id>', methods=['GET', 'POST'])
def edit_faculty(faculty_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Use %s for MySQL, not ?
    cursor.execute('SELECT * FROM faculty WHERE id = %s', (faculty_id,))
    faculty = cursor.fetchone()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        department = request.form['department']
        designation = request.form['designation']

        cursor.execute('''
            UPDATE faculty SET name = %s, email = %s, phone = %s, department = %s, designation = %s
            WHERE id = %s
        ''', (name, email, phone, department, designation, faculty_id))

        conn.commit()
        flash('Faculty updated successfully.')
        return redirect(url_for('admin_faculty_list'))

    cursor.close()
    conn.close()
    return render_template('edit-faculty.html', faculty=faculty)

@app.route('/admin/faculty/delete/<int:faculty_id>')
def delete_faculty(faculty_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM faculty WHERE id = %s', (faculty_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Faculty deleted successfully.')
    return redirect(url_for('admin_faculty_list'))

@app.route('/admin/attendance')
def admin_attendance_list():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT attendance.id,
               DATE(attendance.timestamp) AS date,
               TIME(attendance.timestamp) AS time,
               attendance.latitude,
               attendance.longitude,
               faculty.name
        FROM attendance
        JOIN faculty ON attendance.faculty_id = faculty.id
        ORDER BY attendance.timestamp DESC
    ''')
    attendance_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admin-attendance-list.html', attendance_list=attendance_list)


@app.route('/admin/attendance/edit/<int:attendance_id>', methods=['GET', 'POST'])
def edit_attendance(attendance_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('''
        SELECT attendance.*, faculty.name FROM attendance
        JOIN faculty ON attendance.faculty_id = faculty.id
        WHERE attendance.id = %s
    ''', (attendance_id,))
    record = cursor.fetchone()

    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        latitude = request.form['latitude']
        longitude = request.form['longitude']

        cursor.execute('''
            UPDATE attendance SET date = %s, time = %s,
            latitude = %s, longitude = %s
            WHERE id = %s
        ''', (date, time, latitude, longitude, attendance_id))

        conn.commit()
        cursor.close()
        conn.close()
        flash('Attendance record updated successfully.')
        return redirect(url_for('admin_attendance_list'))

    cursor.close()
    conn.close()
    return render_template('edit-attendance.html', record=record)

@app.route('/admin/attendance/delete/<int:attendance_id>')
def delete_attendance(attendance_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM attendance WHERE id = %s', (attendance_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Attendance record deleted successfully.')
    return redirect(url_for('admin_attendance_list'))

@app.route('/gps-boundary', methods=['GET', 'POST'])
def gps_boundary():
    conn = db_config.get_connection()
    cursor = conn.cursor()
    message = None

    if request.method == 'POST':
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        radius = request.form['radius']

        try:
            # Delete old boundary if exists
            cursor.execute("DELETE FROM gps_boundary")

            # Insert new boundary
            cursor.execute(
                "INSERT INTO gps_boundary (latitude, longitude, radius) VALUES (%s, %s, %s)",
                (latitude, longitude, radius)
            )
            conn.commit()
            message = "GPS boundary updated successfully!"
        except Exception as e:
            message = f"Error updating GPS boundary: {str(e)}"

    # Get current boundary if exists
    cursor.execute("SELECT * FROM gps_boundary LIMIT 1")
    boundary = cursor.fetchone()

    conn.close()
    return render_template('gps-boundary.html', boundary=boundary)

# Helper function to calculate distance between two coordinates
def is_within_boundary(lat1, lon1, lat2, lon2, radius_m):
    R = 6371000  # Radius of Earth in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance <= radius_m

# Route to show HTML page (GET) and receive GPS data (POST)
@app.route('/mark-attendance', methods=['GET', 'POST'])
def mark_attendance():
    if 'faculty_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('mark-attendance.html')

    if request.method == 'POST':
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        conn = db_config.get_connection()
        cursor = conn.cursor()

        # Fetch admin-set GPS boundary
        cursor.execute("SELECT latitude, longitude, radius FROM gps_boundary ORDER BY id DESC LIMIT 1")
        boundary = cursor.fetchone()

        if not boundary:
            conn.close()
            return jsonify({'message': 'Attendance region is not set by admin.'})

        admin_lat, admin_lon, radius = boundary

        if is_within_boundary(latitude, longitude, admin_lat, admin_lon, radius):
            cursor.execute(
                "INSERT INTO attendance (faculty_id, timestamp, location) VALUES (%s, NOW(), %s)",
                (session['faculty_id'], f"{latitude}, {longitude}")
            )
            conn.commit()
            conn.close()
            return jsonify({'message': 'Attendance marked successfully!'})
        else:
            conn.close()
            return jsonify({'message': 'You are outside the attendance boundary.'})

@app.route('/attendance-success')
def attendance_success():
    if 'faculty_id' not in session:
        return redirect(url_for('login'))

    faculty_id = session['faculty_id']
    conn = db_config.get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO attendance (faculty_id) VALUES (%s)", (faculty_id,))
    conn.commit()
    conn.close()

    return render_template('attendance-success.html', faculty_id=faculty_id, timestamp=datetime.now())

@app.route('/admin-dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    conn = db_config.get_connection()
    cursor = conn.cursor()
    
    # Fetch all faculty
    cursor.execute("SELECT * FROM faculty")
    faculty = cursor.fetchall()

    # Fetch all attendance records
    cursor.execute("SELECT * FROM attendance")
    attendance = cursor.fetchall()

    conn.close()

    return render_template('admin-dashboard.html', faculty=faculty, attendance=attendance)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
