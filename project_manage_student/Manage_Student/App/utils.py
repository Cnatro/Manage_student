from datetime import datetime
from flask import Flask, send_file,url_for
import pandas as pd
import os
from App import vnpay,app
from App.dao import student_class,tuition_fee


def export_excel(data,year_learn):

    df = pd.DataFrame(data)

    # 2. Tạo thư mục lưu file
    upload_folder = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(upload_folder, exist_ok=True)

    # 3. Tạo tên file duy nhất
    file_name = f"DataStudentHistory-{year_learn}.xlsx"
    file_path = os.path.join(upload_folder, file_name)

    # 4. Ghi dữ liệu vào file
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    # 5. Trả file về client
    return send_file(
        file_path,
        as_attachment=True,
        download_name="export.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

def export_excel_average_score(data,year_learn,class_name,subject_name):

    df = pd.DataFrame(data)

    # 2. Tạo thư mục lưu file
    upload_folder = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(upload_folder, exist_ok=True)

    # 3. Tạo tên file duy nhất
    file_name = f"DataAverageSocore-{class_name}-{subject_name}-{year_learn}.xlsx"
    file_path = os.path.join(upload_folder, file_name)

    # 4. Ghi dữ liệu vào file
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    # 5. Trả file về client
    return send_file(
        file_path,
        as_attachment=True,
        download_name="export.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

def pay_with_vnpay(student_id):
    price_pay = tuition_fee.get_fee_by_grade(student_class.get_student_by_id(student_id).class_.grade)
    vnp = vnpay.VNPAY()
    vnp.request_data['vnp_Version'] = app.config['VNP_VERSION']
    vnp.request_data['vnp_Command'] = app.config['VNP_COMMAND']
    vnp.request_data['vnp_TmnCode'] = app.config['VNP_TMN_CODE']
    vnp.request_data['vnp_Amount'] = int(price_pay.fee) * 100
    vnp.request_data['vnp_CurrCode'] = app.config['VNP_CURRENCY_CODE']
    vnp.request_data['vnp_TxnRef'] = str(student_id) + '-' + datetime.now().strftime('%Y%m%d%H%M%S')
    vnp.request_data['vnp_Locale'] = 'vn'
    vnp.request_data[
        'vnp_OrderInfo'] = f'Thanh toán học phí cho học sinh ID {student_class.get_student_by_id(student_id).students.profile.name} Số tiền {price_pay.fee}'
    vnp.request_data['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')
    vnp.request_data['vnp_IpAddr'] = app.config['VNP_IP_ADDRESS']
    vnp.request_data['vnp_OrderType'] = 'billpayment'
    vnp.request_data['vnp_ReturnUrl'] = url_for('vnpay_return', _external=True)

    vnpay_payment_url = vnp.get_payment_url(vnpay_payment_url=app.config['VNP_URL'],
                                            secret_key=app.config['VNP_HASH_SECRET'])
    return vnpay_payment_url


def sent_mail(student_id,price):
    try:
        from flask_mail import Message
        from App import mail

        student = student_class.get_student_by_id(student_id).students
        message = Message('Phòng quản lí và đào tạo Trường THPT NNT', sender='NNT@gmail.com', recipients=[student.profile.email])
        message.body = f'Chào {student.profile.name} .Bạn đang thanh toán học phí thành công. Học phí : {price} !!!'
        mail.send(message)
        return "Gửi thành công"
    except Exception as e:
        return str(e)


if __name__=='__main__':
    with app.app_context():
        sent_mail(student_id=88,price=200000)

