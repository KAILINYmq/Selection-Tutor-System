from info import models
from . import index_blu
from flask import request, current_app
from flask.json import jsonify
from info.untils.response_code import RET
import re

from info.untils.Jiekou import DOUBLE

# /teacher/ownInfo?tid=1
@index_blu.route(DOUBLE+'/teacher/ownInfo/')
def index1():
    """
    导师查询个人信息
    :param tid: 老师ID
    :return: ID, name, number, major, email
    """
    # 获取tid值
    tid_data = request.args.get("tid")

    if not re.match('[1-9]\d*', tid_data):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误！")

    try:
        teacher = models.Teacher.query.get(tid_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据错误！")

    if not teacher:
        return jsonify(errno=RET.NODATA, errmsg="查询导师不存在！")

    data = {
        "id": teacher.tid,
        "name": teacher.name,
        # "number": teacher.number,
        "major": teacher.major,
        "email": teacher.email
    }

    return jsonify(data)


@index_blu.route(DOUBLE+'/student/query/student-history', methods=["POST"])
def index2():
    """
    查询申请的学生信息、历史导师信息、历史兴趣小组信息
    :return: studentWithHosity 申请的学生信息、历史导师信息、历史兴趣小组信息
    """
    # 1.获取参数
    sid = request.form.get("sid")

    # 2.校验参数
    if not re.match('[1-9]\d*', sid):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误！")

    # 3.查询数据
    try:
        student = models.Student.query.get(sid)
        student_account = models.AccountPas.query.filter(zid=student.zid)
        student_teacher = models.Teacher.query.filter(tid=student.tid)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据错误！")

    # 4. 合并数据
    studentWithHosity = {
        "studentWithHosity": [

        ],
        "historyGroup": [

        ],
        "studentInfo": {
            "sid": student.sid,
            "name": student.name,
            "groupId": student.group_id,
            "zid": student.zid,
            "className": student.class_name,
            "tid": student.tid,
            # "account": student_account.account,
            "teacherName": student_teacher.name,
            "email": student_teacher.email,
            "introduction": student_teacher.introduction,
            "major": student_teacher.major,
        }
    }

    return jsonify(studentWithHosity)


@index_blu.route(DOUBLE+'/student/GroStudent', methods=["POST"])
def GroStudent():
    """
    展示小组的学生
    :return: students, sid, name, className
    """
    # 1. 获取参数
    gid_data = request.args.get("gid")
    # 2. 检验参数是否合法
    if not re.match('[1-9]\d*', gid_data):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误！")
    # 3. 查询对应的小组
    try:
        group = models.Group.query.get(gid_data).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据错误！")
    # 4. 提取数据
    if not group:
        return jsonify(errno=RET.NODATA, errmsg="查询学习小组不存在！")

    try:
        students = [student for student in index_blu.Student.query.all()]
        student_data = []
        for student in students:
            data = {
                "sid": student.sid,
                "name": student.name,
                "className": student.class_name
            }
            student_data.append(data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据错误！")

    msg = {"error_code": 0, "data": {"students": student_data}}

    return jsonify(msg)


@index_blu.route(DOUBLE+'/student/TeaStudent', methods=["POST"])
def TeaStudent():
    """
    展示导师的学生
    :return:students, sid, name, className
    """
    # 1. 获取相应数据
    tid_data = request.args.get("tid")

    # 2. 检验参数是否合法
    if not re.match('[1-9]\d*', tid_data):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误！")

    try:
        teacher = models.Teacher.query.get(tid_data).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据错误！")

    if not teacher:
        return jsonify(errno=RET.NODATA, errmsg="查询的老师不存在！")

    # 查询对应学生
    try:
        students = models.Student.query.filter_by(tid="tid_data").all()
        data_list = list()
        for student in students:
            student_data = {
                "sid": student.sid,
                "name": student.name,
                "groupId": student.group_id,
                "zid": student.zid,
                "className": student.class_name,
                "tid": student.tid
            }
            data_list.append(student_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据错误！")

    return jsonify(data_list)






