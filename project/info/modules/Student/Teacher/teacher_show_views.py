from info.models import Teacher, Student
from info.modules.Student.Teacher import index_blu_student_teacher
from flask import request, jsonify


# 我的导师
@index_blu_student_teacher.route('/teacher/MyTeacher', methods=['POST'])
def MyTeacher():
    """
    导师查询个人信息
    :param tid: 老师ID
    :return: tid, name, email, introduction, major, groupId, zid, [sid, name, groupId, zid, classname, tid]
    """
    tid = request.args.get('tid')
    print(tid)
    try:
        teacher = Teacher.query.get(tid)
        student = Student.query.get(tid)
    except Exception as e:
        return "查询错误!"
    json_dict = {
        "name": teacher.name,
        "email": teacher.email,
        "introduction": teacher.introduction,
        "major": teacher.major,
        "groupId": teacher.group_id,
        "zid": teacher.zid,
    }
    print(student)
    for i in student:
        pass
    return jsonify(json_dict)