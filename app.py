from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# دالة الاتصال بقاعدة البيانات
def get_db_connection():
    conn = sqlite3.connect('courses.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        course_name = request.form['course_name'].lower()  # تحويل إلى أحرف صغيرة
        course_number = request.form['course_number']
        classification = request.form['classification']

        conn = get_db_connection()
        cursor = conn.cursor()
        
        # استخدام LOWER لمطابقة غير حساسة لحالة الأحرف
        cursor.execute('SELECT * FROM courses WHERE LOWER(course_name) = ? AND course_number = ? AND classification = ?', 
                       (course_name, course_number, classification))
        courses = cursor.fetchall()
        conn.close()

        if courses:
            return render_template('results.html', courses=courses)
        else:
            return render_template('no_course.html')
    return render_template('search.html')

@app.route('/add', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        course_name = request.form['course_name']
        course_number = request.form['course_number']
        classification = request.form['classification']
        group_link = request.form.get('group_link', None)  
        admin_number = request.form.get('admin_number', None)


        print(f"course_name: {course_name}, course_number: {course_number}, classification: {classification}, group_link: {group_link}, admin_number: {admin_number}")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO courses (course_name, course_number, classification, link, admin_number) VALUES (?, ?, ?, ?, ?)', 
                       (course_name, course_number, classification, group_link, admin_number))  
        conn.commit()
        conn.close()

        return redirect(url_for('home'))
    return render_template('add_course.html')
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/course/<int:course_id>')
def course_detail(course_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM courses WHERE id = ?', (course_id,))
    course = cursor.fetchone()
    conn.close()
    return render_template('course_detail.html', course=course)

if __name__ == '__main__':
    app.run(debug=True)


##if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)