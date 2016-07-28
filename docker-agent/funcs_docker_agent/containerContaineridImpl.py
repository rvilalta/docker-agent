import os.path, sys, os
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be
from objects_docker_agent.container import Container
from funcs_docker_agent.containerImpl import ContainerImpl
import time

OVS_BRIDGE="ovs-br1"


class ContainerContaineridImpl:

    @classmethod
    def put(cls, ContainerId, container):
        print str(container)
        print 'handling put'
        raise NotImplementedError("Update of repository not allowed")
       

    @classmethod
    def post(cls, ContainerId, container):

        print str(container)
        print 'handling post'
	cmd = "docker run -d --privileged --net=none --name " + container.ContainerId + " " + container.Image + ' /bin/sh -c "while true; do sleep 1; done;"'
	print (cmd)
	os.system(cmd)

        cmd="ovs-docker add-port " + OVS_BRIDGE + " eth0 " + container.ContainerId
	print (cmd)
        os.system(cmd)
        cmd="docker exec " + container.ContainerId + " ifconfig eth0 " + container.Ip
	print (cmd)
        os.system(cmd)
	ContainerImpl.get()

    @classmethod
    def delete(cls, ContainerId):
        print 'handling delete'
        if ContainerId in be.Container:
            cmd = "ovs-docker del-port " + OVS_BRIDGE + " eth0 " + ContainerId
            print cmd
            os.system(cmd)

            cmd = "docker rm -f " + ContainerId
            print cmd
            os.system(cmd)
            
            ContainerImpl.get()           
        else:
            raise KeyError('ContainerId')

    @classmethod
    def get(cls, ContainerId):
        print 'handling get'
	ContainerImpl.get()
        if ContainerId in be.Container:
            return be.Container[ContainerId]
        else:
            raise KeyError('ContainerId')
