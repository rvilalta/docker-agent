import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be
import imageImpl 


class ImageImageidImpl:

    @classmethod
    def get(cls, ImageId):
        print 'handling get'
	imageImpl.ImageImpl.get()
        if ImageId in be.Image:
            return be.Image[ImageId]
        else:
            raise KeyError('ImageId')
