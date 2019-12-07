from info.models import AccountPas,Student,Teacher,Group,Comm
from info.modules.Student.student import index_blu_student
from flask import request, jsonify
from datetime import datetime
from info import db
from info.untils.Jiekou import DOUBLE

#用户登录
@index_blu_student.route(DOUBLE+'/account/login',methods=['POST'])
def Users_login():
    """
    学生用户登录
    :param  status: 状态,  account:账号， password:密码
    :return: true&false
    """
    status = request.args.get('status')
    account = request.args.get('account')
    password = request.args.get('password')
    try:
        information = AccountPas.query.fillter(AccountPas.account == account).first()
    except Exception as e:
        return "查询失败!"
    isLogin = {
        'isLogin': True
    }
    isnotLogin = {
        'siLofin':False
    }
    if information.status == status:
        if information.password == password:
            return jsonify(isLogin)
        else:
            return jsonify(isnotLogin)
    else:
        return jsonify(isnotLogin)

#查询学生信息
@index_blu_student.route(DOUBLE+'/student/info',methods=['POST'])
def Student_information():
    """
    :param  sid:学生id
    :return: sid, name, groupId, zid, className, tid, account, teacherName, email, introduction,
    major,groupExtra[id, name, majorField, intro,], teacherList[tid, name, email, introduction,
    major, groupId, zid], [tid, name, email, introduction, major, groupId, zid]
    """

    sid = request.args.get('sid')
    try:
        student_information = Student.query.fillter(Student.sid == sid).first()
        teacher_information = Teacher.query.fillter(Teacher.tid == student_information.tid).first()
        group_information = Group.query.fillter(Group.id == student_information.group.id).first()
        account_information = AccountPas.query.fillter(AccountPas.zid == student_information.zid).first()
        group_teacher_information = Teacher.query.fillter(Teacher.group_id == student_information.group_id).all()
    except Exception as e:
        return "查询失败!"

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
    }
    return jsonify({
            "studentInfo":{
                studentlnfo,
                {
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
                            }for i in group_teacher_information
                        ]
                    }
                }

            }
        }

    )

#学生退组
@index_blu_student.route(DOUBLE+'/student/exit/group',methods=['POST'])
def Student_withdrawal():
    """
    :param  sid:学生id  gid:小组id
    :return: true&false
    """
    sid = request.args.get('sid')
    gid = request.args.get('gid')
    try:
        student_information = Student.query.fillter(Student.sid == sid).first()
    except Exception as e:
        return "查询失败!"
    isExit = {
        'isLogin': True
    }
    isnotExit = {
        'siLofin': False
    }
    if student_information.group_id == gid:
        return jsonify(isnotExit)
    else:
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
        one_group_information = Group.query.fillter(Group.id == gid).first()
        group_teacher = Teacher.query.fillter(group_id = gid).all()
    except Exception as e:
        return "查询失败！"
    groupInfo ={
    "id": one_group_information.id,
    "name": one_group_information.name,
    "majorField": one_group_information.major_field,
    "intro": one_group_information.intro,
    }
    return jsonify({
        "groupInfo":{
            groupInfo,
            {
                "teacherList": [
                {
                    "tid": i.tid,
                    "name": i.name,
                    "email": i.email,
                    "introduction": i.introduction,
                    "major": i.major,
                    "groupId": i.group_id,
                    "zid": i.zid
                }] for i in group_teacher
            }

        }
    }

    )

#查询所有小组信息
@index_blu_student.route(DOUBLE+'/group/query-all',methods=['GET'])
def Group_information():
    """
    :param
    :return:  groupData, id, name, majorField, intro, teacherList[]
    """
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
                        }for a in Teacher
                    ]

                }for i in Group
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
    return jsonify({
            'commList':[
                {
                "hid": i.hid,
                "zid": i.zid,
                "tid": i.tid,
                "time": i.time,
                "content":i.content,
                "title": i.title
                } for i in Comm
          ]
        })

#学生提交会议记录
@index_blu_student.route(DOUBLE+'/comm/save',methods=['POST'])
def Student_meetings():
    """
    :param   sid:学生id  title:会议标题  content:会议记录
    :return: true&false
    """
    sid = request.args.get('sid')
    title = request.args.get('title')
    content = request.args.get('content')
    try:
        student_meeting_minutes = Comm(sid=sid,title=title,content=content,time=datetime.now().strftime('%Y-%m-%d %H:%M:%S %f'))
        db.session.add(student_meeting_minutes)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "isSuccess":False
        })
    return jsonify({
            "isSuccess":True
    })

#查询一条会议数据
@index_blu_student.route(DOUBLE+'/comm/query-one',methods=['POST'])
def One_meeting_minutes():
    """
    :param  cid:会议记录id
    :return:  comm[hid, zid, tid, time, content, title]
    """
    cid = request.args.get('cid')
    try:
        meeting_minutes = Comm.query.fillter(Comm.cid == cid).first()
    except Exception as e:
        return jsonify("查询失败")
    return jsonify(
        {
            "comm":{
                "hid": meeting_minutes.hid,
                "zid": meeting_minutes.zid,
                "tid": meeting_minutes.tid,
                "time": meeting_minutes.time,
                "content": meeting_minutes.content,
                "title": meeting_minutes.title
            }
        }
    )