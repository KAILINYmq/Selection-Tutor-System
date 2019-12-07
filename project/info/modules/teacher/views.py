from info import models
from . import index_blu
from flask import request, current_app
from flask.json import jsonify
from info.untils.response_code import RET
import time, datetime
import re

from info import db
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
        student_account = models.AccountPas.query.filter_by(zid=student.zid).first()
        student_teacher = models.Teacher.query.filter_by(tid=student.tid).first()

        # historyTeacher
        student_historyTeacher = models.Activity.query.filter_by(sid=sid, status=22).order_by(models.Activity.tid.desc()).all()
        student_endTeacher = models.Activity.query.filter_by(sid=sid, status=25).order_by(models.Activity.tid.desc()).all()
        teacherHistoryName = models.Teacher.query.filter(models.Teacher.tid.in_([student_historyTeacher[0].tid, student_historyTeacher[1].tid])).order_by(models.Teacher.tid.desc()).all()

        # historyGroup
        student_groupStartTime = models.Activity.query.filter_by(sid=sid, status=2).order_by(models.Activity.tid.desc()).all()
        student_groupEndTime = models.Activity.query.filter_by(sid=sid, status=5).order_by(models.Activity.tid.desc()).all()
        groupHistoryName = models.Group.query.filter(models.Group.id.in_([student_groupStartTime[0].group_id, student_groupStartTime[1].group_id])).order_by(models.Group.id.desc()).all()

        # groupExtra
        groupExtra_id = models.Group.query.filter_by(id=student.group_id).first()
        groupExtra_teacher = models.Teacher.query.filter_by(group_id=groupExtra_id.id).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据错误！")

    teacherList = []
    for groupExtra_teacher_data in groupExtra_teacher:
        teacherList.append({
            "tid": groupExtra_teacher_data.tid,
            "name": groupExtra_teacher_data.name,
            "email": groupExtra_teacher_data.email,
            "introduction": groupExtra_teacher_data.introduction,
            "major": groupExtra_teacher_data.major,
            "groupId": groupExtra_teacher_data.group_id,
            "zid": groupExtra_teacher_data.zid
        })

    historyGroup = []
    tea0 = 0
    for groupStartTime_data in student_groupStartTime:
        historyGroup.append({
            "groupHistoryName": groupHistoryName[tea0].name,
            "interimTime": "null",
            "groupStartTime": groupStartTime_data.a_time,
            "groupEndTime": student_groupEndTime[tea0].a_time,
            "agid": groupHistoryName[tea0].id
        })
        tea0 += 1

    historyTeacher = []
    tea1 = 0
    for historyTeacher_data in student_historyTeacher:
        historyTeacher.append({
            "teacherHistoryName": teacherHistoryName[tea1].name,
            "interimTime": "null",
            "teacherStartTime": historyTeacher_data.a_time,
            "teacherEndTime": student_endTeacher[tea1].a_time,
            "atid": historyTeacher_data.tid
        })
        tea1 += 1

    # 4. 合并数据
    studentWithHosity = {
        "historyTeacher": historyTeacher,
        "historyGroup": historyGroup,
        "studentInfo": {
            "sid": student.sid,
            "name": student.name,
            "groupId": student.group_id,
            "zid": student.zid,
            "className": student.class_name,
            "tid": student.tid,
            "account": student_account.account,
            "teacherName": student_teacher.name,
            "email": student_teacher.email,
            "introduction": student_teacher.introduction,
            "major": student_teacher.major,
            "groupExtra": {
                "id": groupExtra_id.id,
                "name": groupExtra_id.name,
                "majorField": groupExtra_id.major_field,
                "intro": groupExtra_id.intro,
                "teacherList": teacherList
            }
        }
    }

    return jsonify(studentWithHosity=studentWithHosity)


#/activity/query/undomsg?tid=2&type=1
@index_blu.route(DOUBLE+'/activity/query/undomsg')
def index3():
    """
    消息处理展示接口
    :return:
    """
    # 获取tid值
    tid_data = request.args.get("tid")
    type_data = request.args.get("type")

    # 1.验证数据
    if not re.match('[1-9]\d*', tid_data):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误！")
    if not re.match('[1-9]\d*', type_data):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误！")

    # 2.查询数据
    try:
        student_account = models.Activity.query.filter_by(tid=tid_data, is_delete=type_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据错误！")

    news_dict_li = []
    for news_item in student_account:
        news_dict_li.append({
            "applyId": news_item.sid,
            # TODO 需改
            "applyPerson": models.Student.query.filter_by(sid=news_item.sid).first().name,
            "disposeId": 2,
            "disposePerson": "王老师",
            "type": news_item.status,
            "data": news_item.a_time
            })

    return jsonify(news_dict_li)

@index_blu.route(DOUBLE+'/activity/applying/group', methods=["POST"])
def index4():
    """
    兴趣小组处理学生申请的接口
    :return:
    """
    # 1. 获取参数
    sid = request.form.get("sid")
    gid = request.form.get("gid")
    status = request.form.get("status")

    # 2. 校验参数
    if not re.match('[1-9]\d*', sid):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误！")
    if not re.match('[1-9]\d*', gid):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误！")
    if not re.match('[1-9]\d*', status):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误！")

    # 3. 插入数据
    comm = models.Activity()
    comm.sid = sid
    comm.group_id = gid
    comm.a_time = int(time.mktime(datetime.datetime.now().timetuple()))
    comm.status = status
    try:
        db.session.add(comm)
        db.session.commit()
        isApply = True
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        isApply = False

    data = {
        "isApply": isApply
    }

    # 4.返回数据
    return jsonify(data)


@index_blu.route(DOUBLE+'/comm/save', methods=["POST"])
def index5():
    """
    学生提交提交会议记录接口
    :return:
    """
    # 1.获取参数
    tid = request.form.get("tid")
    title = request.form.get("title")
    content = request.form.get("content")

    # 2.校验参数
    if not re.match('[1-9]\d*', tid):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误！")
    if title is "":
        return jsonify(errno=RET.PARAMERR, errmsg="参数不能为空！")
    elif content is "":
        return jsonify(errno=RET.PARAMERR, errmsg="参数不能为空！")

    # 3.操作数据
    comm = models.Comm()
    comm.tid = tid
    comm.title = title
    comm.time = int(time.mktime(datetime.datetime.now().timetuple()))
    comm.content = content

    try:
        db.session.add(comm)
        db.session.commit()
        isSuccess = True
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        isSuccess = False

    data = {
        "isSuccess": isSuccess
    }
    # 4.返回数据
    return jsonify(data)








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
