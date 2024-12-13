from flask import request, redirect, url_for
from App.model import TeacherPlan
from App import db


def save_action(class_id):
    subject_ids = request.form.getlist('subject_id')
    # print(subject_ids)
    list_data_form = [
        {
            'teacher_subject_id': request.form.get(f'teacher_subject_id-{sb_id}'),
            'semester_id': request.form.get(f'semester-{sb_id}'),
            'class_id':class_id
        } for sb_id in subject_ids
    ]
    # print(list_data_form)
    add_teacher_plan(list_data_form)
    return redirect(url_for('assignment_teach'))


def delete_action():
    print('xóa dữ liệu')
    return ''


ACTION_ASSIGNMENT = {
    'save': save_action,
    'delete': delete_action
}


def handle_action(action_name):
    handle = ACTION_ASSIGNMENT.get(action_name)
    return handle


# ======================================================================

def add_teacher_plan(list_data):
    for t in list_data:
        t = TeacherPlan(teacher_subject_id=t['teacher_subject_id'], class_id=t['class_id'], semester_id=t['semester_id'])
        db.session.add(t)
    db.session.commit()
