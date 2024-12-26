import pdb

from App import app,db
from flask import request,jsonify
from App.dao import teacher_subject,semester
from App.model import  Grade

@app.route('/api/admin/get_info',methods=['POST'])
def get_info_by_grade():
    grade_name = request.json.get('grade_value')
    subjects = teacher_subject.get_subjects_by_grade(Grade(int(grade_name)))
    semester_ = semester.get_semester()
    subjects_json = [
        {
            'subject_id':s.id,
            'subject_name':s.name,
        }for s in subjects
    ]
    semester_json = [
        {
            'semester_id':s.id,
            'semester_name':s.name.name,
            'semester_year':s.year,
        }for s in semester_
    ]

    return jsonify({'subjects': subjects_json,'semesters':semester_json})