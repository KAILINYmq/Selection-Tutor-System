from . import index_blu
from flask import request


@index_blu.route('/teacher/MyTeacher/<int:tid>')
def index1(tid):
    print(tid)
    return 'index'