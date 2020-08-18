#!/usr/bin/python3
"""Generates a .tgz archive"""

from fabric.api import local, run, put, env
from datetime import datetime
from os.path import exists

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
    """
        deploy the archive to the webservers
    """
    if exists(archive_path) is False:
        return False

    filename_wo_ext = archive_path[9:34]
    filename_w_ext = archive_path[9:]
    input_path = "/data/web_static/releases/{}/".format(filename_wo_ext)

    try:
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(input_path))
        run("sudo tar -zxvf /tmp/{} -C {}".format(filename_w_ext, input_path))
        run("sudo rm -rf /tmp/{}".format(filename_w_ext))
        run("sudo mv -n {}/web_static/* {}".format(input_path, input_path))
        run("sudo rm -rf {}/web_static".format(input_path))
        run("sudo rm /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(input_path))
        return True
    except Exception:
        return False


def deploy():
    """Creates and distributes an archive to a web server"""

    filep = do_pack()
    if filep is None:
        return False
    return do_deploy(filep)
