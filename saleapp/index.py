import math

from flask import render_template,request,session,jsonify
from saleapp import app

import utils
import flask,io
import pandas as pd
from saleapp.admin import *
from  flask_login import login_user, logout_user
from __init__ import db



@app.route('/admin1')
def admin():
    return render_template("admin.html")
@app.route('/laptop/<int:laptop_id>')
def laptop_details(laptop_id):
    laptop = utils.getlaptop_byid(laptop_id)
    nsx = utils.getNSX_byid(laptop.NSX_id)  # Fetch NSX object by its ID
    return render_template('products.html', laptop=laptop, nsx=nsx)

@app.route('/NSX/<int:nsx_id>')
def NSX_details(nsx_id):
    NSX = utils.getNSX_byid(nsx_id)
    return render_template('products.html', NSX=NSX)
@app.route('/')
def index():
    LT = utils.load_tblLapTop()
    NSX = utils.load_tblNSX()
    id = request.args.get("NSX_id")
    ram = request.args.get("Ram")
    cpu = request.args.get("Cpu")
    ktmh = request.args.get("KichThuocMH")
    search_kw = request.args.get("search_kw")
    gia = request.args.get("gia")
    giakhoang = request.args.get("giakhoang")
    page = request.args.get('page',1)
    # session['cart'] = {}

    laptops = utils.loadLapTop_NSX(idNSX=id, kw=search_kw, ram=ram, cpu=cpu, ktmh=ktmh, gia=gia, giakhoang=giakhoang, page=int(page))

    unique_ram_values = set(lt.Ram for lt in LT)
    unique_cpu_values = set(lt.Cpu for lt in LT)
    unique_ktmh_values = set(lt.KichThuocMH for lt in LT)
    return render_template("user/user.html",
                           LapTop=LT,
                           laptops=laptops,
                           NSX=NSX,
                           ram=ram,
                           unique_ram_values=unique_ram_values,
                           unique_cpu_values=unique_cpu_values,
                           unique_ktmh_values=unique_ktmh_values)
@app.route('/dangky', methods=['get','post'])
def user_dangky():
    err_msg = ""
    if request.method.__eq__('POST'):
        Name = request.form.get('Name')
        Username = request.form.get('Username')
        Password = request.form.get('Password')
        Email = request.form.get('Email')
        confirm = request.form.get('confirm')

        try:
            if Password.strip().__eq__(confirm.strip()):
                utils.add_user(Name=Name, Username=Username,Password=Password, Email=Email)
                return redirect(url_for('index'))

            else:
                err_msg = 'mat khau khong giong'
        except Exception as ex:
            err_msg = 'he thong dang co loi: ' + str(ex)

    return render_template('tester.html', err_msg=err_msg)
@app.route('/user-dangnhap', methods=['GET', 'POST'])
def user_dangnhap():
    err_msg = ''
    if request.method == 'POST':
        Username = request.form.get('Username')
        Password = request.form.get('Password')

        user = utils.check_login(Username=Username, Password=Password)



        if user:
            login_user(user=user)
            if user.is_admin:
                return redirect(url_for('admin.index'))  # Đường dẫn đến trang quản trị của Flask-Admin
            else:
                return redirect(url_for('index'))  # Đường dẫn đến trang chủ của người dùng thông thường


        if user:
            login_user(user=user)

            next = request.args.get('next', 'index')
            return redirect(url_for(next))
        else:
            err_msg = 'Username hoặc Password không chính xác'

    return render_template('dangnhap.html', err_msg=err_msg)

@login.user_loader #tu goi sau khi dang nhap thanh cong
def user_load(User_id):
    return utils.get_user_by_id(User_id=User_id)

