from . import index_blu
from flask import request

@index_blu.route('/index')
def index():
    return 'index'


@index_blu.route('/teacher/ownInfo/<int:tid>')
def index1(tid):
    print(tid)
    return 'index'