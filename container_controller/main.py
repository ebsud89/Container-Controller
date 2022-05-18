from tabnanny import verbose
from telnetlib import DO
import click
import re
import subprocess
from datetime import datetime
import os
import sys

import pdb

from container_controller.logger import *
from container_controller.docker_composer import *
from container_controller.git_controller import *

CONTAINER_NAMES = [
    # Flask Server
    'flask-web-kr-prod',
    'flask-web-kr-devel',
    'flask-web-io-prod',
    'flask-web-io-devel',
    'flask-mobile-prod',
    'flask-mobile-devel',
    'proxy-nginx',
    # 'django-mobile-prod',
    # 'django-mobile-devel'
    'flask-mysql',

    # Frontend
    'webview-prod',
    'webview-devel'
]


BACKEND_DOCKER_COMPOSE_PATH = os.path.expanduser('~/FlaskServer/')
FRONTND_DOCKER_COMPOSE_PATH = os.path.expanduser('~/DasomM-WebView/')

CONTEXT_SETTING = dict(help_option_names=['-h', '--help'])


def validate_container(container_name):
    return True if container_name in CONTAINER_NAMES else False


def validate_version_form(version):
    check = re.match('[\d\.]+\d', version)
    if check:
        return True
    else:
        return False


def check_docker_compose_path():
    if os.path.isdir(BACKEND_DOCKER_COMPOSE_PATH):
        os.chdir(BACKEND_DOCKER_COMPOSE_PATH)
    elif os.path.isdir(FRONTND_DOCKER_COMPOSE_PATH):
        os.chdir(FRONTND_DOCKER_COMPOSE_PATH)
    else:
        assert()


@ click.group(context_settings=CONTEXT_SETTING)
def controller():
    """ 
    Data Team's Docker Container Controller Command (version 1.0.5)

        * SUPPORTED CONTAINER

    \b
          - flask-web-io-prod
          - flask-web-io-devel
          - flask-web-kr-prod
          - flask-web-kr-devel
          - flask-mobile-prod
          - flask-mobile-devel

          - webview-prod
          - webview-devel

        * NOT SUPPORTED

    \b
          - proxy-nginx
          - cache-mysql
    """
    pass


@ click.command()
@ click.option('-n', '--container_name', is_flag=False, required=False, help="container_name")
@ click.option('-a', '--remove_all', is_flag=True, required=False, help="Remove ALL dangingling Image")
def clean(container_name, remove_all):
    """ CLEAN Old & Dangling IMAGE """
    logger = Logger()
    docker_composer = DockerComposer()

    if os.path.isdir(FRONTND_DOCKER_COMPOSE_PATH):
        logger.log("DOCKER COMPOSE - CLEAN (start / remove all dangling images)")
        docker_composer.clean('webview', True)
    else:
        logger.log("DOCKER COMPSSE - CLEAN (Not allowed in Flask-Server")

    logger.log("DOCKER COMPOSE - CLEAN (end)")


@ click.command()
@ click.argument("container_name")
def remove(container_name):
    """ REMOVE [$container_name] Container"""
    logger = Logger()
    docker_composer = DockerComposer()

    check_docker_compose_path()

    if not validate_container(container_name):
        logger.log("  --- " + container_name + " is Not exist in Docker")
        return
    else:
        logger.log(" - Removed " + container_name)
        docker_composer.remove(contiainer_name)


