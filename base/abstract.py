#!/usr/bin/python

import os
import re
from avocado import utils

RHKEY = "fd431d51"

class ContainerHelper():
    def __init__(self, icontainer):
        #brew-pulp-docker01.web.prod.ext.phx2.redhat.com:8888/rhel7/cockpit-ws:122-5
        #/mnt/redhat/brewroot/packages/cockpit-ws-docker/131/1/images/docker-image-sha256:71df4da82ff401d88e31604439b5ce67563e6bae7056f75f8f6dc715b64b4e02.x86_64.tar.gz
        self.tarbased=True
        self.name="testcontainer"
        self.icontainer = icontainer
        self.prepareEnv()
        self.startDocker()
        self.pullImage()

    def prepareEnv(self):
        process.run("yum -y install docker")

    def startDocker(self):
        if not ".tar.gz" in self.icontainer:
            self.tarbased = False
            registry=re.search("([^/]*)", self.icontainer).groups()[0]
            if registry not in open('/etc/sysconfig/docker', 'rw').read()):
                with open("/etc/sysconfig/docker", "a") as myfile:
                    myfile.write("INSECURE_REGISTRY='--insecure-registry $REGISTRY %s'" % registry)
            process.run("system restart docker")

    def pullImage(self):
        if self.tarbased:
            process.run("docker import %s %s" % (self.icontainer, self.name))
        else:
            process.run("docker pull %s" % self.icontainer)
            self.name = self.icontainer
    

    def containerExec(self, args = "-t -i", command = "/bin/bash"):
        return process.run("docker run %s %s %s" % (args, self.name, command))

    def containerStart(self, args = "-t -i", command = "/bin/bash"):
        process.run("docker run %s %s %s" % (args, self.name, command))
        process.run("docker ps | grep  %s" % self.name)
        self.docker_id = process.run("docker ps | grep %s |cut -d " " -f 1" % self.name,shell=True).stdout

    def containerStop():
        process.run("docker stop %s" % self.docker_id)
        process.run("docker rm %s" % self.docker_id)

    def cockpitSigning():
        # TODO not working because of "'
        if "bin" in self.containerExec(args="--entrypoint /bin/bash",command="ls /"): ...
        if "repolist: 0" in self.containerExec(args="--entrypoint /bin/bash",command="yum repolist"): ...
        packages=self.containerExec(args="--entrypoint /bin/bash",command='rpm -qa --qf="%{name}-%{version}-%{release} %{SIGPGP:pgpsig}\n"').stdout

    def CockcpitLabelCheck(self,text):
        if text in process.run("docker inspect %s"):...


if __name__ == '__main__':
    main()
