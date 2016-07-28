from flask import json, Blueprint, request, Response
from flask.views import MethodView
import sys
from objects_common.keyedArrayType import KeyedArrayType, KeyedArrayKeyError

import base64
import re

# BACKEND FUNCTIONS
from funcs_docker_agent.imageImpl import ImageImpl
from funcs_docker_agent.containerContaineridImpl import ContainerContaineridImpl
from funcs_docker_agent.containerImpl import ContainerImpl
from funcs_docker_agent.containerexecImpl import ContainerexecImpl
from funcs_docker_agent.imageImageidImpl import ImageImageidImpl

# CALLABLE OBJECTS
from objects_docker_agent.image import Image
from objects_docker_agent.containerExecRPCInputSchema import ContainerExecRPCInputSchema
from objects_docker_agent.container import Container
from objects_docker_agent.containerExecRPCOutputSchema import ContainerExecRPCOutputSchema

users = {"admin": "pswd1", "user": "pswd2"}

setattr(sys.modules[__name__], __name__,  Blueprint(__name__, __name__))



def byteify(input):
    # Convert JSON unicode strings to python byte strings, recursively on a json_struct
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def json_loads(json_string):
    # Try to use json.loads and raise HTTP Error
    try:
        json_struct = json.loads(json_string) #json parser.
    except ValueError:
        raise BadRequestError("Malformed JSON")
    else:
        return byteify(json_struct)

def json_dumps(js):
    # Pretty-print version of json.dumps
    return json.dumps(js, sort_keys=True, indent=4, separators=(',', ': '))

def create_instance(klass, json_struct, id=None):
    # Try to create an object instance and raise HTTP Errors
    try:
        new_object = klass(json_struct) # Creates an object instance of type klass from the json_struct data
    except KeyError as inst:
        return BadRequestError("Unknown entity name in JSON:" + "<br>" + inst.args[0])
    except TypeError as inst:
        key = inst.args[0]
        value = json.dumps(inst.args[1])
        return BadRequestError("Incorrect type in JSON:" + "<br>" +
                              key + " was:" + "<br>" +
                              value + "<br>" +
                              "Allowed type:" + "<br>" +
                              inst.args[2])
    except ValueError as inst:
        if type(inst.args[1]) == str:
            return BadRequestError("Incorrect value in JSON:" + "<br>" +
                                  "Enum " + inst.args[0] + " was:" + "<br>" +
                                  inst.args[1] + "<br>" +
                                  "Allowed values:" + "<br>" +
                                  "[" + ", ".join(inst.args[2]) + "]")
        elif type(inst.args[1]) == int:
            return BadRequestError("Incorrect value in JSON:" + "<br>" +
                                  "Enum " + inst.args[0] + " was:" + "<br>" +
                                  str(inst.args[1]) + "<br>" +
                                  "Allowed range:" + "<br>" +
                                  "1 - " + str(inst.args[2]))
    except KeyedArrayKeyError as inst:
        return BadRequestError("Error in JSON:" + "<br>" +
                              "Missing key in list:" + "<br>" +
                              inst.args[0] + "<br>" +
                              "Received JSON:" + "<br>" +
                              json.dumps(inst.args[1]) + "<br>" +
                              "Key name:" + "<br>" +
                              inst.args[2])
    else:
        # Check if the id given in the URL matches the id given in the body
        if id != None and id[0] != getattr(new_object, id[1]):
            return BadRequestError(id[1] + " in body not matching " + id[1] + " in URL")
        else:
            return new_object

def modify_instance(existing_object, json_struct):
    try:
        existing_object.load_json(json_struct)
    except KeyError as inst:
        return BadRequestError("Unknown entity name in JSON:" + "<br>" + inst.args[0])
    except TypeError as inst:
        key = inst.args[0]
        value = json.dumps(inst.args[1])
        return BadRequestError("Incorrect type in JSON:" + "<br>" +
                              key + " was:" + "<br>" +
                              value + "<br>" +
                              "Allowed type:" + "<br>" +
                              inst.args[2])
    except ValueError as inst:
        if type(inst.args[1]) == str:
            return BadRequestError("Incorrect value in JSON:" + "<br>" +
                                  "Enum " + inst.args[0] + " was:" + "<br>" +
                                  inst.args[1] + "<br>" +
                                  "Allowed values:" + "<br>" +
                                  "[" + ", ".join(inst.args[2]) + "]")
        elif type(inst.args[1]) == int:
            return BadRequestError("Incorrect value in JSON:" + "<br>" +
                                  "Enum " + inst.args[0] + " was:" + "<br>" +
                                  str(inst.args[1]) + "<br>" +
                                  "Allowed range:" + "<br>" +
                                  "1 - " + str(inst.args[2]))
    except KeyedArrayKeyError as inst:
        return BadRequestError("Error in JSON:" + "<br>" +
                              "Missing key in list:" + "<br>" +
                              inst.args[0] + "<br>" +
                              "Received JSON:" + "<br>" +
                              json.dumps(inst.args[1]) + "<br>" +
                              "Key name:" + "<br>" +
                              inst.args[2])
    else:
        return existing_object


