from flask import Blueprint

# 创建蓝图
index_blu_student = Blueprint("index_student", __name__)

from . import User_login