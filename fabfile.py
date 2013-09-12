import contextlib

from fabric.api import *


env.hosts = ['ftn',]
env.use_ssh_config = True

server_project_dirs = {
    'dev': '~/webapps/dev_llnola_django/livinglots-nola',
    'prod': '~/webapps/llnola_django/livinglots-nola',
}

server_virtualenvs = {
    'dev': 'devllnola',
    'prod': 'llnola',
}


@contextlib.contextmanager
def cdversion(version):
    """cd to the version of livinglots-nola indicated"""
    with prefix('cd %s' % server_project_dirs[version]):
        yield


@contextlib.contextmanager
def workon(version):
    """workon the version of livinglots-nola indicated"""
    with prefix('workon %s' % server_virtualenvs[version]):
        yield


@task
def pull(version='prod'):
    with cdversion(version):
        run('git pull')


@task
def install_requirements(version='prod'):
    with workon(version):
        with cdversion(version):
            run('pip install -r requirements/base.txt')
            run('pip install -r requirements/production.txt')


@task
def build_static(version='prod'):
    run('django-admin.py collectstatic --noinput')
    with cd(server_project_dir + '/livinglotsnola/collected_static/js/'):
        run('r.js -o app.build.js')


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
