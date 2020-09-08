  
from lib import *
import intersect

class Sphere(object):
  def __init__(self, center, radius, colour):
    self.center = center
    self.radius = radius
    self.colour = colour

  def ray_intersect(self, orig, direction):
    L = sub(self.center, orig)
    # print(direction)
    tca = dot(L, direction)
    l = length(L)
    d2 = l**2 - tca**2
    if d2 > self.radius**2:
      return None
    # print("bigger than radius")
    thc = (self.radius**2 - d2)**1/2
    t0 = tca - thc
    t1 = tca + thc
    if t0 < 0:
      t0 = t1
    if t0 < 0:
      return None

    hit = sum(orig, mul(direction, t0))
    normal = norm(sub(hit, self.center))
    
    return intersect.Intersect(
      distance=t0,
      point=hit,
      normal = normal
    )