from info.models import Teacher
from . import index_blu
from flask import request


# 导师查询个人信息
# TODO 未完成
@index_blu.route('/teacher/ownInfo/<int:tid>')
def index1(tid):
    """
    查询老师信息
    :param tid: 老师ID
    :return: ID, name, number, major, email
    """
    try:
        teacher = Teacher.query.get(tid)
    except Exception as e:
        return "查询错误!"

    print(tid)
    print(teacher.name)

    return 'index'