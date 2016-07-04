import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be
import requests
import json
from objects_docker_agent.image import Image

URL = "http://127.0.0.1:4243/images/json"
HEADERS = {'Content-type': 'application/json'}

class ImageImpl:

    @classmethod
    def get(cls, ):
        print 'handling get'
        r = requests.get(URL)
        json_response=json.loads(r.text)
        for image in json_response:
            print image
            repo=image['RepoTags'][0].split(':')[0]
            tags=image['RepoTags'][0].split(':')[1]
            be.Image[image['Id']]=Image({"ImageId":image['Id'], "Repository":repo, "Tag":tags, "Created":str(image["Created"]), "VirtualSize": str(image["VirtualSize"]), "Size":str(image["Size"]) })    
        if be.Image:
            return be.Image
        else:
            raise KeyError('')
