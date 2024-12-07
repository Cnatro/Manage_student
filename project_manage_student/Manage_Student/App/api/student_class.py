from flask import jsonify,request
from App import app
from App.dao import student_class

@app.route('/api/student_class',methods=['post'])
def get_students_by_class():
    class_id = request.json.get('class_id')
    # print(class_id)
    students_array = student_class.get_list_student_by_class_id(class_id)

    students_json = {}
    class_info = {}
    # chuyển array => json
    if students_array:
        for st in students_array:
            students_json[st.id] = {
                'id': st.id,
                'student_id': st.student_id,
                'class_id':st.class_id,
                'staff_id':st.students.staff_id,
                'student_name' :st.students.profile.name,
                'birthday':st.students.profile.birthday,
                'gender':st.students.profile.gender,
                'address':st.students.profile.address,
                'email':st.students.profile.email,
                'number_phone':st.students.profile.number_phone,
                'status_payment':st.students.status_payment,
                'class_name': students_array[0].class_.name,
            }
        class_info = {
            'quantity_student': students_array[0].class_.quantity_student,
            'grade': str(students_array[0].class_.grade),
            'teacher_id': students_array[0].class_.teacher_id
        }
    return jsonify({'students':students_json,'class_':class_info})