from flask import jsonify,request
from App import app
from App.dao import classes
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