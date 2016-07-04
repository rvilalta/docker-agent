import os.path, sys, os
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be
from objects_docker_agent.container import Container

import containerImpl

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
	cmd = "docker run -d --privileged --net=none --name " + container.Name + " " + container.Image + " &"
	os.system(cmd)
        cmd="ovs-docker add-port " + OVS_BRIDGE + " eth0 " + container.Name + " &"
        os.system(cmd)
        cmd="docker exec " + container.Name + " ifconfig eth0 " + container.Ip + " &"
        os.system(cmd)

    @classmethod
    def delete(cls, ContainerId):
        print 'handling delete'
        if ContainerId in be.Container:
            del be.Container[ContainerId]
            cmd = "docker rm -f " + ContainerId
            os.system(cmd)
            
        else:
            raise KeyError('ContainerId')

    @classmethod
    def get(cls, ContainerId):
        print 'handling get'
	containerImpl.ContainerImpl.get()
        if ContainerId in be.Container:
            return be.Container[ContainerId]
        else:
            raise KeyError('ContainerId')
