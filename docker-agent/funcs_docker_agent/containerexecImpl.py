import os.path, sys, os
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))


class ContainerexecImpl:

    @classmethod
    def post(cls, containerexecrpcinputschema):
        print str(containerexecrpcinputschema)
        print 'handling RPC operation'
        cmd="docker exec " + containerexecrpcinputschema.ContainerId + " " + containerexecrpcinputschema.Command
        print cmd
        os.system(cmd)

