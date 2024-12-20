from flask_login import current_user

from App import app
from App.dao import teacher_list
from flask import jsonify,request

@app.route('/api/teacher_score/get_info_by_class',methods=['POST'])
def get_info_by_class():
    class_id = request.json.get('class_id')
    teach_class = teacher_list.get_plan_by_class_id(class_id=class_id,teacher_id=current_user.id)
    print(teach_class)
    return jsonify({'info':500})