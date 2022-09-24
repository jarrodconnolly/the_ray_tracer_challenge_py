""" Camera Tests """

import math

from rt.camera import Camera
from rt.colour import Colour
from rt.matrix import Matrix
from rt.tuple import Point, Vector
from rt.world import World


class TestCamera:
  """ features/camera.feature """

  def test_camera(self):
    """ Constructing a camera """
    c = Camera(160, 120, math.pi / 2)
    assert c.hsize == 160
    assert c.vsize == 120
    assert c.field_of_view == math.pi / 2
    assert c.transform == Matrix.identity()

  def test_pixel_size_horizontal(self):
    """ The pixel size for a horizontal canvas """
    c = Camera(200, 125, math.pi / 2)
    assert math.isclose(c.pixel_size, 0.01)

  def test_pixel_size_vertical(self):
    """ The pixel size for a vertical canvas """
    c = Camera(125, 200, math.pi / 2)
    assert math.isclose(c.pixel_size, 0.01)

  def test_ray_center_canvas(self):
    """ Constructing a ray through the center of the canvas """
    c = Camera(201, 101, math.pi / 2)
    r = c.ray_for_pixel(100, 50)
    assert r.origin == Point(0, 0, 0)
    assert r.direction == Vector(0, 0, -1)

  def test_ray_corner_canvas(self):
    """ Constructing a ray through a corner of the canvas """
    c = Camera(201, 101, math.pi / 2)
    r = c.ray_for_pixel(0, 0)
    assert r.origin == Point(0, 0, 0)
    assert r.direction == Vector(0.66519, 0.33259, -0.66851)

  def test_ray_camera_transformed(self):
    """ Constructing a ray when the camera is transformed """
    c = Camera(201, 101, math.pi / 2)
    c.transform = Matrix.rotation_y(math.pi / 4) * Matrix.translation(0, -2, 5)
    r = c.ray_for_pixel(100, 50)
    assert r.origin == Point(0, 2, -5)
    assert r.direction == Vector(math.sqrt(2) / 2, 0, -math.sqrt(2) / 2)

  def test_render_world_camera(self):
    """ Rendering a world with a camera """
    w = World.DefaultWorld()
    c = Camera(11, 11, math.pi / 2)
    from_p = Point(0, 0, -5)
    to = Point(0, 0, 0)
    up = Vector(0, 1, 0)
    c.transform = from_p.view_transform(to, up)
    image = c.render(w)
    assert image.pixel_at(5, 5) == Colour(0.38066, 0.47583, 0.2855)
