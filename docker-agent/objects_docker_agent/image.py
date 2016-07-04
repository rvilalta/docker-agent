from objects_common.jsonObject import JsonObject

class Image(JsonObject):

    def __init__(self, json_struct=None):
        self.Repository=""
        self.Created=""
        self.ImageId=""
        self.Tag=""
        self.VirtualSize=""
        self.Size=""
        super(Image, self).__init__(json_struct)

