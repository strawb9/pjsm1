from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from StudentManage import db, app
from flask_login import UserMixin
import enum
import hashlib


class Base(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

class UserRoleEnum(enum.Enum):
    ADMIN = 1
    STAFF = 2
    TEACHER = 3

class User(Base, UserMixin):
    hoTen_u = Column(String(50), nullable=False)
    gioiTinh_u = Column(Boolean)
    email_u = Column(String(50), nullable=False, unique=True)
    sdt_u = Column(String(12), nullable=False)
    matKhau_u = Column(String(50), nullable=False)
    tenDangNhap = Column(String(150), nullable=False, unique=True)#unique giong primarykey nhung duoc phep thay doi
    user_role = Column(Enum(UserRoleEnum))


    def __str__(self):
        self.name


class QuanTriVien(User):
    admin_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id), unique=True)
    vaiTro = Column(String(50), nullable=False)


class NhanVienTruong(User):
    nv_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id), unique=True)
    vaiTro = Column(String(50), nullable=False)

class QuyDinh(Base):
    tenQD=Column(String(50),nullable=False)
    moTa = Column(String(50), nullable=False)


class Khoi(db.Model):
    __tablename__ = 'Khoi'
    khoi_id = Column(Integer, primary_key=True, autoincrement=True)
    tenKhoi = Column(Enum('Grade 10', 'Grade 11', 'Grade 12'), nullable=False)
    classes = relationship('Lop', backref='Khoi', lazy=True)
    students = relationship('HocSinh', backref='Khoi', lazy=True)


class Lop(db.Model):
    __tablename__ = 'Lop'
    lop_id = Column(Integer, primary_key=True, autoincrement=True)
    tenLop = Column(String(50), nullable=False)
    khoi_id = Column(Integer, ForeignKey(Khoi.khoi_id), nullable=False)
    students = relationship('HocSinh', backref='Lop', lazy=True)

class HocKi(db.Model):
    __tablename__ = 'HocKi'
    hocki_id = Column(Integer, primary_key=True, autoincrement=True)
    tenHK = Column(String(50), nullable=False)
    tests = relationship('Test', backref='Semester', lazy=True)


class HocSinh(db.Model):
    __tablename__ = 'HocSinh'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenHs = Column(String(50), nullable=False)
    gioiTinh = Column(Enum('Nam', 'Nữ'), nullable=False)
    ngaysinh = Column(DateTime, nullable=False)
    diaChi = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False)
    khoi_id = Column(Integer, ForeignKey(Khoi.khoi_id), nullable=False)
    tests = relationship('Test', backref='HocSinh', lazy=True)
    lop_id = Column(Integer, ForeignKey(Lop.lop_id), nullable=True)


class MonHoc(db.Model):
    __tablename__ = 'MonHoc'
    monHoc_id = Column(Integer, primary_key=True, autoincrement=True)
    tenMH = Column(String(100), nullable=False)
    tests = relationship('Test', backref='MonHoc', lazy=True)
    teachers = relationship('GiaoVien', backref='MonHoc', lazy=True)


class GiaoVien(db.Model):
    __tablename__ = 'GiaoVien'
    giaoVien_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id), unique=True)
    boMon = Column(String(50), nullable=False)
    tenGV = Column(String(50), nullable=False)
    monHoc_id = Column(Integer, ForeignKey(MonHoc.monHoc_id), nullable=False)


class Test(db.Model):
    __tablename__ = 'Test'
    id_test = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum('15 phút', '1 tiết', 'Cuối kỳ'), nullable=False)
    diemm = Column(Float, nullable=False)
    hs_id = Column(Integer, ForeignKey(HocSinh.id), nullable=False)
    monHoc_id = Column(Integer, ForeignKey(MonHoc.monHoc_id), nullable=False)
    hocki_id = Column(Integer, ForeignKey(HocKi.hocki_id), nullable=False)


lop_giaovien = db.Table('lop_giaovien',
                        Column('lop_id', Integer, ForeignKey(HocSinh.id), primary_key=True),
                        Column('giaoVien_id', Integer, ForeignKey(GiaoVien.giaoVien_id), primary_key=True))

