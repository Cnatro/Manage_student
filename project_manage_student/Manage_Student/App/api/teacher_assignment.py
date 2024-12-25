from flask import jsonify,request
from App import app
from App.dao import classes,semester
from App.model import Grade

@app.route('/api/teacher_assignment',methods=['POST'])
def get_class_by_grade():
    grade_value = int(request.json.get('grade'))

    if grade_value:
        class_ = classes.get_list_class(Grade(grade_value))
        list_class_json = [
            {
                'grade': c.grade.value,
                'class_name': c.name,
                'class_id' : c.id
            }
            for c in class_
        ]
        # print(list_class_json)
        return jsonify({'class_list': list_class_json})
    return jsonify({})

# @app.route('/api/teacher_score',methods=['POST'])
# def get_subject_by_class():
#     class_value = int(request.json.get('class_in_teacher_score'))
#
#     if class_value:
#         # lấy danh sách lớp
#         class_ = classes.get_list_class(class_value)
#
#         list_class_json = [
#             {
#                 'grade': c.grade.value,
#                 'class_name': c.name,
#                 'class_id' : c.id
#             }
#             for c in class_
#         ]
#         # print(list_class_json)
#         return jsonify({'class_list': list_class_json})
#     return jsonify({})


@app.route('/api/teacher_assignment/get_value_year',methods=['POST'])
def get_value_by_year():
    year_ = request.json.get('year')
    values = semester.get_semester_by_year(year_)
    values_json = [
        {
            'id':v.id,
            'name': v.name.name
        }for v in values
    ]
    return jsonify({'values':values_json})