class NotFoundError(Response):
    def __init__(self, message):
        super(NotFoundError, self).__init__()
        self.status = '404 '+message
        self.status_code = 404
        self.headers = {'Content-Type': 'text/html'}
        self.data = '<h1>'+message+'</h1>'

class BadRequestError(Response):
    def __init__(self, message):
        super(BadRequestError, self).__init__()
        self.status = '400 '+message
        self.status_code = 400
        self.headers = {'Content-Type': 'text/html'}
        self.data = '<h1>'+message+'</h1>'

class Unauthorized(Response):
    def __init__(self, message):
        super(Unauthorized, self).__init__()
        self.status = '401 '+message
        self.status_code = 401
        self.headers = {'WWW-Authenticate','Basic realm="Auth example"'}
        self.data = '<h1>'+message+'</h1>'

class Successful(Response):
    def __init__(self, message, info=''):
        super(Successful, self).__init__()
        self.status = '200 '+message
        self.status_code = 200
        self.headers = {'Content-Type': 'application/json'}
        self.data = info


#/restconf/config/Image/
class ImageMethodView(MethodView):

    def get(self, ):
        print "Retrieve operation of resource: Image"
        try:
            response = ImageImpl.get()
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/Container/(\w+)/
class ContainerContaineridMethodView(MethodView):

    def put(self, ContainerId):
        print "Update operation of resource: Container"
        json_struct = request.get_json() #json parser.
        try:
            existing_object = ContainerContaineridImpl.get(ContainerId)
        except (KeyError or NotImplementedError) as inst:
            if inst.args[0] != 'ContainerId':
                return NotFoundError(inst.args[0] + " not found")

            new_object = create_instance(Container, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    ContainerContaineridImpl.put(ContainerId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        
        else:
            existing_object = modify_instance(existing_object, json_struct)
            if isinstance(existing_object, BadRequestError):
                return existing_object
            elif isinstance(existing_object, NotFoundError):
                return existing_object
            else:
                try:
                    ContainerContaineridImpl.put(ContainerId, existing_object)
                    js=existing_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")

        return Successful("Successful operation",json_dumps(js))



    def post(self, ContainerId):
        print "Create operation of resource: Container"
        try:
            response = ContainerContaineridImpl.get(ContainerId)
        except KeyError as inst:
            if inst.args[0] != 'ContainerId':
                return NotFoundError(inst.args[0] + " not found")

            json_struct = request.get_json() #json parser.
            new_object = create_instance(Container, json_struct, (ContainerId,'ContainerId'))
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    ContainerContaineridImpl.post(ContainerId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            return BadRequestError("Object already exists. For updates use PUT.")
        return Successful("Successful operation",json_dumps(js))


    def delete(self, ContainerId):
        print "Delete operation of resource: Container"
        try:
            response=ContainerContaineridImpl.delete(ContainerId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            return Successful('Successful operation')


    def get(self, ContainerId):
        print "Retrieve operation of resource: Container"
        try:
            response = ContainerContaineridImpl.get(ContainerId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/Container/
class ContainerMethodView(MethodView):

    def get(self, ):
        print "Retrieve operation of resource: Container"
        try:
            response = ContainerImpl.get()
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/operations/ContainerExec/
class ContainerexecMethodView(MethodView):

    def post(self, ):
        print "Create operation of resource: ContainerExec"
        json_struct = request.get_json() #json parser.
        new_object = create_instance(ContainerExecRPCInputSchema, json_struct)
        if isinstance(new_object, BadRequestError):
            return new_object
        elif isinstance(new_object, NotFoundError):
            return new_object
        else:
            try:
               ContainerexecImpl.post(new_object)
               js=new_object.json_serializer()
            except KeyError as inst:
                return NotFoundError(inst.args[0] + " not found")

        return Successful("Successful operation",json_dumps(js))



#/restconf/config/Image/(\w+)/
class ImageImageidMethodView(MethodView):

    def get(self, ImageId):
        print "Retrieve operation of resource: Image"
        try:
            response = ImageImageidImpl.get(ImageId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))



getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/Image/", view_func = globals()["ImageMethodView"].as_view('"Image"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/Container/<ContainerId>/", view_func = globals()["ContainerContaineridMethodView"].as_view('"ContainerContainerid"'+'"_api"'), methods=['PUT', 'POST', 'DELETE', 'GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/Container/", view_func = globals()["ContainerMethodView"].as_view('"Container"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/operations/ContainerExec/", view_func = globals()["ContainerexecMethodView"].as_view('"Containerexec"'+'"_api"'), methods=['POST'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/Image/<ImageId>/", view_func = globals()["ImageImageidMethodView"].as_view('"ImageImageid"'+'"_api"'), methods=['GET'])