hocsinh_giaovien = db.Table('hocsinh_monhoc',
                            Column('hs_id', Integer, ForeignKey(HocSinh.id), primary_key=True),
                            Column('monHoc_id', Integer, ForeignKey(MonHoc.monHoc_id), primary_key=True))

hs_lop = db.Table('hs_lop',
                  Column('hs_id', Integer, ForeignKey(HocSinh.id), primary_key=True),
                  Column('lop_id', Integer, ForeignKey(Lop.lop_id), primary_key=True))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        u1 = User(hoTen_u="Diem", gioiTinh_u=0, email_u="diem@gmail.com", sdt_u="093444111",
                  matKhau_u=str(hashlib.md5('123'.strip().encode('utf-8')).hexdigest()), tenDangNhap='diem',
                  user_role='TEACHER')
        u2 = User(hoTen_u="Yen", gioiTinh_u=0, email_u="Yen@gmail.com", sdt_u="093412344",
                  matKhau_u=str(hashlib.md5('123'.strip().encode('utf-8')).hexdigest()), tenDangNhap='yen',
                  user_role='ADMIN')
        u3 = User(hoTen_u="Duy", gioiTinh_u=1, email_u="duy@gmail.com", sdt_u="093412322",
                  matKhau_u=str(hashlib.md5('123'.strip().encode('utf-8')).hexdigest()), tenDangNhap='duy',
                  user_role='STAFF')
        db.session.add_all([u1, u2, u3])
        db.session.commit()

        grade1 = Khoi(tenKhoi='Grade 10')
        grade2 = Khoi(tenKhoi='Grade 11')
        grade3 = Khoi(tenKhoi='Grade 12')
        db.session.add_all([grade1, grade2, grade3])
        db.session.commit()

        c1 = Lop(tenLop='10A1', khoi_id=1)
        c2 = Lop(tenLop='10A2', khoi_id=1)
        c3 = Lop(tenLop='10A3', khoi_id=1)
        c4 = Lop(tenLop='11A1', khoi_id=2)
        c5 = Lop(tenLop='11A2', khoi_id=2)
        c6 = Lop(tenLop='11A3', khoi_id=2)
        c7 = Lop(tenLop='12A1', khoi_id=3)
        c8 = Lop(tenLop='12A2', khoi_id=3)
        c9 = Lop(tenLop='12A3', khoi_id=3)
        db.session.add_all([c1, c2, c3, c4, c5, c6, c7, c8, c9])
        db.session.commit()

        s1 = MonHoc(tenMH="Ngữ văn")
        s2 = MonHoc(tenMH="Toán")
        s3 = MonHoc(tenMH="Ngoại ngữ")
        s4 = MonHoc(tenMH="Vật lý")
        s5 = MonHoc(tenMH="Hóa học")
        s6 = MonHoc(tenMH="Sinh học")
        s7 = MonHoc(tenMH="Lịch sử")
        s8 = MonHoc(tenMH="Địa lý")
        s9 = MonHoc(tenMH="Giáo dục công dân")
        s10 = MonHoc(tenMH="Tin học")
        s11 = MonHoc(tenMH="Giáo dục quốc phòng và an ninh")
        s12 = MonHoc(tenMH="Công nghệ")
        db.session.add_all([s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12])
        db.session.commit()

        s1 = HocKi(tenHK="Học kỳ 1 năm học 2021-2022")
        s2 = HocKi(tenHK="Học kỳ 2 năm học 2021-2022")
        s3 = HocKi(tenHK="Học kỳ 1 năm học 2022-2023")
        s4 = HocKi(tenHK="Học kỳ 2 năm học 2022-2023")
        s5 = HocKi(tenHK="Học kỳ 1 năm học 2023-2024")
        s6 = HocKi(tenHK="Học kỳ 2 năm học 2023-2024")
        s7 = HocKi(tenHK="Học kỳ 1 năm học 2024-2025")
        s8 = HocKi(tenHK="Học kỳ 2 năm học 2024-2025")
        db.session.add_all([s1, s2, s3, s4, s5, s6, s7, s8])
        db.session.commit()
