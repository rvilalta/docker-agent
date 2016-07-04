from objects_common.jsonObject import JsonObject

class ContainerExecRPCInputSchema(JsonObject):

    def __init__(self, json_struct=None):
        self.Command=""
        self.ContainerId=""
        super(ContainerExecRPCInputSchema, self).__init__(json_struct)

