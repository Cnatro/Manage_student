import pdb
from datetime import datetime

from flask_login import current_user

from App import app, db
from App.dao import teacher_list,exam
from flask import jsonify, request
from App.model import Exam, Score


@app.route('/api/teacher_score/get_info_by_class', methods=['POST'])
def get_info_by_class():
    class_id = request.json.get('class_id')
    teach_class = teacher_list.get_plan_by_class_id(class_id=class_id, teacher_id=current_user.id)

    teach_class_json = {}
    subjects = []
    for t in teach_class:
        if t.teacher_subjects.subjects.id not in teach_class_json:
            teach_class_json[t.teacher_subjects.subjects.id] = []
            subjects.append({
                'subject_id': t.teacher_subjects.subjects.id,
                'subject_name': t.teacher_subjects.subjects.name,
            })

        teach_class_json[t.teacher_subjects.subjects.id].append({
            'subject_id': t.teacher_subjects.subjects.id,
            'semester_id': t.semester_id,
            'semester_name': t.semester.name.name
        })
    return jsonify({'values': teach_class_json, 'year': datetime.now().year,'subjects':subjects})


@app.route('/api/teacher_score/<int:teacher_plan_id>/score', methods=['GET','POST'])
def add_score(teacher_plan_id):
    list_score = request.json.get('list_score')

    for s in list_score:
        if s.get('student_id') and teacher_plan_id:
            tmp_exam = exam.get_exam_by_student_id(teacher_plan_id=teacher_plan_id,student_id=int(s['student_id']))
            if tmp_exam is None:
                tmp_exam = Exam(teacher_plan_id=teacher_plan_id, student_id=int(s['student_id']))
                db.session.add(tmp_exam)
                db.session.commit()
            if s.get('type_exam') and s.get('value'):
                is_score_exit = (Score.query.filter(Score.type_exam.__eq__(s.get('type_exam')),
                                                    Score.exam_id.__eq__(tmp_exam.id),
                                           Score.count_exam.__eq__(s.get('count_exam'))).first())
                if is_score_exit is None:
                    new_score = Score(type_exam=s.get('type_exam'),
                                      value=float(s.get('value')),
                                      count_exam=s.get('count_exam'),
                                      exam_id=tmp_exam.id)
                    db.session.add(new_score)
    db.session.commit()
    return jsonify({'status': 200})


@app.route('/api/teacher_score/<int:teacher_plan_id>/edit_score', methods=['PUT'])
def edit_score(teacher_plan_id):
    list_score = request.json.get('list_score')
    for s in list_score:
        if s.get('student_id') and teacher_plan_id:
            tmp_exam = exam.get_exam_by_student_id(teacher_plan_id=teacher_plan_id,student_id=int(s['student_id']))
            if s.get('type_exam') and s.get('value'):
                score = (Score.query.filter(Score.exam_id.__eq__(tmp_exam.id),
                                           Score.type_exam.__eq__(s.get('type_exam')),
                                           Score.count_exam.__eq__(s.get('count_exam')))
                         .first())
                score.value = float(s.get('value'))
    db.session.commit()
    return jsonify({'status': 200})