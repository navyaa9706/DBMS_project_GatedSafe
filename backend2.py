from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import mysql.connector
from mysql.connector.errors import Error, DatabaseError

app = Flask(__name__)
app.secret_key = 'supersecretkey'

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'Visitor_management_db'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guard/login', methods=['GET', 'POST'])
def guard_login():
    if request.method == 'POST':
        gid = request.form.get('guard-id')
        password = request.form.get('password')

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT gua_password FROM SecurityGuards WHERE GID = %s", (gid,))
            result = cursor.fetchone()
        except Error as e:
            flash("Database error during login.", "error")
            result = None
        finally:
            cursor.close()
            conn.close()

        if result:
            stored_password = result[0]
            if password == stored_password:
                session['gid'] = gid
                flash("Login successful.", "success")
                return redirect(url_for('guard_dashboard'))
            else:
                flash("Incorrect password.", "error")
        else:
            flash("Guard ID not found.", "error")

    return render_template('guard-login.html')

@app.route('/guard/dashboard')
def guard_dashboard():
    return render_template('guard-dashboard.html')

@app.route('/resident/login', methods=['GET', 'POST'])
def resident_login():
    if request.method == 'POST':
        rid = request.form.get('rid')
        password = request.form.get('password')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT RID, password FROM Residents WHERE RID=%s", (rid,))
        resident = cursor.fetchone()
        cursor.close()
        conn.close()

        if resident:
            db_rid, db_password = resident
            if db_password == password:
                session['resident_id'] = db_rid
                flash("Login successful", "success")
                return redirect(url_for('resident_dashboard'))
            else:
                flash("Invalid password", "error")
        else:
            flash("Resident not found", "error")

    return render_template('resident-login.html')

@app.route('/resident/dashboard')
def resident_dashboard():
    rid = session.get('resident_id')
    if not rid:
        flash("Please log in first", "error")
        return redirect(url_for('resident_login'))

    visits = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT flat_no, r_name FROM Residents WHERE RID=%s", (rid,))
        resident = cursor.fetchone()

        if resident:
            flat_no, name = resident
            cursor.execute("""
                SELECT log_id, visitor_name, purpose, entry_gate, entry_time, exit_gate, exit_time
                FROM EntryExitLogs WHERE flat_no=%s ORDER BY entry_time DESC
            """, (flat_no,))
            visits = cursor.fetchall()
        else:
            flash("Resident not found", "error")
            return redirect(url_for('resident_login'))

    except Error as e:
        flash("Database error while loading dashboard.", "error")
        return redirect(url_for('resident_login'))
    finally:
        cursor.close()
        conn.close()

    return render_template('resident-dashboard.html', rid=rid, flat_no=flat_no, name=name, visits=visits)

