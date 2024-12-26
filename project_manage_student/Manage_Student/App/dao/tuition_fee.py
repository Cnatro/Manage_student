from App.model import TuitionFee, VnPayHistory, Receipt
from App import db
from App.dao import student_class


def get_fee_by_grade(grade):
    return TuitionFee.query.filter(TuitionFee.grade.__eq__(grade)).first()


def add_vnPay_history(transaction_id, price_pay, create_day, description):
    vnpay = VnPayHistory(transaction_id=transaction_id, price_pay=price_pay, create_day=create_day,
                         description=description)
    db.session.add(vnpay)
    db.session.commit()
    return vnpay


def add_receipt(student_id, staff_id, create_day, transaction_id):
    st = student_class.get_student_by_id(student_id)
    st.students.status_payment = 1
    db.session.add(st)

    rpt = Receipt(student_id=student_id, staff_id=staff_id, transaction_id=transaction_id, create_day=create_day)
    db.session.add(rpt)

    db.session.commit()
