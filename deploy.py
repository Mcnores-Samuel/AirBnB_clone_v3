#!/usr/bin/python3
from fabric.api import local
from os import path


def do_deploy(archive_path):
    if not path.exists(archive_path):
        return False

    filename = str(archive_path).split("/")[-1]
    releases = "/data/web_static/releases"
    uncompfile = str(filename).split('.')[0]

    local('cp {} /tmp/'.format(archive_path))

    if path.exists("/tmp/{}".format(filename)):
        local('mkdir -p /data/web_static/releases/{}/'.format(uncompfile))
        local('tar -xzf /tmp/{} -C {}/{}/'.format(filename,
                                                  releases,
                                                  uncompfile))
        local('rm /tmp/{}'.format(filename))
        local('rsync -a {}/{}/web_static/ {}/{}'.format(releases,
                                                        uncompfile,
                                                        releases,
                                                        uncompfile))
        local('rm -rf {}/{}/web_static/'.format(releases, uncompfile))

    local('rm -rf /data/web_static/current')
    local('ln -s {}/{} /data/web_static/current'.format(releases, uncompfile))
