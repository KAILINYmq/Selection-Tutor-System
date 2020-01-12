import logging

class Config(object):
    """工程配置信息"""
    DEBUG = True

    # 生成数据库模型
    # flask-sqlacodegen --outfile models.py --flask mysql+pymysql://root:123456@47.100.50.208:3307/doubleSelect
    # flask-sqlacodegen "mysql+pymysql://root:123456@47.100.50.208:3307/doubleSelect" --tables teacher, student, activity, comm, group, leader, account_pass --outfile "info/models.py"  --flask
    # 数据库的配置信息
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root_txy:123456Ymq.@129.28.155.16:3306/MentorSelect?charset=utf8"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 如果请求结束时候， 如果指定此配置为True，那么SQLAlchemy会自动执行一次commit

    # 设置日志等级
    LOG_LEVEL = logging.DEBUG

class Development(Config):
    """项目配置文件(开发环境下)"""
    DEBUG = True

class ProductionConfig(Config):
    """项目配置文件(生产环境下)"""
    DEBUG = False
    LOG_LEVEL = logging.WARNING

class TestingConfig(Config):
    """项目配置文件(单元测试环境下)"""
    DEBUG = True
    TESTING = True

config = {
    "development": Development,
    "production": ProductionConfig,
    "testing": TestingConfig
}