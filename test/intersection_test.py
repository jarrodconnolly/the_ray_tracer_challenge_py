""" Intersection Tests """
from ray import Intersection, Intersections, Sphere

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
