import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be
import requests
import json
from objects_docker_agent.container import Container
import subprocess

URL = "http://127.0.0.1:4243/containers/json"
HEADERS = {'Content-type': 'application/json'}

class ContainerImpl:

    @classmethod
    def get_ovs_port_name(cls, ContainerId ):
        print "get_ovs_port_name"
        cmd="ovs-vsctl --data=bare --no-heading --columns=name find interface external_ids:container_id=" + ContainerId + " external_ids:container_iface=eth0"
        print (cmd)
        ovs_port_name = subprocess.check_output(cmd, shell=True)
        print ovs_port_name
        return ovs_port_name

    @classmethod
    def update_info(cls, ):
        print "update_info"
        r = requests.get(URL, headers=HEADERS)
        json_response=json.loads(r.text)
        for container in json_response:
            name = container['Names'][0].split("/")[1]
            be.Container[name].Created=str(container["Created"])
            be.Container[name].Status=container["Status"]

    @classmethod
    def get(cls, ):
        print 'handling get'
        cls.update_info()
        return be.Container

