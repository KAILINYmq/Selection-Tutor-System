from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
from logging.handlers import RotatingFileHandler

from config import config

# 配置数据库
db = SQLAlchemy()

def setup_log(config_name):
    # 创建日志的记录等级
    logging.basicConfig(level=config[config_name].LOG_LEVEL)  # 调试debug等级
    # 创建日志记录器， 指明日志保存路径，每个日志文件的最大最小，保护日志文件个数上线
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 *100, backupCount=10)
    # 创建日志记录的格式，日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象 (flask app使用) 添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


def create_app(config_name):
    # 配置日志,并且传入配置名字， 以便能获取到指定配置对应的日志等级
    setup_log(config_name)
    # 创建Flask对象
    app = Flask(__name__)
    # 加载配置
    app.config.from_object(config[config_name])
    # 通过app初始化db
    db.init_app(app)


    # 注册蓝图
    from info.modules.teacher import index_blu
    app.register_blueprint(index_blu)

    return app