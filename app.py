from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__, static_folder='.', static_url_path='')

CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# ===== DEMO DATA (không cần database) =====
DEMO_USERS = {
    'student': {
        'email': 'student1@example.com',
        'password': 'studentpass',
        'FullName': 'Nguyễn Văn An',
        'Phone': '0901234567',
        'Class': 'CNTT-01',
        'Role': 'student',
        'StudentID': 'SV001'
    },
    'teacher': {
        'email': 'gv.demo@university.edu.vn',
        'password': 'teacher123',
        'FullName': 'TS. Nguyễn Văn Giảng',
        'Phone': '0123456789',
        'Department': 'Khoa Công nghệ Thông tin',
        'Role': 'teacher',
        'TeacherID': 'GV001'
    }
}

# ===== SERVE FRONTEND =====
@app.route('/')
def index():
    return send_from_directory('.', 'login.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

# ===== HEALTH CHECK =====
@app.route('/api')
def home():
    return jsonify({
        "message": "✅ Flask backend is running!",
        "status": "online",
        "mode": "demo",
        "timestamp": datetime.now().isoformat(),
        "api_endpoints": {
            "authentication": ["POST /api/login", "POST /api/change-password"],
            "students": ["POST /api/students/register", "GET /api/students"],
            "grades": ["POST /api/grades", "GET /api/grades/<student_id>"],
            "attendance": ["POST /api/attendance", "GET /api/attendance/<student_id>"],
            "profile": ["PUT /api/profile/<user_id>"]
        }
    })

# ===== API ĐĂNG NHẬP =====
@app.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 204

    try:
        data = request.json
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        role = data.get('role', 'student')

        if not email or not password:
            return jsonify({'success': False, 'message': 'Email và mật khẩu không được để trống'}), 400

        demo = DEMO_USERS.get(role)
        if demo and email == demo['email'].lower() and password == demo['password']:
            user_data = {k: v for k, v in demo.items() if k != 'password'}
            return jsonify({'success': True, 'message': 'Đăng nhập thành công', 'user': user_data})

        return jsonify({'success': False, 'message': 'Email hoặc mật khẩu không đúng'}), 401

    except Exception as e:
        return jsonify({'success': False, 'message': f'Lỗi server: {str(e)}'}), 500

# ===== API DANH SÁCH SINH VIÊN =====
@app.route('/api/students', methods=['GET', 'OPTIONS'])
def get_students():
    if request.method == 'OPTIONS':
        return '', 204
    students = [
        {'StudentID': 'SV001', 'FullName': 'Nguyễn Văn An', 'Email': 'student1@example.com', 'Phone': '0901234567', 'Class': 'CNTT-01', 'AvgGrade': 8.5},
        {'StudentID': 'SV002', 'FullName': 'Trần Thị Bình', 'Email': 'student2@example.com', 'Phone': '0912345678', 'Class': 'CNTT-01', 'AvgGrade': 7.8},
        {'StudentID': 'SV003', 'FullName': 'Lê Văn Cường', 'Email': 'student3@example.com', 'Phone': '0923456789', 'Class': 'CNTT-02', 'AvgGrade': 9.0},
    ]
    return jsonify({'success': True, 'data': students, 'count': len(students)})

# ===== API ĐIỂM SỐ =====
@app.route('/api/grades', methods=['POST', 'OPTIONS'])
def add_grade():
    if request.method == 'OPTIONS':
        return '', 204
    try:
        data = request.json
        midterm = float(data.get('midterm', 0))
        final = float(data.get('final', 0))
        avg = round(midterm * 0.4 + final * 0.6, 2)
        return jsonify({'success': True, 'message': 'Đã thêm điểm thành công', 'average': avg})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Lỗi: {str(e)}'}), 500

@app.route('/api/grades/<student_id>', methods=['GET', 'OPTIONS'])
def get_student_grades(student_id):
    if request.method == 'OPTIONS':
        return '', 204
    grades = [
        {'GradeID': 1, 'Subject': 'Toán cao cấp', 'Midterm': 7.5, 'Final': 8.0, 'Average': 7.8, 'Semester': 1, 'Year': 2024},
        {'GradeID': 2, 'Subject': 'Lập trình Python', 'Midterm': 8.5, 'Final': 9.0, 'Average': 8.8, 'Semester': 1, 'Year': 2024},
        {'GradeID': 3, 'Subject': 'Mạng máy tính', 'Midterm': 6.5, 'Final': 7.5, 'Average': 7.1, 'Semester': 1, 'Year': 2024},
    ]
    return jsonify({'success': True, 'data': grades, 'count': len(grades)})

# ===== API ĐIỂM DANH =====
@app.route('/api/attendance', methods=['POST', 'OPTIONS'])
def mark_attendance():
    if request.method == 'OPTIONS':
        return '', 204
    return jsonify({'success': True, 'message': 'Đã lưu điểm danh'})

@app.route('/api/attendance/<student_id>', methods=['GET', 'OPTIONS'])
def get_attendance(student_id):
    if request.method == 'OPTIONS':
        return '', 204
    return jsonify({'success': True, 'data': [], 'count': 0})

# ===== API CẬP NHẬT PROFILE =====
@app.route('/api/profile/<user_id>', methods=['PUT', 'OPTIONS'])
def update_profile(user_id):
    if request.method == 'OPTIONS':
        return '', 204
    return jsonify({'success': True, 'message': 'Đã cập nhật thông tin'})

# ===== API ĐỔI MẬT KHẨU =====
@app.route('/api/change-password', methods=['POST', 'OPTIONS'])
def change_password():
    if request.method == 'OPTIONS':
        return '', 204
    return jsonify({'success': True, 'message': 'Đã đổi mật khẩu thành công'})

# ===== ĐĂNG KÝ SINH VIÊN =====
@app.route('/api/students/register', methods=['POST', 'OPTIONS'])
def register_student():
    if request.method == 'OPTIONS':
        return '', 204
    return jsonify({'success': True, 'message': 'Đăng ký thành công'})

# ===== ERROR HANDLERS =====
@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'message': 'Endpoint không tồn tại'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'message': 'Lỗi server nội bộ'}), 500

# ===== KHỞI ĐỘNG SERVER =====
if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Flask API Server - QLTT Lớp học (Demo Mode)")
    print("=" * 60)
    print("📡 API: http://localhost:5000")
    print("🌐 Frontend: http://localhost:5000/login.html")
    print("✅ Chạy ở chế độ demo - không cần database")
    print("=" * 60)
    app.run(debug=True, port=5000, host='0.0.0.0')