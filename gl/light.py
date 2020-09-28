from lib import *

class Light(object):
    def __init__(self,color=(1,1,1), position=V3(0,0,0), intensity=1, is_anaglyph =False):
        self.color = color
        self.position = position
        self.intensity = intensity
        self.is_anaglyph = is_anaglyph