@app.route('/api/add-cart', methods=['post']) #duong dan khop voi js
def add_to_card():
    data = request.json
    id = str(data.get('id'))
    MaLapTop = data.get('MaLapTop')
    TenLapTop =data.get('TenLapTop')
    DonGiaBan =data.get('DonGiaBan')
    Anh = data.get('Anh')


    cart = session.get('cart')
    if not cart:
        cart={}

    if id in cart:
        cart[id]['quantity'] = cart[id]['quantity'] + 1
    else:
        cart[id] = {
            'id':id,
            'MaLapTop': MaLapTop,
            'TenLapTop':TenLapTop,
            'DonGiaBan':DonGiaBan,
            'Anh':Anh,
            'quantity': 1
        }
    session['cart'] = cart #capnhat lai gio hang moi

    return jsonify(utils.count_cart(cart))

@app.route('/api/update-cart', methods=['put'])
def update_cart():
    data = request.json
    id = str(data.get('id'))
    quantity = data.get('quantity')

    cart = session.get('cart')
    if cart and id in cart:
        cart[id]['quantity'] = quantity
        session['cart'] = cart #capnhat lai gio hang moi

    return jsonify(utils.count_cart(cart))


@app.route('/api/delete-cart/<laptop_id>', methods=['delete'])
def delete_cart(laptop_id):
    cart = session.get('cart')

    if cart and laptop_id in cart:
        del cart[laptop_id]
        session['cart'] = cart #capnhat lai gio hang moi


    return jsonify(utils.count_cart(cart))


@app.route('/api/pay', methods = ['post'])
def Thanhtoan(): #Pay
    try:
        utils.add_hoadon(session.get('cart'))
        del session['cart']
    except:
        return jsonify({'code': 400})

    return jsonify({'code':200})



@app.route('/cart')
def cart():
   return render_template('cart.html',
                          stats=utils.count_cart(session.get('cart')))


@app.route('/dangxuat')
def user_dangxuat():
    logout_user()
    return redirect(url_for('user_dangnhap'))

@app.context_processor
def common_response():
    return {
        'NSX': utils.load_tblNSX(),
        'cart_stats': utils.count_cart(session.get('cart'))
    }
# @app.route('/admin/export_json')
# def export_json():
#     with app.app_context():
#         data = {
#             'LapTop': [serialize(dienthoai) for dienthoai in LapTop.query.all()]
#         }
#
#         # Create an in-memory file object
#         json_file = io.BytesIO()
#         json_file.write(json.dumps(data, default=str, indent=4).encode('utf-8'))
#         json_file.seek(0)
#
#         # Send the in-memory file as a response
#         return send_file(json_file, as_attachment=True, download_name='laptop.json', mimetype='application/json')

# @app.route('/admin/export_docx')
# def export_docx():
#     with app.app_context():
#         data = {
#             'LapTop': [serialize(LapTop) for LapTop in LapTop.query.all()]
#         }
#
#         document = create_docx(data)
#
#         # Save to a BytesIO stream
#         doc_io = io.BytesIO()
#         document.save(doc_io)
#         doc_io.seek(0)
#
#         return send_file(doc_io, as_attachment=True, download_name='Laptop.docx',
#                          mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
# @app.route('/admin/export_excel')
# def export_excel():
#     with app.app_context():
#         # Query and serialize your data
#         data = [serialize(dienthoai) for dienthoai in LapTop.query.all()]
#
#         # Create a pandas DataFrame
#         df = pd.DataFrame(data)
#
#         # Create an in-memory file object for the Excel file
#         excel_file = io.BytesIO()
#         with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
#             df.to_excel(writer, index=False, sheet_name='LapTop')
#
#         # Seek to the beginning of the stream
#         excel_file.seek(0)
#
#         # Send the in-memory file as a response
#         return send_file(excel_file, as_attachment=True, download_name='laptop.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')



@app.route('/products')
def products_list():
    LT = utils.load_tblLapTop()
    NSX = utils.load_tblNSX()
    return render_template("products.html",
                           LapTop=LT,
                           NSX=NSX,)





if __name__ == "__main__":
    from saleapp.admin import *
    app.run(debug=True)

