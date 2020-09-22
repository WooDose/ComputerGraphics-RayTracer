from lib import *

class Light(object):
    def __init__(self,color=(1,1,1), position=V3(0,0,0), intensity=1):
        self.color = color
        self.position = position
        self.intensity = intensity


