from subprocess import PIPE
import subprocess
import os

from logger import Logger


class DockerComposer:

    logger = Logger()

    def __export_tag(self, version):
        # command = ["echo", "'TAG=" + version +
        #            "'", ">", "../../../FlaskServer/.env"]
        # self.__run_command_pipe(command)
        if os.path.isfile("../../../FlaskServer/.env"):
            os.chdir("../../../FlaskServer/")
            with open(os.getcwd() + ".env", "w") as file:
                file.write("TAG="+version)

    def __run_command_shell(self, command):
        debugcommand = " - {0}".format(" ".join(command))
        self.logger.log(debugcommand)

        retval = subprocess.run(args=command, shell=True, timeout=60,
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.STDOUT)

        return retval

    def __run_command_pipe(self, command):
        debugcommand = " - {0}".format(" ".join(command))
        self.logger.log(debugcommand)

        # process = subprocess.Popen(
        #     command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  # , shell=True)

        # while True:
        #     output = process.stdout.readline()
        #     if process.poll() is not None and output == '':
        #         break
        #     if output:
        #         print(output.strip().decode(), flush=True)
        # retval = process.poll()
        with subprocess.Popen(command, stdout=PIPE, universal_newlines=True) as p:
            for line in p.stdout:
                print(line, end='')

        retval = p.returncode
        self.logger.log(retval)
        if retval != 0:
            self.logger.log(
                f" - Somthing is happend in {command}.\n Please check your command OR repository")
        return retval

    def __update_image_tag(self, container_name, version):
        command = ['docker', 'image', 'tag', "flaskserver_" + container_name +
                   ":latest", "flaskserver_" + container_name + ":" + version]

        retval = self.__run_command_pipe(command)

    def check_image_is_existing(self, container_name, version):
        command = ["docker", "image", "inspect",
                   "flaskserver_" + container_name + ":" + version]

        retval = self.__run_command_pipe(command)

        return retval

    def clean(self, container_name, remove_all):

        if remove_all:
            command = ["docker images", "prune"]
            self.__run_command_pipe(command)
        elif container_name:
            command = ["docker images -q -f dangling=true " + container_name]
            image_ids_byte = self.__run_command_pipe(command)
            image_ids = bytes.decode(image_ids_byte)

            if image_ids != "":
                logger.log("No container")

            for img_id in image_ids.readlines():
                img_id = img_id.decode("utf-8")
                img_id = img_id.replace("\n", "")

                logger.log("Removing container image id " + id)
                # command = ["docker", "rmi", "-f", str(id)]
                # self.run_command(command)

    def remove(self, contiainer_name):

        command = ["docker-compose", "rm", "-s", contiainer_name]

        retval = self.__run_command_pipe(command)

    def build(self, container_name, version, force=False):

        command = ["docker-compose", "build", "--no-cache", container_name]

        retval = self.__run_command_pipe(command)

        if retval == 0:
            if version is not None:
                self.__update_image_tag(container_name, version)
                self.logger.log(" - Build Success # IMAGE NAME = " +
                                container_name + ":" + version + " with ':latest'")
            else:
                self.logger.log(" - Build Success # IMAGE NAME = " +
                                container_name + ":latest' \(ONLY\)")
        else:
            self.logger.log(" - Build Failed" + container_name)

    def up(self, container_name=""):

        self.__export_tag("latest")

        if container_name != "":
            command = ["docker-compose", "up", "-d", container_name]
        else:
            command = ["docker-compose", "up", "-d"]

        retval = self.__run_command_pipe(command)

    def run(self, container_name, version):

        self.__export_tag(version)

        command = ["docker-compose", "up", "-d", container_name]

        retval = self.__run_command_pipe(command)

    def down(self):

        self.__export_tag("latest")

        command = ["docker-compose", "down", "-v", "-t", "30"]

        retval = self.__run_command_pipe(command)
