"""
Camera module
"""
from __future__ import annotations

import math

#import rt
from rt.canvas import Canvas
from rt.matrix import Matrix
from rt.ray import Ray
from rt.tuple import Point
from rt.world import World


class Camera:
  """
  Camera
  """
  def __init__(self, hsize: int, vsize: int, field_of_view: float) -> Camera:
    self.hsize = hsize
    self.vsize = vsize
    self.field_of_view = field_of_view
    self.transform = Matrix.identity()

    half_view = math.tan(self.field_of_view / 2)
    aspect = self.hsize / self.vsize
    if aspect >= 1:
      self.half_width = half_view
      self.half_height = half_view / aspect
    else:
      self.half_width = half_view * aspect
      self.half_height = half_view
    self.pixel_size = (self.half_width * 2) / self.hsize

  def ray_for_pixel(self, px, py) -> Ray:
    """ get a ray from camera to an x,y on the canvas """
    xoffset = (px + 0.5) * self.pixel_size
    yoffset = (py + 0.5) * self.pixel_size

    world_x = self.half_width - xoffset
    world_y = self.half_height - yoffset

    pixel = self.transform.inverse * Point(world_x, world_y, -1)
    origin = self.transform.inverse * Point(0, 0, 0)
    direction = (pixel - origin).normalize()

    return Ray(origin, direction)

  def render(self, world: World) -> Canvas:
    """ render the image """
    image = Canvas(self.hsize, self.vsize)

    for y in range(0, self.vsize):
      for x in range(0, self.hsize):
        ray = self.ray_for_pixel(x, y)
        colour = world.colour_at(ray)
        image.write_pixel(x, y, colour)

    return image
