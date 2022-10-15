"""
Camera module
"""
from __future__ import annotations

import math
from multiprocessing import Pool

#import rt
from rt.canvas import Canvas
from rt.matrix import Matrix
from rt.ray import Ray
from rt.tuple import Point
from rt.world import World


def pixel_render(x, y, camera, world, image):
  """ render a single pixel for parallel testing """
  ray = camera.ray_for_pixel(x, y)
  colour = world.colour_at(ray)
  image.write_pixel(x, y, colour)

def pixel_render_row(x_max, y, camera, world):
  """ render a single row for parallel testing """
  row_data = []
  for x in range(0,x_max):
    ray = camera.ray_for_pixel(x, y)
    colour = world.colour_at(ray)
    row_data.append(colour)
    #image.write_pixel(x, y, colour)
  return row_data

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

  def single_pixel(self, world: World, x: int, y: int) -> None:
    """ debug a single pixel """
    ray = self.ray_for_pixel(x, y)
    world.colour_at(ray)



  def render_parallel(self, world: World) -> Canvas:
    """ parallel render """
    image = Canvas(self.hsize, self.vsize)

    #coordinates = ((x, y, self, world, image) for x in range(self.hsize) for y in range(self.vsize))
    coordinates = ((self.hsize, y, self, world) for y in range(self.vsize))
    with Pool() as pool:
      pool.starmap(pixel_render_row, coordinates)
      # row_data = pool.starmap(pixel_render_row, coordinates)

    return image

  def render(self, world: World) -> Canvas:
    """ render the image """
    image = Canvas(self.hsize, self.vsize)

    for y in range(0, self.vsize):
      for x in range(0, self.hsize):
        ray = self.ray_for_pixel(x, y)
        colour = world.colour_at(ray)
        image.write_pixel(x, y, colour)

    return image

  def render_png(self, world: World) -> Canvas:
    """ render the PNG image """
    image = Canvas(self.hsize, self.vsize)

    for y in range(0, self.vsize):
      for x in range(0, self.hsize):
        ray = self.ray_for_pixel(x, y)
        colour = world.colour_at(ray)
        image.write_pixel_png(x, y, colour)

    return image