@ click.command()
@ click.argument("container_name")
@ click.option('-v', '--version', is_flag=False, required=True, help="attach TAG's at container is building (X.Y.Z)", default="latest")
@ click.option('-b', '--branch', is_flag=False, required=False, help="Check out LOCAL custom branch in repository")
@ click.option('-r', '--remote', is_flag=False, required=False, help="Check out REMOTE custom branch in repository")
@ click.option('-f', '--force', is_flag=True, required=False, help="force add tag")
def build(container_name, version, branch, remote, force):
    """ BUILD Container Image"""
    logger = Logger()
    docker_composer = DockerComposer()
    git_controller = GitController()

    check_docker_compose_path()

    if not validate_container(container_name):
        logger.log("  --- " + container_name +
                   " is Not Container for DATA TEAM's Service")
        return

    if version:
        if not validate_version_form(version):
            logger.log("  === Pleas input correct version form")
        else:
            retval = docker_composer.check_image_is_existing(
                container_name, version)

            if (retval == 0) or force:
                logger.log("  --- " + container_name +
                           " is Not exist in Docker Images")
                logger.log("  --- " + container_name +
                           ":latest & :" + version + " IMAGE will be created")
            else:
                logger.log("  --- " + container_name +
                           " is already exist in Docker Images")
                logger.log("  --- " + container_name +
                           ":latest will be created only & existing "
                           + container_name + ":" + version + " will be changed")

            if branch:
                custom_branch_name = branch
                git_controller.checkout_branch(
                    container_name, custom_branch_name)
                docker_composer.build(container_name, version)
            elif remote:
                custom_branch_name = remote
                git_controller.checkout_branch(
                    container_name, custom_branch_name, True)
                docker_composer.build(container_name, version)
            else:
                git_controller.checkout_branch(container_name)
                docker_composer.build(container_name, version)
    else:
        if force:
            logger.log("  --- " + container_name +
                       ":latest IMAGE will be only created \(Not Recommanded\)")
            git_controller.checkout_branch(container_name)
            docker_composer.build(container_name, version, True)
        else:
            logger.log("  --- " + container_name +
                       ":latest IMAGE will be only created \(Not Recommanded\)\n Please use '-f' or '--force' option to build image forcely.")


@ click.command()
def up():
    """
    Re-run All container using modified images

    \b
    (do this after building container's image)
    """

    logger = Logger()
    docker_composer = DockerComposer()

    check_docker_compose_path()

    docker_composer.up()

    logger.log(" - Run RE-built Container (Not impact UP-TO-DATE container)")


@ click.command()
@ click.argument("container_name")
@ click.option('-v', '--version', is_flag=False, required=False, help="(NOT IMPLEMENTED) attach TAG's at container is building (X.Y.Z)", default="latest")
def run(container_name, version):
    """
    Re-run [$container_name] Container (STOPPED)

    \b
    (do this after building container's image)
    """
    logger = Logger()
    docker_composer = DockerComposer()

    check_docker_compose_path()

    if version:
        docker_composer.run(container_name, version)
    else:
        docker_composer.run(container_name, "latest")

    logger.log(" - Run RE-built Container (Not impact UP-TO-DATE container)")


@ click.command()
@ click.argument("container_name")
def restart(container_name):
    """
    Re-Start [$container_name] Container (RUNNING)

    \b
    (do this after building container's image)
    """
    logger = Logger()
    docker_composer = DockerComposer()

    check_docker_compose_path()

    if container_name.find("nginx") != -1:
        docker_composer.reload_nginx()
        logger.log(" - Run RE-built Container (Not impact UP-TO-DATE container)")


@ click.command()
@ click.option('-f', '--force', is_flag=True, required=False, help="All Container Will be down \(required -f \(force\)\)")
def down(force):
    """  DownAll FlaskServer Container """
    logger = Logger()
    docker_composer = DockerComposer()

    check_docker_compose_path()

    if force:
        logger.log(
            " - All Contiainer is going down within 30s with anomynous volume")
        docker_composer.down()
    else:
        logger.log(
            " - Are you sure to CONTINUE ? Please use \'f \(force\)\' flag ")


def main():
    controller.add_command(clean)
    controller.add_command(remove)
    controller.add_command(build)
    controller.add_command(up)
    controller.add_command(run)
    controller.add_command(restart)
    controller.add_command(down)
    controller()


if __name__ == "__main__":
    main()
