#!/usr/bin/python3
"""Generates a .tgz archive"""

from fabric.api import run, put, env
from os.path import exists

env.user = 'ubuntu'
env.hosts = ['35.237.242.122', '54.234.135.146']


def do_deploy(archive_path):
    """Distributes an archive to web servers"""

    if exists(archive_path) is False:
        return False

    file_name = archive_path.split('/')[1]
    fol_name = file_name.split('.')[0]
    route = '/data/web_static/releases/' + fol_name
    try:
        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(route))
        run('rm -rf {}/web_static'.format(route))
        run('rm -rf /data/web_static/current')
        run('ln -s {}/ {}'.format(route, '/data/web_static/current'))
        run('tar -xzf /tmp/{} -C {}/'.format(file_name, route))
        run('rm -rf /tmp/{}'.format(file_name))
        run('cp {}/web_static/* {}/'.format(route))
        return True
    except:
        return False
