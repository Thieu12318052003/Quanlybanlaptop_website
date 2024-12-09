from flask import Flask,send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer,Boolean ,String, Float,Enum ,ForeignKey,LargeBinary,DateTime
from saleapp.__init__ import *
from datetime import  datetime
from enum import  Enum as  UserEnum
# from docx import Document
from sqlalchemy.orm import relationship
from flask_login import UserMixin

#
# class tblChiTietHDN(db.Model):
#     __tablename__ = 'tblChiTietHDN'
#     SoHDN = db.Column(Integer, primary_key=True, nullable=True)
#     MaLapTop = db.Column(String(10), db.ForeignKey('tblLapTop.MaLapTop'), primary_key=True, nullable=False)
#     SLNhap = db.Column(Integer, nullable=True)
#     KhuyenMai = db.Column(Float, nullable=True)
#
# class tblChiTietHDB(db.Model):
#     __tablename__ = 'tblChiTietHDB'
#     SoHDB = db.Column(Integer, primary_key=True, nullable=False)
#     MaLapTop = db.Column(String(10), db.ForeignKey('tblLapTop.MaLapTop'), primary_key=True, nullable=False)
#     SLBan = db.Column(Integer, nullable=True)
#     KhuyenMai = db.Column(Float, nullable=True)
#
# class tblHoaDonNhap(db.Model):
#     __tablename__ = 'tblHoaDonNhap'
#     SoHDN = db.Column(Integer, primary_key=True, nullable=False)
#     MaNV = db.Column(String(10), db.ForeignKey('tblNhanVien.MaNV'), nullable=True)
#     NgayBan = db.Column(DateTime, nullable=True)
#     MaNCC = db.Column(String(10), db.ForeignKey('tblNCC.MaNCC'), nullable=True)
#
# class tblHoaDonBan(db.Model):
#     __tablename__ = 'tblHoaDonBan'
#     SoHDB = db.Column(Integer, primary_key=True, nullable=False)
#     MaNV = db.Column(String(10), db.ForeignKey('tblNhanVien.MaNV'), nullable=True)
#     NgayBan = db.Column(DateTime, nullable=True)
#     MaKH = db.Column(String(10), db.ForeignKey('tblKhachHang.MaKH'), nullable=True)

# class KhachHang(db.Model):
#     __tablename__ = 'KhachHang'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     MaKH = db.Column(String(10), nullable=False)
#     TenKH = db.Column(String(100), nullable=True)
#     DiaChi = db.Column(String(100), nullable=True)
#     SDTKH = db.Column(Integer, nullable=True)
# #
# class tblNhanVien(db.Model):
#     __tablename__ = 'tblNhanVien'
#     MaNV = db.Column(String(10), primary_key=True, nullable=False)
#     TenNV = db.Column(String(100), nullable=True)
#     GioiTinh = db.Column(String(100), nullable=True)
#     DiaChi = db.Column(String(100), nullable=True)
#     NgaySinh = db.Column(DateTime, nullable=True)
#     SDTNV = db.Column(Integer, nullable=True)
#
#
# class tblNCC(db.Model):
#     __tablename__ = 'tblNCC'
#     MaNCC = db.Column(String(10), primary_key=True, nullable=False)
#     TenNCC = db.Column(String(100), nullable=True)
#     hoadonnhaps = db.relationship('tblHoaDonNhap', backref='ncc', lazy=True)


class User(db.Model, UserMixin):#da ke thua
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(String(100), nullable=False)
    Username = db.Column(String(100), nullable=False, unique=True)
    Password = db.Column(String(100), nullable=False)
    Email = db.Column(String(100))
    Active = db.Column(Boolean, default= True)
    Ngay_laptk= db.Column(DateTime, default = datetime.now())
    # user_role = db.Column(Enum(UserRole), default=UserRole.USER)
    is_admin = db.Column(db.Boolean, default=False)  # Thêm trường is_admin
    hoadon = relationship('Hoadon', backref='user', lazy=True)


    def __str__(self):
        return self.name
class NSX(db.Model):
    __tablename__ = 'NSX'
    id = Column(Integer, primary_key=True, autoincrement=True)
    TenNSX = Column(String(100), unique=True, nullable=False)
    laptops = relationship('LapTop', backref='NSX', lazy=True)

    def __str__(self):
        return self.TenNSX

class LapTop(db.Model):
    __tablename__ = 'LapTop'
    id = Column(Integer, primary_key=True, autoincrement=True)
    MaLapTop = Column(String(10), unique=True, nullable=False)
    TenLapTop = Column(String(100), unique=True, nullable=False)
    Ram = Column(String(100))
    Cpu = Column(String(100))
    OCung = Column(String(100))
    KichThuocMH = Column(String(100))
    DoPhanGiai = Column(String(100))
    CardDoHoa = Column(String(100))
    DonGiaNhap = Column(Float)
    DonGiaBan = Column(Float)
    SoLuong = Column(Integer, default=0)
    Anh = Column(db.String(100))
    NSX_id = Column(Integer, ForeignKey(NSX.id), nullable=False)
    receipt_details = relationship('HoadonChitiet', backref='laptop', lazy=True)

    def __str__(self):
        return self.NSX.TenNSX

class Hoadon(db.Model): #Hoa don
    __tablename__ = 'Hoadon'
    id = Column(db.Integer, primary_key=True, autoincrement=True)
    create_date = Column(DateTime,default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('HoadonChitiet', backref='hoadon', lazy=True)


class HoadonChitiet(db.Model):#Chi tiet hoa don

    __tablename__ = 'HoadonChitiet'

    hoadon_id = Column(Integer , ForeignKey('Hoadon.id'), nullable=False ,primary_key=True)
    laptop_id = Column(Integer, ForeignKey('LapTop.id'), nullable=False, primary_key=True) #product
    quantity = Column(Integer, default=0)
    Dongia = Column(Float , default=0) #unit_price

    @property
    def tong_tien(self):
        return self.quantity * self.Dongia

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
