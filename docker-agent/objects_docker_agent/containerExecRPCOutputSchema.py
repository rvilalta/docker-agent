from objects_common.jsonObject import JsonObject

class ContainerExecRPCOutputSchema(JsonObject):

    def __init__(self, json_struct=None):
        self.Result=""
        super(ContainerExecRPCOutputSchema, self).__init__(json_struct)

