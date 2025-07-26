
from flask import Flask, render_template, request, redirect, session
import psycopg2
from database import get_db_connection

app = Flask(__name__)
app.secret_key = 'sama'


fake_users = {
    'sama@student.cu.edu.eg': {'password': '123456', 'role': 'student'},
    'admin@university.edu': {'password': 'admin123', 'role': 'admin'}
}


complaints_list = []
suggestion_list = []


@app.route('/')
def home():
    if 'email' in session:
        if session['role'] == 'admin':
            return redirect('/admin')
        else:
            return redirect('/dashboard')
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT users_role FROM users WHERE users_email = %s AND users_password = %s", (email, password))
        result = cur.fetchone()

        cur.close()
        conn.close()

        if result:
            session['email'] = email
            session['role'] = result[0]  # 'student' or 'admin'
            if result[0] == 'admin':
                return redirect('/admin')
            else:
                return redirect('/dashboard')
        else:
            return render_template('login.html', error="❌ Invalid email or password")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if 'email' not in session or session.get('role') != 'student':
        return redirect('/login')

    conn = get_db_connection()
    cur = conn.cursor()

    # نجيب ID الطالب
    cur.execute("SELECT users_id FROM users WHERE users_email = %s", (session['email'],))
    user = cur.fetchone()
    if not user:
        cur.close()
        conn.close()
        return "User not found", 404

    user_id = user[0]

    # نجيب الإشعارات الحقيقية
    cur.execute("""
        SELECT notifications_message, notifications_is_read, notifications_created_at
        FROM notifications
        WHERE user_id = %s
        ORDER BY notifications_created_at DESC
    """, (user_id,))

    notifications = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('dashboard.html', email=session['email'], notifications=notifications)

# --------------------
@app.route('/admin')
def admin_dashboard():
    if 'email' not in session or session.get('role') != 'admin':
        return redirect('/login')

    return render_template("admin.html", email=session['email'], complaints=complaints_list)


@app.route('/complaint', methods=['GET', 'POST'])
def complaint():
    if 'email' not in session or session.get('role') != 'student':
        return redirect('/login')

    conn = get_db_connection()
    cur = conn.cursor()

    # نجيب ID الطالب من الإيميل
    cur.execute("SELECT users_id FROM users WHERE users_email = %s", (session['email'],))
    user = cur.fetchone()
    if not user:
        cur.close()
        conn.close()
        return "User not found", 404

    user_id = user[0]

    # لما يبعت شكوى
    if request.method == 'POST':
        complaint_type = request.form['type']
        complaint_dep = request.form['dep']
        message = request.form['message']

        cur.execute("""
            INSERT INTO complaints (sender_id, complaints_type, complaints_dep, complaints_message)
            VALUES (%s, %s, %s, %s)
        """, (user_id, complaint_type, complaint_dep, message))

        conn.commit()

    # نعرض كل الشكاوى بتاعته
    cur.execute("""
        SELECT complaints_type, complaints_dep, complaints_message, complaints_status, complaints_created_at
        FROM complaints
        WHERE sender_id = %s
        ORDER BY complaints_created_at DESC
    """, (user_id,))

    complaints = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('complaint.html', complaints=complaints)

@app.route('/suggestion', methods=['GET', 'POST'])
def suggestion():
    if 'email' not in session or session.get('role') != 'student':
        return redirect('/login')

    conn = get_db_connection()
    cur = conn.cursor()

    # نجيب ID الطالب
    cur.execute("SELECT users_id FROM users WHERE users_email = %s", (session['email'],))
    user = cur.fetchone()
    if not user:
        cur.close()
        conn.close()
        return "User not found", 404

    user_id = user[0]

    if request.method == 'POST':
        suggestion_type = request.form['type']
        suggestion_dep = request.form['dep']
        message = request.form['message']

        cur.execute("""
            INSERT INTO suggestions (users_id, suggestions_type, suggestions_dep, suggestions_message)
            VALUES (%s, %s, %s, %s)
        """, (user_id, suggestion_type, suggestion_dep, message))
        conn.commit()

    # نعرض الاقتراحات بتاعته
    cur.execute("""
        SELECT suggestions_type, suggestions_dep, suggestions_message, suggestions_created_at
        FROM suggestions
        WHERE users_id = %s
        ORDER BY suggestions_created_at DESC
    """, (user_id,))
    suggestions = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('suggestion.html', suggestions=suggestions)

# --------------------
# Run App
# --------------------
if __name__ == '__main__':
    app.run(debug=True)
