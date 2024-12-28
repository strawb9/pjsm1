from flask import render_template, request, redirect, session, jsonify
from flask_admin import expose

from StudentManage import app, login, db, utils
from StudentManage.models import *
import dao
from flask_login import login_user, current_user, logout_user
from StudentManage import admin
import string
from datetime import datetime





@app.route('/', methods=['get'])
def home():
    return render_template('home.html')


@app.route('/nhanvien')
def nhanvien():
    return render_template('staff.html')


@app.route('/giaovien')
def giaovien():
    return render_template('teacher.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/login', methods=['post', 'get'])
def signin():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        if role:
            if role.__eq__('GIAOVIEN'):
                role = UserRoleEnum.TEACHER
                u = dao.check_login(username=username, password=password, role=role)
                login_user(u)
                return redirect('/giaovien')
            else:
                if role.__eq__('ADMIN'):
                    role = UserRoleEnum.ADMIN
                    u = dao.check_login(username=username, password=password, role=role)
                    login_user(u)
                    return redirect('/admin')
                else:
                    role = UserRoleEnum.STAFF
                    u = dao.check_login(username=username, password=password, role=role)
                    login_user(u)
                    return redirect('/nhanvien')
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


@app.route("/Nhapdiem")
def Nhapdiemm():
    return render_template('NhapDiem.html', classes=dao.get_lop(), subjects=dao.get_monhoc(), semesters=dao.get_hocki())


@app.route("/Xuatdiem")
def Xuatdiem():
    return render_template('XuatDiem.html', classes=dao.get_lop(), semesters=dao.get_hocki())


@app.route("/Themhocsinh")
def Themhocsinh():
    return render_template('tiepnhan.html')


@app.route("/Taodanhsach")
def Taodanhsach():
    student = dao.create_class_list()
    classes = dao.get_lop()

    return render_template('taodanhsachlop.html', classes=classes)


@app.route("/Dieuchinhlop")
def Dieuchinhlop():
    return render_template('dieuchinhlop.html', classes=dao.get_class_is_blank())


@app.route("/ThemHocSinh", methods=['POST'])
def ThemHocSinh():
    err_msg = ''
    if request.method.__eq__('POST'):
        tenHs = request.form.get('tenHs')
        gioiTinh = request.form.get('gioiTinh')
        ngaysinh = request.form.get('ngaysinh')
        diaChi = str(request.form.get('diaChi'))
        phone = request.form.get('phone')
        email = request.form.get('email')
        khoi = request.form.get('khoi')
        substring = email[(len(email) - 10):]
        if len(phone) != 10:
            err_msg = 'Số điện thoại sai. Vui lòng nhập lại!'
            return render_template('tiepnhan.html', err_msg=err_msg)
        if not substring.__eq__('@gmail.com'):
            err_msg = 'Email sai. Vui lòng nhập lại!'
            return render_template('tiepnhan.html', err_msg=err_msg)
        try:
            birthdate = datetime.strptime(ngaysinh, '%Y-%m-%d')
        except:
            err_msg = 'Bạn chưa nhập ngày sinh. Vui lòng thử lại!'
            return render_template('tiepnhan.html', err_msg=err_msg)
        if (app.config['nambatdau'] - birthdate.year) < app.config['mintuoi'] or (
                app.config['nambatdau'] - birthdate.year) > app.config['maxtuoi']:
            err_msg = 'Ngày sinh không hợp lệ. Vui lòng thử lại!'
            return render_template('tiepnhan.html', err_msg=err_msg)

        student = HocSinh(tenHs=tenHs, gioiTinh=gioiTinh, ngaysinh=ngaysinh, diaChi=diaChi, phone=phone,
                          email=email, khoi_id=khoi)
        db.session.add(student)
        db.session.commit()
        err_msg = 'Lưu thành công'
        return render_template('tiepnhan.html', err_msg=err_msg)


@app.route("/api/Timkiemhs", methods=['POST'])
def Timkiemhs():
    if request.method.__eq__('POST'):
        name = request.json.get('timkiemhs')
        students = dao.get_student_by_name(name)
        stu = {}
        stu[0] = {"quantity": len(students)}

        for i in range(1, len(students) + 1):
            if students[i - 1].lop_id:
                stu[i] = {
                    "id": students[i - 1].id,
                    "tenHs": students[i - 1].tenHs,
                    "lop": students[i - 1].Lop.tenLop
                }
            else:
                stu[i] = {
                    "id": students[i - 1].id,
                    "tenHs": students[i - 1].tenHs,
                    "lop": "Chưa có lớp"
                }

        return stu


