""" Plane Tests """
from rt.plane import Plane
from rt.ray import Ray
from rt.tuple import Point, Vector


class TestPlane:
  """ features/planes.feature """

  def test_matrix(self):
    """ The normal of a plane is constant everywhere """
    p = Plane()
    n1 = p.local_normal_at(Point(0, 0, 0))
    n2 = p.local_normal_at(Point(10, 0, -10))
    n3 = p.local_normal_at(Point(-5, 0, 150))
    assert n1 == Vector(0, 1, 0)
    assert n2 == Vector(0, 1, 0)
    assert n3 == Vector(0, 1, 0)

  def test_ray_parallel(self):
    """ Intersect with a ray parallel to the plane """
    p = Plane()
    r = Ray(Point(0, 10, 0), Vector(0, 0, 1))
    xs = p.intersect(r)
    assert len(xs) == 0

  def test_ray_coplanar(self):
    """ Intersect with a coplanar ray """
    p = Plane()
    r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
    xs = p.intersect(r)
    assert len(xs) == 0

  def test_ray_above(self):
    """ A ray intersecting a plane from above """
    p = Plane()
    r = Ray(Point(0, 1, 0), Vector(0, -1, 0))
    xs = p.intersect(r)
    assert len(xs) == 1
    assert xs[0].t == 1
    assert xs[0].object == p

  def test_ray_below(self):
    """ A ray intersecting a plane from below """
    p = Plane()
    r = Ray(Point(0, -1, 0), Vector(0, 1, 0))
    xs = p.intersect(r)
    assert len(xs) == 1
    assert xs[0].t == 1
    assert xs[0].object == p
