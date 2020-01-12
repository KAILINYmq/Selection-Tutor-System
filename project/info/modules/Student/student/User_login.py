from info.models import AccountPas,Student,Teacher,Group,Comm
from info.modules.Student.student import index_blu_student
from flask import request, jsonify
from info import db
from info.untils.response_code import RET
from info.untils.Jiekou import DOUBLE

#用户登录
@index_blu_student.route(DOUBLE+'/account/login',methods=['POST'])
def Users_login():
    """
    学生用户登录
    :param  status: 状态,  account:账号， password:密码
    :return: true&false
    """
    status = request.form.get('status')
    account = request.form.get('account')
    password = request.form.get('password')
    try:
        information = AccountPas.query.filter(AccountPas.account == account).first()
        if information == None:
            return jsonify(errno=RET.USERERR,errmsg="用户不存在或未激活")
    except Exception as e:
        return ('访问失败404')
    isLogin = {
        'isLogin': True
    }
    if information.status == int(status):
        if password is None or information.password != password:
            return jsonify(errno=RET.PWDERR, errmsg="密码错误!")
        else:
            return jsonify(isLogin)
    else:
        return jsonify(errno=RET.ROLEERR,errmsg="用户身份错误!")

#查询学生信息
@index_blu_student.route(DOUBLE+'/student/info',methods=['POST'])
def Student_information():
    """
    :param  sid:学生id
    :return: sid, name, groupId, zid, className, tid, account, teacherName, email, introduction,
    major,groupExtra[id, name, majorField, intro,], teacherList[tid, name, email, introduction,
    major, groupId, zid], [tid, name, email, introduction, major, groupId, zid]
    """
    sid = request.form.get('sid')

    try:
        student_information = Student.query.filter(Student.sid == sid).first()
        teacher_information = Teacher.query.filter(Teacher.tid == student_information.tid).first()
        group_information = Group.query.filter(Group.id == student_information.group_id).first()
        account_information = AccountPas.query.filter(AccountPas.zid == student_information.zid).first()
        group_teacher_information = Teacher.query.filter(Teacher.group_id == student_information.group_id).all()
    except Exception as e:
        return jsonify(errno=RET.USERERR,errmsg="用户不存在或未激活")

    studentlnfo ={
        "sid": student_information.sid,
        "name": student_information.name,
        "groupId": student_information.group_id,
        "zid": student_information.zid,
        "className": student_information.class_name,
        "tid": student_information.tid,
        "account": account_information.account,
        "teacherName": teacher_information.name,
        "email": teacher_information.email,
        "introduction": teacher_information.introduction,
        "major": teacher_information.major,
        "groupExtra": {
            "id": group_information.id,
            "name": group_information.name,
            "majorField": group_information.major_field,
            "intro": group_information.intro,
            "teacherList": [
                {
                    "tid": i.tid,
                    "name": i.name,
                    "email": i.email,
                    "introduction": i.introduction,
                    "major": i.major,
                    "groupId": i.group_id,
                    "zid": i.zid
                } for i in group_teacher_information
            ]
        }
    }
    return jsonify({
            "studentInfo":
                studentlnfo,

    } )

#学生退组
@index_blu_student.route(DOUBLE+'/student/exit/group',methods=['POST'])
def Student_withdrawal():
    """
    :param  sid:学生id  gid:小组id
    :return: true&false
    """
    sid = request.form.get('sid')
    gid = request.form.get('gid')
    isExit = {
        'isLogin': True
    }
    isnotExit = {
        'siLofin': False
    }
    try:
        student_information = Student.query.filter(Student.sid == sid).first()
        again_student_information = Student.query.filter(Student.group_id == gid).first()
        if student_information == again_student_information:
            student_information.group_id = 0
            db.session.commit()
        else:
            return ("选择小组错误")
    except Exception as e:
        db.session.rollback()
        return jsonify(isnotExit)
    return jsonify(isExit)

#查询单个小组信息
@index_blu_student.route(DOUBLE+'/group/query-one',methods=['GET'])
def One_group_information():
    """
    :param   gid:小组id
    :return: id, name, majorField, intro, teacherList[tid, name, email, introduction, major, groupId, zid]
    """
    gid = request.args.get('gid')
    try:
        one_group_information = Group.query.filter(Group.id == gid).first()
        group_teacher = Teacher.query.filter(Teacher.group_id == gid).all()
    except Exception as e:
        return jsonify(errno=RET.NODATA,errmsg="无数据!")
    groupInfo ={
    "id": one_group_information.id,
    "name": one_group_information.name,
    "majorField": one_group_information.major_field,
    "intro": one_group_information.intro,
    "teacherList": [
        {
            "tid": i.tid,
            "name": i.name,
            "email": i.email,
            "introduction": i.introduction,
            "major": i.major,
            "groupId": i.group_id,
            "zid": i.zid
        }for i in group_teacher]

    }

    return jsonify({
        "groupInfo":
            groupInfo,

    }

    )

#查询所有小组信息
@index_blu_student.route(DOUBLE+'/group/query-all',methods=['GET'])
def Group_information():
    """
    :param
    :return:  groupData, id, name, majorField, intro, teacherList[]
    """
    group_teacher_information = []
    try:
        group_information = Group.query.filter(Group.id != 0).all()
        for i in group_information:
            if Teacher.query.filter(i.id == Teacher.group_id).all() != list():
                group_teacher_information.append(Teacher.query.filter(i.id == Teacher.group_id).all())
    except Exception as e:
        return jsonify(errno=RET.DBERR,errmsg="数据库查询错误!")
    return jsonify({
            "groupData":[
                {
                    "id": i.id,
                    "name":i.name,
                    "majorField": i.major_field,
                    "intro": i.intro,
                    "teacherList": [
                        {
                            "tid": a.tid,
                            "name": a.name,
                            "email": a.email,
                            "introduction": a.introduction,
                            "major": a.major,
                            "groupId": a.group_id,
                            "zid": a.zid
                        }for b in group_teacher_information for a in b if a.group_id == i.id
                    ]

                }for i in group_information
            ]
        }
    )

#查询所有会议记录
@index_blu_student.route(DOUBLE+'/comm/list',methods=['POST'])
def Meeting_minutes():
    """
    :param
    :return:  commList[hid, zid, tid, time, content, title]
    """
    try:
        comm_information = Comm.query.filter(Comm.hid).all()
    except Exception as e:
        return jsonify(errno=RET.DBERR,errmsg="数据库查询错误!")
    return jsonify({
            'commList':[
                {
                "hid": i.hid,
                "sid": i.sid,
                "tid": i.tid,
                "time": i.time,
                "content":i.content,
                "title": i.title
                } for i in comm_information
          ]
        })

#查询一条会议数据
@index_blu_student.route(DOUBLE+'/comm/query-one',methods=['POST'])
def One_meeting_minutes():
    """
    :param  hid:会议记录id
    :return:  comm[hid, zid, tid, time, content, title]
    """
    hid = request.form.get('hid')
    try:
        meeting_minutes = Comm.query.filter(Comm.hid == hid).first()
        if meeting_minutes == None:
            return ("没有此条数据")
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg="数据库查询错误!")
    return jsonify(
        {
            "comm": {
                "hid": meeting_minutes.hid,
                "sid": meeting_minutes.sid,
                "tid": meeting_minutes.tid,
                "time": meeting_minutes.time,
                "content": meeting_minutes.content,
                "title": meeting_minutes.title
            }
        }
    )