@app.route('/api/Chuyenlop', methods=['post'])
def Chuyenlop():
    hs_id = request.json.get('hs_id')
    lop_id = request.json.get('lop_id')
    student = dao.get_student_by_id(hs_id)
    lop = dao.get_class_by_id(lop_id)
    blank_class = dao.get_class_is_blank()

    if not student:
        return jsonify({'content': 'ID học sinh không tồn tại. Vui lòng kiểm tra lại'})

    if not lop:
        return jsonify({'content': 'ID lớp học không tồn tại. Vui lòng kiểm tra lại'})

    if not lop in blank_class:
        return jsonify({'content': 'Lớp học đã đầy. Vui lòng chọn lớp khác'})

    if student.khoi_id == lop.khoi_id:
        student.lop_id = lop.lop_id
        db.session.commit()
        return jsonify({'content': 'Thành công'})
    else:
        return jsonify({'content': 'Lớp chuyển đến không thuộc khối của học sinh'})


@app.route('/api/Xuatlop', methods=['post'])
def Xuatlop():
    lop_id = request.json.get('lop_id')
    classes = dao.get_class_by_id(lop_id)
    students = dao.get_student_by_class(lop_id)
    stu = {}

    stu[0] = {
        "id": classes.lop_id,
        "class": classes.tenLop,
        "quantity": len(students)
    }

    for i in range(1, len(students) + 1):
        stu[i] = {
            "tenHs": students[i - 1].tenHs,
            "gioiTinh": students[i - 1].gioiTinh,
            "ngaysinh": students[i - 1].ngaysinh.strftime("%d/%m/%Y"),
            "diaChi": students[i - 1].diaChi
        }

    return stu


@app.route('/api/Timkiemlop', methods=['post'])
def Timkiemlop():
    lop_id = request.json.get('timkiemlop')
    students = dao.get_student_by_class(lop_id)
    stu = {}

    stu[0] = {
        "tenLop": students[0].Lop.tenLop,
        "num_row_15m": request.json.get('num_row_15m'),
        "num_row_45m": request.json.get('num_row_45m'),
        "quantity": len(students)
    }

    for i in range(1, len(students) + 1):
        stu[i] = {
            "id": students[i - 1].id,
            "name": students[i - 1].tenHs
        }

    session['num_test'] = {"num_row_15m": request.json.get('num_row_15m'),
                           "num_row_45m": request.json.get('num_row_45m'), "lop_id": lop_id}

    return stu


@app.route('/api/Luudiem', methods=['post'])
def Luudiem():
    stu = request.json.get('scores')
    monHoc_id = request.json.get('monHoc_id')
    hocki_id = request.json.get('hocki_id')
    num_row_15m = len(session['num_test']['num_row_15m'])
    num_row_45m = len(session['num_test']['num_row_45m'])
    student = dao.get_student_by_class(session['num_test']['lop_id'])

    for i in range(len(stu)):
        for j in range(num_row_15m + num_row_45m + 1):
            if not stu[i][j]:
                return jsonify({'content': 'Có học sinh chưa nhập điểm. Vui lòng kiểm tra lại!'})
            elif float(stu[i][j]) > 10 or float(stu[i][j]) < 0:
                return jsonify({'content': 'Điểm không hợp lệ. Vui lòng kiểm tra lại!'})

    for s in student:
        tests = Test.query.filter(Test.hs_id == s.id, Test.monHoc_id == monHoc_id, Test.hocki_id == hocki_id).all()
        for t in tests:
            db.session.delete(t)
            db.session.commit()

    for i in range(len(stu)):
        for j in range(num_row_15m + num_row_45m + 1):
            type = ''
            if j < num_row_15m:
                type = '15 phút'
            elif j < (num_row_15m + num_row_45m):
                type = '1 tiết'
            else:
                type = 'Cuối kỳ'
            test = Test(type=type, diemm=round(float(stu[i][j]), 1), hs_id=student[i].id,
                        monHoc_id=monHoc_id, hocki_id=hocki_id)
            db.session.add(test)
            db.session.commit()

    return jsonify({'content': 'Lưu thành công'})


