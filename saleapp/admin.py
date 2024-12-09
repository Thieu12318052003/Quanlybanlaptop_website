from flask_admin.contrib.sqla import ModelView
from saleapp import admin, db
from flask import redirect, url_for, flash, jsonify, Response
import json
from saleapp.models import *

class ProductView(ModelView):
    column_display_pk = True
    can_view_details = True
    edit_modal = True
    details_modal = True
    create_modal = True
    can_export = True
    column_labels = {
        'TenLapTop': 'Tên Laptop',
        'Ram': 'RAM',
        'Cpu': 'CPU',
        'OCung': 'Ổ Cứng',
        'KichThuocMH': 'Kích Thước Màn Hình',
        'DoPhanGiai': 'Độ Phân Giải',
        'CardDoHoa': 'Card Đồ Họa',
        'DonGiaNhap': 'Đơn Giá Nhập',
        'DonGiaBan': 'Đơn Giá Bán',
        'SoLuong': 'Số Lượng',
        'Anh': 'Ảnh',
        'NSX_id': 'id Nhà Sản Xuất'
    }
    column_list = ('id', 'MaLapTop', 'TenLapTop', 'Ram', 'Cpu', 'OCung', 'KichThuocMH', 'DoPhanGiai', 'CardDoHoa', 'DonGiaNhap', 'DonGiaBan', 'SoLuong', 'Anh', 'NSX_id')
    form_columns = ('MaLapTop', 'TenLapTop', 'Ram', 'Cpu', 'OCung', 'KichThuocMH', 'DoPhanGiai', 'CardDoHoa', 'DonGiaNhap', 'DonGiaBan', 'SoLuong', 'Anh', 'NSX_id')


# Register the views

admin.add_view(ProductView(LapTop, db.session, name='LapTop'))
# Additional registrations for other models...

class NSXView(ModelView):
    column_display_pk = True
    can_view_details = True
    edit_modal = True
    details_modal = True
    create_modal = True
    can_export = True
admin.add_view(NSXView(NSX, db.session, name='NSX'))


admin.add_view(ModelView(HoadonChitiet, db.session, name='HoadonChitiet'))

class HoadonView(ModelView):
    column_display_pk = True
    can_view_details = True
    edit_modal = True
    details_modal = True
    create_modal = True
    can_export = True
    column_labels = {
        'id' : 'id',
        'create_date':'ngày thành lập',
        'user_id':'id người dùng'
    }
    column_list = (
    'id','create_date','user_id')
    form_columns = (
    'id', 'create_date', 'user_id'
    )




admin.add_view(HoadonView(Hoadon, db.session, name='Hoadon'))


# class HoadonChitietView(ModelView):
#     column_display_pk = True
#     can_view_details = True
#     edit_modal = True
#     details_modal = True
#     create_modal = True
#     can_export = True
#     column_labels = {
#         'hoadon_id': 'id hóa đơn',
#         'laptop_id': 'id laptop',
#         'quantity': 'Số lượng mua',
#         'Dongia': 'Đơn giá bán',
#         'tong_tien': 'Tổng tiền'
#     }
#     column_list = (
#         'hoadon_id', 'laptop_id', 'quantity', 'Dongia', 'tong_tien')
#     form_columns = (
#         'hoadon_id', 'laptop_id', 'quantity', 'Dongia')
#
#     def _tong_tien_formatter(view, context, model, name):
#         return model.tong_tien
#
#     column_formatters = {
#         'tong_tien': _tong_tien_formatter
#     }
#
# admin.add_view(HoadonChitietView(HoadonChitiet, db.session, name='Hóa đơn chi tiết'))
