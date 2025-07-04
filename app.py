# app.py
from flask import Flask, render_template, request, redirect, url_for, session
import db_config
from datetime import datetime

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