@app.route('/api/Xuatdiemm', methods=['post'])
def Xuatdiemm():
    lop_id = request.json.get('lop_id')
    hocki_id = request.json.get('hocki_id')
    semester_1 = dao.calc_semester_score_average(lop_id=lop_id, hocki_id=hocki_id)
    semester_2 = dao.calc_semester_score_average(lop_id=lop_id, hocki_id=int(hocki_id) + 1)
    schoolyear = ''
    if hocki_id == '1':
        schoolyear = 'Năm học 2020-2021'
    elif hocki_id == '3':
        schoolyear = 'Năm học 2021-2022'
    elif hocki_id == '5':
        schoolyear = 'Năm học 2022-2023'
    elif hocki_id == '7':
        schoolyear = 'Năm học 2023-2024'
    result = {}
    result[0] = {
        'quantity': len(semester_1),
        'class': dao.get_class_by_id(lop_id).tenLop,
        'schoolyear': schoolyear
    }
    for i in range(len(semester_1)):
        result[i + 1] = {
            'tenHs': dao.get_student_by_id(semester_1[i]['hs_id']).tenHs,
            'semester_1': semester_1[i]['diemm'],
            'semester_2': semester_2[i]['diemm']
        }

    return result


# @app.route("/api/statisticsScore", methods=['POST'])
# def StatisticsScore():
#     monHoc_id = request.json.get('monHoc_id')
#     hocki_id = request.json.get('hocki_id')
#     classes = dao.get_Lop()
#     semester = 0
#     schoolyear = ''
#     if int(hocki_id) % 2 == 0:
#         semester = 2
#     else:
#         semester = 1
#     if hocki_id == '1':
#         schoolyear = 'Năm học 2020-2021'
#     elif hocki_id == '3':
#         schoolyear = 'Năm học 2021-2022'
#     elif hocki_id == '5':
#         schoolyear = 'Năm học 2022-2023'
#     elif hocki_id == '7':
#         schoolyear = 'Năm học 2023-2024'
#     stu = {}
#     stu[0] = {
#         'monhoc': dao.get_subject_by_id(monHoc_id).tenMH,
#         'hocki': semester,
#         'schoolyear': schoolyear,
#         'quantity': len(classes)
#     }
#     for i in range(len(classes)):
#         statistics = dao.statistics_subject(lop_id=classes[i].lop_id, monHoc_id=monHoc_id, hocki_id=hocki_id)
#         count = 0
#         for j in range(len(statistics)):
#             if statistics[j]['score'] >= 5:
#                 count = count + 1
#         rate = 0
#         if len(statistics) == 0:
#             rate = 0
#         else:
#             rate = round(float(count / len(statistics) * 100), 1)
#         stu[i + 1] = {
#             'lop': classes[i].tenLop,
#             'quantity_student': len(statistics),
#             'quantity_passed': count,
#             'rate': rate
#         }
#     return stu
#
# @app.route("/api/Thaydoiqd", methods=['POST'])
# def Thaydoiqd():
#     quantity = int(request.json.get('quantity'))
#     min_age = int(request.json.get('min_age'))
#     max_age = int(request.json.get('max_age'))
#
#     if quantity <= 0 or min_age <= 0 or max_age <= 0:
#         return jsonify({'status': 200, 'content': 'Thông tin không hợp lệ. Vui lòng kiểm tra lại!'})
#     if min_age >= max_age:
#         return jsonify({'status': 200, 'content': 'Tuổi lớn nhất phải lớn hơn tuổi nhỏ nhất. Vui lòng kiểm tra lại!'})
#     lops = dao.get_lop()
#     max = 0
#     for c in lops:
#         student = dao.get_student_by_class(c.lop_id)
#         if max < len(student):
#             max = len(student)
#     if quantity < max:
#         return jsonify(
#             {'status': 200, 'content': str.format('Sĩ số tối đa phải lớn hơn {0}. Vui lòng kiểm tra lại!', max)})
#     app.config['soluong'] = quantity
#     app.config['mintuoi'] = min_age
#     app.config['maxtuoi'] = max_age
#     return jsonify({'status': 500, 'content': 'Thành công!'})


if __name__ == '__main__':
    app.run(debug=True)
