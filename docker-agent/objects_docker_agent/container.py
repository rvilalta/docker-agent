from objects_common.jsonObject import JsonObject

class Container(JsonObject):

    def __init__(self, json_struct=None):
        self.Image=""
        self.Hostname=""
        self.Created=""
        self.Status=""
        self.Ip=""
        self.OvsPortName=""
        self.ContainerId=""
        super(Container, self).__init__(json_struct)

