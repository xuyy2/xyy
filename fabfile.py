from fabric.api import env, run
from fabric.operations import sudo

# 代码托管仓库地址
GIT_REPO = "https://github.com/xuyy2/xyy"

# 用于登录服务器的用户名、密码
env.user = 'root'
env.password = 'kDRzdZhlQl9I'

# 填写你自己的主机对应的域名
env.hosts = ['xyy.ink']

# 一般情况下为 22 端口，如果非 22 端口请查看你的主机服务提供商提供的信息
env.port = '27488'


def deploy():
    # 需要部署的项目的根目录
    source_folder = '/home/xyy/sites/xyy.ink/xyy'
    # 进入根目录
    # git pull拉取远程仓库的最新代码
    run('cd %s && git pull' % source_folder)
    run("""
        cd {} &&
        ../env/bin/pip install -r requirements.txt &&
        ../env/bin/python3 manage.py collectstatic --noinput &&
        ../env/bin/python3 manage.py migrate
        """.format(source_folder))
    sudo('restart gunicorn-demo.zmrenwu.com')
    sudo('service nginx reload')
