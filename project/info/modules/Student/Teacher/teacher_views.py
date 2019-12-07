from info.models import Activity, Student, Teacher
from info import db
from info.modules.Student.Teacher import index_blu_student_teacher
from flask import request, jsonify
from info.untils.Jiekou import DOUBLE
from datetime import datetime

# 退出导师申请
@index_blu_student_teacher.route(DOUBLE+'/activity/applying/outteacher', methods=['POST'])
def ExitTeacher():
    """
    退出导师申请
    :param sid: 学生ID
    :return: 1 or 2
    """
    sid = request.args.get('sid')
    try:
        activity = Activity.query.filter_by(sid=sid).all()
        for i in activity:
            if i.status == 24:
                return jsonify(2)
        activity_add = Activity(sid=sid, status=24, a_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), is_delete=1)
        db.session.add(activity_add)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify('操作失败404')
    return jsonify(1)

# 我的导师团队
@index_blu_student_teacher.route(DOUBLE+'/teacher/MyTeacher', methods=['POST'])
def MyTeacherteam():
    """
    我的导师团队
    :param tid: 老师ID
    :return: tid, name, email, introduction, major, groupId, zid, [sid, name, groupId, zid, classname, tid]
    """
    tid = request.args.get('tid')
    try:
        teacher = Teacher.query.get(tid)
        student = Student.query.filter(Student.tid == tid).all()
    except Exception as e:
        return "查询错误!"
    json_dict = {
        'name': teacher.name,
        'email': teacher.email,
        'introduction': teacher.introduction,
        'major': teacher.major,
        'groupId': teacher.group_id,
        'zid': teacher.zid,
    }
    return jsonify([
                        json_dict,
                        [
                            {
                                'sid': i.sid,
                                'name': i.name,
                                'zid': i.zid,
                                'classname': i.class_name,
                                'tid': i.tid,
                            } for i in student
                        ]
                    ])

# 提交导师申请
@index_blu_student_teacher.route(DOUBLE+'/teacher/submitApplications', methods=['POST'])
def ApplyTeacher():
    """
    提交导师申请
    :param currentTid: tid:老师id, sid:学生id, Date:日期
    :return: data[status]
    """
    tid = request.args.get('tid')
    sid = request.args.get('sid')
    Date = request.args.get('Date')
    json_dict = {
        'data': {
            'status': 21
        }
    }
    try:
        activity = Activity.query.filter_by(sid=sid).all()
        for i in activity:
            if i.status == 21:
                return jsonify(json_dict)
        activity_add = Activity(sid=sid, tid=tid, status=21, a_time=Date, is_delete=1)
        db.session.add(activity_add)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify('操作失败404')
    return jsonify(json_dict)

# 导师信息
@index_blu_student_teacher.route(DOUBLE+'/teacher/queryInfo', methods=['POST', 'GET'])
def TeacherMessage():
    """
    导师信息
    :param tid:老师id, sid:学生id
    :return: tid, name, major, email, memebers, ApplicationStatus
    """
    tid = request.args.get('tid')
    sid = request.args.get('sid')
    ApplicationStatus = 3
    try:
        teacher = Teacher.query.get(tid)
        student = Student.query.filter(Student.tid == tid).count()
        activity = Activity.query.filter(Activity.tid == tid, Activity.sid == sid).all()
        if student < 10:
            ApplicationStatus = 1
        for i in activity:
            if i.status == 21:
                ApplicationStatus = 2
    except Exception as e:
        print(e)
        return "查询错误!"
    json_dict = {
        'data': {
            'tid': teacher.tid,
            'name': teacher.name,
            'major': teacher.major,
            'email': teacher.email,
            'members': student,
            'ApplicationStatus': ApplicationStatus
        }
    }
    return jsonify(json_dict)

# 选择导师
@index_blu_student_teacher.route(DOUBLE+'/teacher/queryAll', methods=['POST'])
def ChoiceTeacher():
    """
    导师信息
    :param sid:学生id
    :return: teacher, tid, tname, status
    """
    sid = request.args.get('sid')
    teacher = Teacher.query.all()

    def status_select(i):
        ApplicationStatus = 3
        if Student.query.filter(Student.tid == i.tid).count() < 10:
            ApplicationStatus = 1
        for i in Activity.query.filter(Activity.tid == i.tid, Activity.sid == sid).all():
            if i.status == 21:
                ApplicationStatus = 2
        return ApplicationStatus

    return jsonify({
        'teacher': [
            {
                'tid': i.tid,
                'tname': i.name,
                'status': status_select(i)
            } for i in teacher
        ]
    })