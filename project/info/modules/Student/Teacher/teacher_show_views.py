from info.models import Teacher, Student
from info.modules.Student.Teacher import index_blu_student_teacher
from flask import request, jsonify
from info.untils.response_code import RET

# 我的导师
@index_blu_student_teacher.route('/teacher/MyTeacher', methods=['POST'])
def MyTeacher():
    """
    我的导师
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

# 退出导师申请
@index_blu_student_teacher.route('/activity/applying/outteacher', methods=['POST'])
def ExitTeacher():
    """
    退出导师申请
    :param sid: 学生ID
    :return: 1 or 2
    """
    pass
    # sid = request.args.get('sid')
    # try:
    #     student = Student.query.get(sid)
    # except Exception as e:
    #     return "查询错误!"


# 提交导师调换申请
@index_blu_student_teacher.route('/teacher/submitChange', methods=['POST'])
def Myteacherteam():
    """
    提交导师调换申请
    :param currentTid: 当前老师id, tragetTid:目标老师id, sid:学生id, Date:日期
    :return: error_code, data[teacher[name, major], student[sName, class, number]]
    """
    tid = request.args.get('tid')
    try:
        teacher = Teacher.query.get(tid)
        student = Student.query.filter(Student.tid == tid).all()
    except Exception as e:
        return '查询错误!'
    json_dict = {
        'error_code': 0,
        'data': {
            'teacher': {
                'name': teacher.name,
                'major': teacher.major
            }
        }
    }
    return jsonify(json_dict)

# 导师信息
@index_blu_student_teacher.route('/teacher/queryInfo', methods=['POST'])
def TeacherMessage():
    """
    导师信息
    :param tid:老师id, sid:学生id
    :return: tid, name, major, email, memebers, ApplicationStatus
    """
    tid = request.args.get('tid')
    sid = request.args.get('sid')
    try:
        teacher = Teacher.query.get(tid)
        student = Student.query.filter(Student.tid == tid).all()
    except Exception as e:
        return "查询错误!"
    json_dict = {
        'error_code': RET.OK,
        'data': {
            'tid': teacher.tid,
            'name': teacher.name,
            'major': teacher.major,
            'email': teacher.email,
            # 'members': student.count(),
            'ApplicationStatus': 1
        }
    }
    return jsonify(json_dict)
