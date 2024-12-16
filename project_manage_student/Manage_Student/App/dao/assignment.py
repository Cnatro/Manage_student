from operator import truediv

from flask import request, redirect, url_for
from sqlalchemy import false

from App.model import TeacherPlan
from App import db


def save_action(class_id):
    subject_ids = request.form.getlist('subject_id')
    list_data_form = []
    for sb_id in subject_ids:
        if request.form.get(f'semester-both-{sb_id}') == 'both':
            list_data_form += [
                {
                    'teacher_subject_id': int(request.form.get(f'teacher_subject_id-{sb_id}')),
                    'semester_id': [int(s) for s in request.form.getlist(f'semester-{sb_id}')],
                    'class_id': int(class_id)
                }
            ]
        else:
            list_data_form += [
                {
                    'teacher_subject_id': int(request.form.get(f'teacher_subject_id-{sb_id}')),
                    'semester_id': int(request.form.get(f'semester-{sb_id}')),
                    'class_id': int(class_id)
                }
            ]
    # print(list_data_form)
    add_teacher_plan(list_data_form)


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
    for dt in list_data:
        if isinstance(dt['semester_id'], int):
            create_plan(
                teacher_subject_id=dt['teacher_subject_id'],
                class_id=dt['class_id'],
                semester_id=dt['semester_id']
            )
            # nhưng kế hoạch đã tồn tại trc đó nhưng ở khác kì vì này chỉ được 1 kì duy nhất thôi
            query_another = TeacherPlan.query.filter(TeacherPlan.teacher_subject_id.__eq__(dt['teacher_subject_id']),
                                                     TeacherPlan.class_id.__eq__(dt['class_id']),
                                                     TeacherPlan.semester_id != dt['semester_id']).first()
            if query_another:
                db.session.delete(query_another)
                db.session.commit()
        else:
            for s in dt['semester_id']:
                create_plan(
                    teacher_subject_id=dt['teacher_subject_id'],
                    class_id=dt['class_id'],
                    semester_id=s
                )


def create_plan(teacher_subject_id, class_id, semester_id):
    plan = TeacherPlan.query.filter(TeacherPlan.teacher_subject_id.__eq__(teacher_subject_id),
                                    TeacherPlan.class_id.__eq__(class_id),
                                    TeacherPlan.semester_id.__eq__(semester_id)).first()

    if plan:
        return True
    else:
        plan = TeacherPlan(
            teacher_subject_id=teacher_subject_id,
            class_id=class_id,
            semester_id=semester_id
        )
        db.session.add(plan)
        db.session.commit()
        return False
