import json
import os
from saleapp import app, db
from saleapp.models import *  # Correct import from models
import hashlib
from flask_login import current_user


def load_tblLapTop():
    return LapTop.query.all()
def load_tblNSX():
    return NSX.query.all()

def loadLapTop_NSX(idNSX=None, kw=None, ram=None, cpu=None, ktmh=None, gia=None, giakhoang=None, page=1):
    from sqlalchemy.orm import joinedload
    laptop = LapTop.query.options(joinedload(LapTop.NSX))
    if idNSX:
        laptop = laptop.filter(LapTop.NSX_id == idNSX)
    if kw:
        laptop = laptop.filter(LapTop.TenLapTop.contains(kw))
    if ram:
        laptop = laptop.filter(LapTop.Ram == ram)
    if cpu:
        laptop = laptop.filter(LapTop.Cpu == cpu)
    if ktmh:
        laptop = laptop.filter(LapTop.KichThuocMH == ktmh)
    if gia:
        laptop = laptop.filter(LapTop.DonGiaBan >= gia)
    if giakhoang:
        laptop = laptop.filter(LapTop.DonGiaBan <= giakhoang)

    page_size=app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    end = start + page_size

    return laptop.slice(start, end).all()
def getlaptop_byid(laptop_id):
    return LapTop.query.get(laptop_id)
def getNSX_byid(NSX_id):
    return NSX.query.get(NSX_id)
def get_user_by_id(User_id):
    return User.query.get(User_id)
def add_user(Name, Username, Password, **kwargs):
    user = User(Name=Name.strip() ,
                Username=Username.strip(),
                Password=Password,
                Email=kwargs.get('Email'))

    db.session.add(user)
    db.session.commit()

def check_login(Username, Password):
    if Username and Password:
        user = User.query.filter_by(Username=Username.strip()).first()
        if user and user.Password == Password.strip():
            return user
    return None
def count_cart(cart):
    total_quantity, total_amount = 0, 0

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_amount += c['quantity'] * c['DonGiaBan']

    return {
        'total_quantity': total_quantity,
        "total_amount": total_amount
    }

import logging

def add_hoadon(cart): #add receipt
    if cart:
        try:
            hoadon = Hoadon(user_id=current_user.id)
            db.session.add(hoadon)
            db.session.commit()

            for c in cart.values():
                chitiet = HoadonChitiet(
                    hoadon_id=hoadon.id,
                    laptop_id=c['id'],
                    quantity=c['quantity'],
                    Dongia=c['DonGiaBan']
                )
                db.session.add(chitiet)
            db.session.commit()

        except Exception as e:
            logging.error(f"Error adding receipt to database: {e}")
            db.session.rollback()

def display_all_laptops():
    laptops = LapTop.get_all_laptops()
    for laptop in laptops:
        print(f"ID: {laptop.id}, MaLapTop: {laptop.MaLapTop}, Ten: {laptop.Ten}, Ram: {laptop.Ram}, Cpu: {laptop.Cpu}, OCung: {laptop.OCung}, KichThuocMH: {laptop.KichThuocMH}, DoPhanGiai: {laptop.DoPhanGiai}, CardDoHoa: {laptop.CardDoHoa}, MaNSX: {laptop.MaNSX}, DonGiaNhap: {laptop.DonGiaNhap}, DonGiaBan: {laptop.DonGiaBan}, SoLuong: {laptop.SoLuong}, Anh: {laptop.Anh}")

def serialize(model):
    return {column.name: getattr(model, column.name) for column in model.__table__.columns}
def serialize(model):
    return {column.name: getattr(model, column.name) for column in model.__table__.columns}

# def create_docx(data):
#     document = Document()
#     document.add_heading('Database Export', 0)
#
#     for table_name, records in data.items():
#         document.add_heading(table_name, level=1)
#         for record in records:
#             for key, value in record.items():
#                 document.add_paragraph(f'{key}: {value}')
#             document.add_paragraph()
#
#     return document



# def display_all_laptops():
#     laptops = LapTop.get_all_laptops()
#     for laptop in laptops:
#         print(f"ID: {laptop.id}, MaLapTop: {laptop.MaLapTop}, Ten: {laptop.Ten}, Ram: {laptop.Ram}, Cpu: {laptop.Cpu}, OCung: {laptop.OCung}, KichThuocMH: {laptop.KichThuocMH}, DoPhanGiai: {laptop.DoPhanGiai}, CardDoHoa: {laptop.CardDoHoa}, MaNSX: {laptop.MaNSX}, DonGiaNhap: {laptop.DonGiaNhap}, DonGiaBan: {laptop.DonGiaBan}, SoLuong: {laptop.SoLuong}, Anh: {laptop.Anh}")

if __name__ == "__main__":
    with app.app_context():
        load_tblLapTop()