@app.route('/visitor/new', methods=['GET', 'POST'])
def new_visitor():
    if request.method == 'POST':
        data = {key: request.form[key] for key in ['visitorName','contact','flatNo','purpose','entryGate','status']}
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO EntryExitLogs (visitor_name, visitor_contact, flat_no, purpose, entry_time, entry_gate, verified_by_guard)
                VALUES (%s, %s, %s, %s, NOW(), %s, %s)
            """, (data['visitorName'], data['contact'], data['flatNo'], data['purpose'], data['entryGate'], session.get('gid')))
            conn.commit()

            cursor.execute("""
                INSERT INTO Visitors (v_name, contact, no_of_visits, is_frequent)
                VALUES (%s, %s, 1, FALSE)
                ON DUPLICATE KEY UPDATE
                    no_of_visits = no_of_visits + 1,
                    is_frequent = (no_of_visits + 1) > 5
            """, (data['visitorName'], data['contact']))
            conn.commit()

            flash("Visitor entry submitted.", "success")
            return redirect(url_for('guard_dashboard'))

        except DatabaseError as e:
            if e.errno == 1644:
                flash("Flat number not found.", "error")
            else:
                flash("Database error during visitor entry.", "error")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    return render_template('new-visitor.html')

@app.route('/frequent-visitors', methods=['GET', 'POST'])
def fixed_visitors():
    if request.method == 'POST':
        data = {key: request.form.get(key) for key in [
            'fullName','visitorType','gender','phoneNumber','altPhoneNumber',
            'address','houseId','allowedDays','allowedTimeStart',
            'allowedTimeEnd','dateRegistered','status'
        ]}
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO fixed_visitors
                (full_name, visitor_type, gender, phone_number, alt_phone_number, address,
                 assigned_house_id, allowed_days, allowed_time_start, allowed_time_end,
                 date_registered, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, tuple(data.values()))
            conn.commit()
            flash("Fixed visitor registered successfully.", "success")
            return redirect(url_for('guard_dashboard'))

        except Error as e:
            flash("Database error during fixed visitor registration.", "error")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    return render_template('frequent-visitors.html')

@app.route('/log-exit', methods=['GET', 'POST'])
def log_exit():
    if request.method == 'POST':
        visitor_name = request.form.get('visitorName')
        contact = request.form.get('contact')
        gate = request.form.get("exitGate")
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.callproc('UPDATEEXIT', [visitor_name, contact, gate])
            conn.commit()
            flash('Visitor exit logged successfully.', 'success')
        except mysql.connector.Error as err:
            flash(f'Error logging exit: {err.msg}', 'error')
            if conn:
                conn.rollback()
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return redirect(url_for('guard_dashboard'))

    return render_template('log_exit.html')


@app.route('/frequency-detection', methods=['GET', 'POST'])
def frequency_detection():
    if request.method == 'POST':
        data = {key: request.form.get(key) for key in ['visitorName','contact','flatNo','startDate','endDate','threshold']}

        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM EntryExitLogs
                WHERE visitor_name=%s AND visitor_contact=%s AND flat_no=%s
                AND entry_time BETWEEN %s AND %s
            """, (data['visitorName'], data['contact'], data['flatNo'], data['startDate'], data['endDate']))
            count = cursor.fetchone()[0]
            suspicious = int(count) > int(data['threshold']) if data['threshold'] else False
            flash(f"Visitor {data['visitorName']} visit count: {count}. Suspicious: {suspicious}", 'info')
        except mysql.connector.Error as err:
            flash(f"Error during frequency detection: {err.msg}", 'error')
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return render_template('frequency-detection.html')


@app.route('/suspicious')
def suspicious():
    conn = None
    cursor = None
    visitors = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT log_id, visitor_name, visitor_contact, flat_no, entry_time, exit_time
            FROM EntryExitLogs
            WHERE exit_gate IS NULL
            AND TIMESTAMPDIFF(HOUR, entry_time, NOW()) > 6
        """)
        visitors = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f"Error loading suspicious visitors: {err.msg}", 'error')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template('suspicious.html', suspicious=visitors)


@app.route("/past-visitors")
def past_visitors():
    print("Route /past-visitors is active")
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
            log_id,
            visitor_name,
            visitor_contact,
            flat_no,
            purpose,
            entry_time,
            exit_time,
            entry_gate,
            exit_gate,
            verified_guard
        FROM entryexitlogs
        ORDER BY entry_time DESC;
    """
    cursor.execute(query)
    records = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('past-visitors.html', records=records)



@app.route('/emergency', methods=['GET', 'POST'])
def emergency():
    visitor_records = []

    if request.method == 'POST':
        flat_no = request.form.get('flatno')
        incident_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.callproc('emergency_lookup', [incident_time, flat_no])
            for result in cursor.stored_results():
                visitor_records = result.fetchall()

            flash('Emergency alert submitted.', 'success')
        except Exception as err:
            flash(f'Error: {err}', 'error')
        finally:
            cursor.close()
            conn.close()

    return render_template('emergency.html', records=visitor_records)

@app.errorhandler(404)
def page_not_found(e):
    flash('Page not found.', 'warning')
    return render_template('index.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
