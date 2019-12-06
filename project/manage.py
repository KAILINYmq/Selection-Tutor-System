from flask_script import Manager
from info import create_app

app = create_app('development')

# 添加扩展命令行
manager = Manager(app)

if __name__ == '__main__':
    manager.run()