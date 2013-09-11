from fabric.api import *


# TODO set hosts
env.hosts = ['',]
env.use_ssh_config = True

# TODO set
server_project_dir = ''


@task
def pull():
    with cd(server_project_dir):
        run('git pull')


@task
def build_static():
    run('django-admin.py collectstatic --noinput')
    with cd(server_project_dir + '/livinglotsnola/collected_static/js/'):
        run('r.js -o app.build.js')


@task
def install_requirements():
    with cd(server_project_dir):
        run('pip install -r requirements/base.txt')
        run('pip install -r requirements/production.txt')


@task
def syncdb():
    run('django-admin.py syncdb')


@task
def migrate():
    run('django-admin.py migrate')


@task
def restart_django():
    run('supervisorctl -c ~/supervisor/supervisord.conf restart django')


@task
def restart_memcached():
    run('supervisorctl -c ~/supervisor/supervisord.conf restart memcached')


@task
def status():
    run('supervisorctl -c ~/supervisor/supervisord.conf status')


@task
def deploy():
    pull()
    install_requirements()
    syncdb()
    migrate()
    build_static()
    restart_django()
