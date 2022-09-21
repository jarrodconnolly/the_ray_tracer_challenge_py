""" Ray Tests """
from rt.matrix import Matrix
from rt.ray import Ray
from rt.tuple import Point, Vector


class TestRay:
  """ features/rays.feature """

  def test_ray(self):
    """ Creating and querying a ray """
    origin = Point(1, 2, 3)
    direction = Vector(4, 5, 6)
    r = Ray(origin, direction)
    assert r.origin == origin
    assert r.direction == direction

  def test_ray_position(self):
    """ Computing a point from a distance """
    r = Ray(Point(2, 3, 4), Vector(1, 0, 0))
    assert r.position(0) == Point(2, 3, 4)
    assert r.position(1) == Point(3, 3, 4)
    assert r.position(-1) == Point(1, 3, 4)
    assert r.position(2.5) == Point(4.5, 3, 4)

  def test_ray_translate(self):
    """ Translating a ray """
    r = Ray(Point(1, 2, 3), Vector(0, 1, 0))
    m = Matrix.translation(3, 4, 5)
    r2 = r.transform(m)
    assert r2.origin == Point(4, 6, 8)
    assert r2.direction == Vector(0,  1, 0)

  def test_ray_scale(self):
    """ Scaling a ray """
    r = Ray(Point(1, 2, 3), Vector(0, 1, 0))
    m = Matrix.scaling(2, 3, 4)
    r2 = r.transform(m)
    assert r2.origin == Point(2, 6, 12)
    assert r2.direction == Vector(0,  3, 0)
