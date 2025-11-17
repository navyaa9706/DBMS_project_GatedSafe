from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

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

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT gua_password FROM SecurityGuards WHERE GID = %s", (gid,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            stored_password = result[0]
            if password == stored_password:  # Replace with hashed check if needed
                return redirect(url_for('guard_dashboard'))
            else:
                flash('Incorrect password.', 'error')
        else:
            flash('Guard ID not found.', 'error')

    return render_template('guard-login.html')

@app.route('/guard/dashboard')
def guard_dashboard():
    return render_template('guard-dashboard.html')

@app.route('/resident/login', methods=['GET', 'POST'])
def resident_login():
    if request.method == 'POST':
        rid = request.form.get('resident-id')
        password = request.form.get('password')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT RID FROM Residents WHERE RID=%s", (rid,))
        resident = cursor.fetchone()
        cursor.close()
        conn.close()
        if resident:
            return redirect(url_for('resident_dashboard', rid=rid))
        flash('Invalid Resident ID or Password')
    return render_template('resident-login.html')

@app.route('/resident/dashboard')
def resident_dashboard():
    rid = request.args.get('rid')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT flat_no, r_name FROM Residents WHERE RID=%s", (rid,))
    resident = cursor.fetchone()
    visits = []
    if resident:
        flat_no = resident[0]
        name = resident[1]
        cursor.execute("""
            SELECT log_id, visitor_name, purpose, entry_gate, entry_time, exit_gate, exit_time
            FROM EntryExitLogs WHERE flat_no=%s ORDER BY entry_time DESC
        """, (flat_no,))
        visits = cursor.fetchall()
    cursor.close()
    conn.close()
    if resident:
        return render_template('resident-dashboard.html', rid=rid, flat_no=flat_no, name=name, visits=visits)
    flash('Resident not found')
    return redirect(url_for('resident_login'))

@app.route('/visitor/new', methods=['GET', 'POST'])
def new_visitor():
    if request.method == 'POST':
        data = {key: request.form[key] for key in ['visitorName','contact','flatNo','purpose','entryGate','exitGate','status']}
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO EntryExitLogs (visitor_name, visitor_contact, flat_no, purpose, entry_time, entry_gate, exit_gate, status)
            VALUES (%s, %s, %s, %s, NOW(), %s, %s, %s)
        """, (data['visitorName'], data['contact'], data['flatNo'], data['purpose'], data['entryGate'], data['exitGate'], data['status']))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Visitor entry submitted.')
        return redirect(url_for('guard_dashboard'))
    return render_template('new-visitor.html')

@app.route('/frequent-visitors', methods=['GET', 'POST'])
def frequent_visitors():
    if request.method == 'POST':
        data = {key: request.form[key] for key in ['visitorName','contact','category','flatNo','entryGate','exitGate']}
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO fixed_visitors
            (full_name, phone_number, visitor_type, assigned_house_id, allowed_days, allowed_time_start, allowed_time_end, date_registered)
            VALUES (%s, %s, %s, %s, '', '00:00', '23:59', CURDATE())
        """, (data['visitorName'], data['contact'], data['category'], data['flatNo']))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Frequent visitor logged.')
        return redirect(url_for('guard_dashboard'))
    return render_template('frequent-visitors.html')

@app.route('/log-exit', methods=['GET', 'POST'])
def log_exit():
    if request.method == 'POST':
        visitor_name = request.form.get('visitorName')
        contact = request.form.get('contact')

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.callproc('UPDATEEXIT', [visitor_name, contact])
            conn.commit()
            flash('Visitor exit logged successfully.', 'success')
        except mysql.connector.Error as err:
            flash(f'Error: {err.msg}', 'error')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('guard_dashboard'))

    return render_template('log_exit.html')

@app.route('/frequency-detection', methods=['GET', 'POST'])
def frequency_detection():
    if request.method == 'POST':
        data = {key: request.form.get(key) for key in ['visitorName','contact','flatNo','startDate','endDate','threshold']}
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM EntryExitLogs
            WHERE visitor_name=%s AND visitor_contact=%s AND flat_no=%s
            AND entry_time BETWEEN %s AND %s
        """, (data['visitorName'], data['contact'], data['flatNo'], data['startDate'], data['endDate']))
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        suspicious = int(count) > int(data['threshold']) if data['threshold'] else False
        flash(f"Visitor {data['visitorName']} visit count: {count}. Suspicious: {suspicious}")
    return render_template('frequency-detection.html')

@app.route('/suspicious')
def suspicious():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT log_id, visitor_name, visitor_contact, flat_no, entry_time, exit_time, status
        FROM EntryExitLogs WHERE status='Suspicious'
    """)
    visitors = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('suspicious.html', suspicious=visitors)

@app.route('/emergency', methods=['GET', 'POST'])
def emergency():
    if request.method == 'POST':
        flat_no = request.form.get('flatno')
        details = request.form.get('details')
        # Optional: call emergency_lookup procedure or notify system here
        flash('Emergency alert submitted.')
    return render_template('emergency.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
