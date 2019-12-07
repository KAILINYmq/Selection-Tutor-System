from info import models
from . import index_blu
from flask import request, current_app
from flask.json import jsonify
from info.untils.response_code import RET
import re


# /teacher/ownInfo?tid=1
@index_blu.route('/teacher/ownInfo/')
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


@index_blu.route('/student/query/student-history', methods=["POST"])
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
        teacher = models.Teacher.query.get(tid_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据错误！")


    return "OK"


# TODO 未完成
@index_blu.route('/student/GroStudent', methods=["POST"])
def GroStudent():
    """
    展示小组的学生
    :param gid:
    :return: students sid name className
    """
    gid = request.args.get("gid")
    # if
    index_blu.Student.query.all()

    # group = index_blu.Group.query.filter_by(id=gid).first()
    # if not group:
    #     # return("没有对应的小组")
    #     return jsonfiy("error_code":1)
    # else:
    #     students = [student for student in index_blu.Student.query.all()]
    #     return jsonfiy({"error_code" : 0,"data":{students}})
    #
