""" Intersection Tests """
from rt.intersection import Intersection, Intersections
from rt.matrix import Matrix
from rt.ray import Ray
from rt.sphere import Sphere
from rt.tuple import Point, Vector


class TestIntersection:
  """ features/intersections.feature """

  def test_intersection(self):
    """ An intersection encapsulates t and object """
    s = Sphere()
    i = Intersection(3.5, s)
    assert i.t == 3.5
    assert i.object == s

  def test_intersections(self):
    """ Aggregating intersections """
    s = Sphere()
    i1 = Intersection(1, s)
    i2 = Intersection(2, s)
    xs = Intersections(i1, i2)
    assert len(xs) == 2
    assert xs[0].t  == 1
    assert xs[1].t == 2

  def test_hit_intersections_positive(self):
    """ The hit, when all intersections have positive t """
    s = Sphere()
    i1 = Intersection(1, s)
    i2 = Intersection(2, s)
    xs = Intersections(i2, i1)
    i = xs.hit()
    assert i == i1

  def test_hit_intersections_some_negative(self):
    """ The hit, when some intersections have negative t """
    s = Sphere()
    i1 = Intersection(-1, s)
    i2 = Intersection(2, s)
    xs = Intersections(i2, i1)
    i = xs.hit()
    assert i == i2

  def test_hit_intersections_all_negative(self):
    """ The hit, when all intersections have negative t """
    s = Sphere()
    i1 = Intersection(-2, s)
    i2 = Intersection(-1, s)
    xs = Intersections(i2, i1)
    i = xs.hit()
    assert i is None

  def test_hit_intersections_lowest_non_negative(self):
    """ The hit is always the lowest nonnegative intersection """
    s = Sphere()
    i1 = Intersection(5, s)
    i2 = Intersection(7, s)
    i3 = Intersection(-3, s)
    i4 = Intersection(2, s)
    xs = Intersections(i1, i2, i3, i4)
    i = xs.hit()
    assert i == i4

  def test_precompute_intersection(self):
    """ Precomputing the state of an intersection """
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    shape = Sphere()
    i = Intersection(4, shape)
    comps = i.prepare_computations(r)
    assert comps.t == i.t
    assert comps.object == i.object
    assert comps.point == Point(0, 0, -1)
    assert comps.eyev == Vector(0, 0, -1)
    assert comps.normalv == Vector(0, 0, -1)

  def test_hit_intersection_outside(self):
    """ The hit, when an intersection occurs on the outside """
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    shape = Sphere()
    i = Intersection(4, shape)
    comps = i.prepare_computations(r)
    assert comps.inside is False

  def test_hit_intersection_inside(self):
    """ The hit, when an intersection occurs on the inside """
    r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
    shape = Sphere()
    i = Intersection(1, shape)
    comps = i.prepare_computations(r)
    assert comps.point == Point(0, 0, 1)
    assert comps.eyev == Vector(0, 0, -1)
    assert comps.inside is True
    assert comps.normalv == Vector(0, 0, -1)

  def test_hit_offset_point(self):
    """ The hit should offset the point """
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    shape = Sphere()
    shape.transform = Matrix.translation(0, 0, 1)
    i = Intersection(5, shape)
    comps = i.prepare_computations(r)
    assert comps.over_point.z < -1e-05 / 2
    assert comps.point.z > comps.over_point.z
