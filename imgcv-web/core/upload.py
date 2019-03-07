import uuid
import os
from PIL import Image
from flask import request


class Upload:
    base_path = os.getcwd() + './static/'

    def run(self, req: request):
        f = req.files['file']
        filename = f.filename
        file_types = filename.split(".")
        file_type = filename.split(".")[len(file_types) - 1]
        file_path = self.base_path + str(uuid.uuid1()) + '.' + file_type
        f.save(file_path)
        return file_path

    def file_info(self, req):
        path = self.run(req)
        im = Image.open(path)
        info = {
            'size': im.size,
            'mode': im.mode,
            'palette': im.palette,
            'format': im.format,
            'info': im.info
        }
        im.close()
        if os.path.exists(path):
            os.remove(path)
        return info

