import struct
import pprint
import math
from lib import *
from sphere import Sphere
from math import pi
import random
from light import Light

def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(c):
    return struct.pack('=h', c)

def dword(c):
    return struct.pack('=l', c)

def color(r, g, b):
    return bytes([b, g, r])

class Render(object):
    def __init__(self, width, height, vpw, vph, vpx, vpy):
        self.width = width
        self.height = height
        self.framebuffer = []
        self.clearColor = color(0,0,0)
        self.glCreateWindow()
        self.glViewport(vpw, vph, vpx, vpy)
        self.drawColor = color(0,0,0)
        self.glClear()
        self.scene = []

    def glInit(self):
        pass
    
    def glCreateWindow(self):
        print(self.framebuffer)
        self.framebuffer = [
            [self.clearColor for x in range(self.width)]
             for y in range(self.height)
        ]
        #pprint.pprint(self.framebuffer)
    
    def glViewport(self, width, height, x, y):
        self.ViewportWidth = width
        self.ViewportHeight = height
        self.xNormalized = x
        self.yNormalized = y


    def glClear(self):
        self.framebuffer = [
            [self.clearColor for x in range(self.width)]
             for y in range(self.height)
        ]

    def glClearColor(self, r,g,b):
        self.clearColor = color(int(r*255),int(g*255),int(b*255))

    def glColor(self, r,g,b):
        self.drawColor = color(int(r*255),int(g*255),int(b*255))

    def point(self,x,y):
        self.framebuffer[x][y] = self.drawColor

    def glVertex(self, x,y): 
        xW = int(((x+1)*(self.ViewportWidth/2))+self.xNormalized)
        yW = int(((y+1)*(self.ViewportHeight/2))+self.yNormalized)
        xW = (xW - 1) if xW == self.width else xW
        yW = (yW - 1) if yW == self.height else yW
        self.point(xW, yW)

    def glFinish(self, filename):
        f = open(filename, 'bw')

        ## Write file header
        # Header Field
        f.write(char('B'))
        f.write(char('M'))
        # Size in Bytes
        f.write(dword(14 + 40 + (self.width * self.height * 3)))
        #Reserved
        f.write(word(0))
        f.write(word(0))
        #Offset
        f.write(dword(14 + 40))

        # Image header 
        # Bytes in Header
        f.write(dword(40))
        # Width
        f.write(dword(self.width))
        # Height
        f.write(dword(self.height))
        # Color Planes
        f.write(word(1))
        # Bits/Pixel
        f.write(word(24))
        # Pixel array compression
        f.write(dword(0))
        # Size of raw bitmap
        f.write(dword(self.width * self.height * 3))
        #Colors in palette
        f.write(dword(0))
        #Important Colors
        f.write(dword(0))
        # Unused/Reserved
        f.write(dword(0))
        f.write(dword(0))

        # Pixel data
        
        print(self.framebuffer)
        for x in range(self.height):
            for y in range(self.width):
                f.write(self.framebuffer[y][x])
        f.close()
    
    def point(self,x,y):
        self.framebuffer[x][y] = self.drawColor

    def scene_intersect(self, orig, direction):
        zbuffer = float('inf')
        colour = None
        for obj in self.scene:
            intersect = obj.ray_intersect(orig, direction)
            if intersect is not None:
                # print("I intersect")
                if intersect.distance < zbuffer:
                    zbuffer = intersect.distance
                    colour = obj.colour
                    return True, obj.colour, intersect
        return False, (0,0,0), intersect
        
    def cast_ray(self, orig, direction):
        collision, colour , impact = self.scene_intersect(orig, direction)
        
        if collision:
            light_dir = norm(sub(self.light.position, impact.point))
            intensity = max(0,dot(light_dir, impact.normal))
            colour = (colour[0]*intensity, colour[1]*intensity, colour[2]*intensity)
            self.glColor(*colour)           
        else:
            # print("i didn't hit")
            self.glColor(0,0,0)

    def render(self):
        fov = pi/2
        for y in range(self.height):
            for x in range(self.width):
                flip = 1
                if flip >= 1:
                    i =  (2*(x + 0.5)/self.width - 1)*math.tan(fov/2)*self.width/self.height
                    j = -(2*(y + 0.5)/self.height - 1)*math.tan(fov/2)

                    direction = norm(V3(i, j, -1))
                    self.cast_ray(V3(0,0,0), direction)
                    self.point(x,y)

##Please for the love of God don't use non-4 multiples for your dimensions unless you want to absoultely do you know what to your you know what.

bitmap = Render(160,160,160,160, 0, 0)

bitmap.light = Light(
    V3(-1, -1, 1),
    1
)

bitmap.scene = [
    Sphere(V3(0.6, -2.0, -8), 0.15, (0.6,0.6,0.6)), # mouth dots upper right
    Sphere(V3(-0.6, -2.0, -8), 0.15, (0.6,0.6,0.6)), # mouth dots upper left
    Sphere(V3(0.3, -1.75, -8), 0.15, (0.6,0.6,0.6)), # mouth dots lower right
    Sphere(V3(-0.3, -1.75, -8), 0.15, (0.6,0.6,0.6)), # mouth dots lower left
    Sphere(V3(0, -2.5, -8), 0.3, (1,0.2,0)), # nose
    Sphere(V3(-0.45, -2.9, -8), 0.08, (1,1,1)), # eye glare left
    Sphere(V3(0.75, -2.9, -8), 0.08, (1,1,1)), # eye glare right
    Sphere(V3(-0.6, -3, -8), 0.2, (0,0,0)), # eye left
    Sphere(V3(0.6, -3, -8), 0.2, (0,0,0)), # eye right
    Sphere(V3(0, 4, -8), 0.5, (0.3,0.3,0.3)), # buttons lowest
    Sphere(V3(0, 2, -8), 0.5, (0.3,0.3,0.3)), # buttons mid
    Sphere(V3(0, 0, -8), 0.5, (0.3,0.3,0.3)), # buttons highest
    Sphere(V3(0, 3, -8), 3, (0.85,0.85,0.85)), # fat ball
    Sphere(V3(0, 0, -8), 2, (0.85,0.85,0.85)), # middle ball
    Sphere(V3(0, -2.5, -8), 1.5, (0.85,0.85,0.85)), # tiny ball
]

# bitmap.scene = []
# for z in range(-4,-2):
#     for x in range(-3,3):
#         for y in range(-3,3):
#             x_ = float(x/3)
#             y_ = float(y/3)
#             bitmap.scene.append(Sphere(V3(x_,y_,z), 0.5, (1,0,1)))

# bitmap.scene = [
#     Sphere(V3(0, 0, -8), 0.5, (1,1,1)),
#     Sphere(V3(0, 0, -7), 0.5, (0.8,0.6,0.1))

# ]
bitmap.render()


bitmap.glFinish(r'snowman.bmp')

# bitmap.glFinish(r'tests.bmp')


