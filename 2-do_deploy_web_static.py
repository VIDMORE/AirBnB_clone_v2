#!/usr/bin/python3
"""Generates a .tgz archive"""

from fabric.api import local, run, put, env
from datetime import datetime
from os.path import isfile

env.user = 'ubuntu'
env.hosts = ['35.237.242.122', '54.234.135.146']


def do_pack():
    """Function to compress files"""

    local("mkdir -p versions")
    result = local("tar -czvf versions/web_static_{}.tgz web_static"
                   .format(datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")),
                   capture=True)
    if result.failed:
        return None
    return result


def do_deploy(archive_path):
    """Distributes an archive to web servers"""

    if isfile(archive_path):
        file_name = archive_path.split('/')[1]
        fol_name = file_name.split('.')[0]
        route = '/data/web_static/releases/' + fol_name
        try:
            put(archive_path, '/tmp/')
            run('mkdir -p {}'.format(route))
            run('tar -xzvf /tmp/{} -C {}/'.format(file_name, route))
            run('rm /tmp/{}'.format(file_name))
            run('sudo mv {}/web_static/* {}/'.format(route))
            run('rm -rf {}/web_static'.format(route))
            run('rm -rf /data/web_static/current')
            run('sudo ln -s {}/ {}'.format(route, '/data/web_static/current'))
            return True
        except:
            return False
    else:
        return False
