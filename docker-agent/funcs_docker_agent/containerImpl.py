import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be
import requests
import json
from objects_docker_agent.container import Container

URL = "http://127.0.0.1:4243/containers/json"
HEADERS = {'Content-type': 'application/json'}
HOSTNAME = "docker1"

class ContainerImpl:

    @classmethod
    def get(cls, ):
        print 'handling get' 
        return be.Container

