from flask import Blueprint

# 创建蓝图
index_blu_student_teacher = Blueprint("index_student_teacher", __name__)

from . import teacher_views