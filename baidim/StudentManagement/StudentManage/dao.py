from StudentManage.models import *
from StudentManage import app, login
import hashlib
from sqlalchemy import func
from flask import jsonify
from flask_login import login_user, current_user, logout_user


def check_login(username, password, role):
    return User.query.filter(User.tenDangNhap.__eq__(username),
                             User.matKhau_u.__eq__(password),
                             User.user_role.__eq__(role)).first()


def add_user(name, role, password, email, sdt, gioi_tinh, full_name):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(tenDangNhap=name,
             user_role=role,
             matKhau_u=password,
             email_u=email,
             gioiTinh_u=gioi_tinh,
             sdt_u=sdt,
             hoTen_u=full_name)
    db.session.add(u)
    db.session.commit()
    return u


@login.user_loader
def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_lop():
    return Lop.query.all()


def get_class_by_id_grade(khoi_id):
    return Lop.query.filter(Lop.khoi_id.__eq__(khoi_id)).all()


def get_class_by_id(lop_id):
    return Lop.query.filter(Lop.lop_id.__eq__(lop_id)).first()


def get_class_is_blank():
    classes = Lop.query.all()
    classes_blank = []
    for c in classes:
        if len(c.students) < app.config['soluong']:
            classes_blank.append(c)
    return classes_blank


def get_student_by_class(lop_id):
    return HocSinh.query.filter(HocSinh.lop_id.__eq__(lop_id)).all()


def get_student():
    return HocSinh.query.all()


def get_student_by_name(tenHs):
    return HocSinh.query.filter(HocSinh.tenHs.icontains(tenHs)).all()


def get_student_by_id(id):
    return HocSinh.query.get(id)


def get_student_by_id_grade(khoi_id):
    return HocSinh.query.filter(HocSinh.khoi_id == khoi_id).all()


def get_monhoc():
    return MonHoc.query.all()


def get_subject_by_id(id):
    return MonHoc.query.filter(MonHoc.monHoc_id == id).first()


def get_hocki():
    return HocKi.query.all()


def get_semester_by_id(id):
    return HocKi.query.filter(HocKi.hocki_id == id).first()


def get_khoi():
    return Khoi.query.all()

def get_subject_report(subject_id, semester_id):
    """
    Trả về báo cáo tổng kết môn học.
    """
    from sqlalchemy.sql import func, case
    from StudentManage.models import Test, HocSinh, Lop

    # Truy vấn dữ liệu
    data = db.session.query(
        Lop.tenLop.label('lop'),
        func.count(Test.hs_id).label('si_so'),
        func.sum(case([(Test.diemm >= 5, 1)], else_=0)).label('so_luong_dat')
    ).join(HocSinh, HocSinh.id == Test.hs_id) \
     .join(Lop, Lop.lop_id == HocSinh.lop_id) \
     .filter(Test.monHoc_id == subject_id, Test.hocki_id == semester_id) \
     .group_by(Lop.tenLop).all()

    # Tính tỷ lệ và định dạng kết quả
    result = []
    for row in data:
        ty_le = (row.so_luong_dat / row.si_so) * 100 if row.si_so > 0 else 0
        result.append({
            'lop': row.lop,
            'si_so': row.si_so,
            'so_luong_dat': row.so_luong_dat,
            'ty_le': round(ty_le, 2)
        })
    return result

app.jinja_env.globals.update(enumerate=enumerate)



def calc_semester_score_average(lop_id, hocki_id):
    student = get_student_by_class(lop_id)
    subjects = get_monhoc()

    scores = {}

    # Initialize scores for each student
    for i in range(len(student)):
        scores[i] = {
            'hs_id': student[i].id,
            'diemm': 0,
            'count': 0
        }

    for subject in subjects:

        test_15m = db.session.query(Test.hs_id, func.sum(Test.diemm), func.count(Test.diemm)) \
            .join(HocSinh, HocSinh.id == Test.hs_id) \
            .filter(Test.hocki_id == hocki_id, Test.monHoc_id == subject.monHoc_id,
                    HocSinh.lop_id == lop_id, Test.type == '15 phút') \
            .group_by(Test.hs_id).all()

        test_45m = db.session.query(Test.hs_id, func.sum(Test.diemm), func.count(Test.diemm)) \
            .join(HocSinh, HocSinh.id == Test.hs_id) \
            .filter(Test.hocki_id == hocki_id, Test.monHoc_id == subject.monHoc_id,
                    HocSinh.lop_id == lop_id, Test.type == '1 tiết') \
            .group_by(Test.hs_id).all()

        test_final = db.session.query(Test.hs_id, func.sum(Test.diemm), func.count(Test.diemm)) \
            .join(HocSinh, HocSinh.id == Test.hs_id) \
            .filter(Test.hocki_id == hocki_id, Test.monHoc_id == subject.monHoc_id,
                    HocSinh.lop_id == lop_id, Test.type == 'Cuối kỳ') \
            .group_by(Test.hs_id).all()

        for i in range(len(scores)):
            hs_id = scores[i]['hs_id']
            score_15m = next((s for s in test_15m if s[0] == hs_id), None)
            score_45m = next((s for s in test_45m if s[0] == hs_id), None)
            score_final = next((s for s in test_final if s[0] == hs_id), None)

            if score_15m and score_45m and score_final:

                a = float(score_15m[1])
                b = float(score_45m[1])
                c = float(score_final[1])
                x = int(score_15m[2])
                y = int(score_45m[2])
                z = int(score_final[2])

                total_weighted_score = (a + b * 2 + c * 3)
                total_count = (x + y * 2 + z * 3)

                if total_count > 0:
                    average_score = round(total_weighted_score / total_count, 1)
                    scores[i]['diemm'] += average_score
                    scores[i]['count'] += 1

    for i in range(len(scores)):
        if scores[i]['count'] != 0:
            scores[i]['diemm'] = round(scores[i]['diemm'] / scores[i]['count'], 1)
        else:
            scores[i]['diemm'] = 0

    return scores


def create_class_list():
    grade = get_khoi()
    for g in grade:
        students = get_student_by_id_grade(g.khoi_id)
        classes = get_class_by_id_grade(g.khoi_id)
        i = 0
        for s in students:
            if s.lop_id:
                continue
            else:
                s.lop_id = classes[i].lop_id
                db.session.commit()
                i = i + 1
            if i == len(classes):
                i = 0
    return get_student()
