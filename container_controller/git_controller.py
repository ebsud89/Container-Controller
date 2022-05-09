import os
import subprocess
import re

from container_controller.logger import *

import pdb

CURRENT_PATH = ""
GIT_PATH = "../../../FlaskServer/"


REPO_DICT = {
    "io": "FlaskServer-Web-io",
    "kr": "FlaskServer-Web-kr",
    "mobile": "FlaskServer-Mobile",
}

BRANCH_DICT = {
    "prod": "master",
    "devel": "develop"
}


class GitController():

    repo_name = ""
    branch_name = ""

    def __parse_container_name(self, container_name):

        # if re.match('kr', container_name):
        #     self.repo_name = REPO_DICT["kr"]
        # elif re.match('io', container_name):
        #     self.repo_name = REPO_DICT["io"]
        # elif re.match('mobile', container_name):
        #     self.repo_name = REPO_DICT["mobile"]
        # else:
        #     assert()

        if container_name.find('kr') != -1:
            self.repo_name = REPO_DICT["kr"]
        elif container_name.find('io') != -1:
            self.repo_name = REPO_DICT["io"]
        elif container_name.find('mobile') != -1:
            self.repo_name = REPO_DICT["mobile"]
        else:
            assert()

        if re.search(r"prod\b", container_name):
            self.branch_name = BRANCH_DICT["prod"]
        elif re.search(r"devel\b", container_name):
            self.branch_name = BRANCH_DICT["devel"]
        else:
            assert()

    def get_all_branches(self, repo_name):

        print("get_all_branch\n")
        os.chdir(GIT_PATH + repo_name)

        proc = subprocess.Popen(['git', 'branch'], stdout=subprocess.PIPE)
        stdout, _ = proc.communicate()

        print(sorted(v.strip(' *')
                     for v in stdout.decode('utf-8').split('\n') if v), end="\n\n")

    def checkout_branch(self, container_name, custom_branch_name="", origin=False):

        logger = Logger()

        self.__parse_container_name(container_name)

        logger.log(f"  --- MOVE PATH {os.getcwd()} / {self.repo_name}")
        os.chdir(os.getcwd() + "/" + self.repo_name)

        if custom_branch_name == "":
            logger.log(
                f"  - GIT CONTROLLER : checkout_brnach {self.repo_name} / {self.branch_name}")
            if origin:
                proc = subprocess.Popen(
                    ['git', 'checkout', '-t', "origin/" + self.branch_name], stdout=subprocess.PIPE)
                stdout, stderr = proc.communicate()
            else:
                proc = subprocess.Popen(
                    ['git', 'checkout', self.branch_name], stdout=subprocess.PIPE)
                stdout, stderr = proc.communicate()
        else:
            if self.branch_name == BRANCH_DICT["prod"]:
                logger.log(
                    f" ----- {cusmtom_branch_name} is not allowed for building PRODUCTION container")
            else:
                logger.log(
                    f"  - GIT CONTROLLER : checkout brnach {self.repo_name} / {custom_branch_name}")
                proc = subprocess.Popen(
                    ['git', 'checkout', custom_branch_name], stdout=subprocess.PIPE)
                stdout, stderr = proc.communicate()

        if stderr is None:
            logger.log(
                f"  - GIT CONTROLLER : pulling branch {self.repo_name} / {custom_branch_name}")
            proc = subprocess.Popen(
                ['git', 'pull', 'origin', self.branch_name]
            )
            stdout, _ = proc.communicate()
        else:
            logger.log(
                f" - GIT CONTROLLER: ERROR in checkout branch (please check branch's name)")
            logger.log(f"  - ERROR : {stderr}")

        # logger.log(sorted(v.strip(' *')
        #            for v in stdout.decode('utf-8').split('\n') if v))


if __name__ == "__main__":
    CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

    container_name = "flask-web-kr-devel"

    git_controller = GitController()

    # parse = git_controller.parse_container_name(container_name)
    # print(parse, end="\n\n")

    git_controller.get_all_branches(parse[0])
    git_controller.checkout_branch(parse[1])
