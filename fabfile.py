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

supervisord_programs = {
    'dev': 'devllnola',
    'prod': 'llnola',
}

supervisord_conf = '~/var/supervisor/supervisord.conf'

@contextlib.contextmanager
def cdversion(version, subdir=''):
    """cd to the version of livinglots-nola indicated"""
    with prefix('cd %s' % '/'.join([server_project_dirs[version], subdir])):
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
    with workon(version):
        run('django-admin.py collectstatic --noinput')
        with cdversion(version, 'livinglotsnola/collected_static/js/'):
            run('bower install')
            run('r.js -o app.build.js')


@task
def syncdb(version='prod'):
    with workon(version):
        run('django-admin.py syncdb')


@task
def migrate(version='prod'):
    with workon(version):
        run('django-admin.py migrate')


@task
def restart_django():
    with workon('dev'):
        run('supervisorctl -c %s restart django' % supervisord_conf)


@task
def restart_memcached():
    with workon('dev'):
        run('supervisorctl -c %s restart memcached' % supervisord_conf)


@task
def status():
    with workon('dev'):
        run('supervisorctl -c %s status' % supervisord_conf)


@task
def start(version='prod'):
    pull(version=version)
    install_requirements(version=version)
    syncdb(version=version)
    migrate(version=version)
    build_static(version=version)
    with workon(version):
        run('supervisorctl -c %s start %s' % (supervisord_conf,
                                              supervisord_programs[version]))


@task
def stop(version='prod'):
    with workon(version):
        run('supervisorctl -c %s stop %s' % (supervisord_conf,
                                             supervisord_programs[version]))


@task
def deploy():
    pull()
    install_requirements()
    syncdb()
    migrate()
    build_static()
    restart_django()
