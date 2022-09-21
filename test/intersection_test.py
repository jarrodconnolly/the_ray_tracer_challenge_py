""" Intersection Tests """
import rt as RT

class TestIntersection:
  """ features/intersections.feature """

  def test_intersection(self):
    """ An intersection encapsulates t and object """
    s = RT.Sphere()
    i = RT.Intersection(3.5, s)
    assert i.t == 3.5
    assert i.object == s

  def test_intersections(self):
    """ Aggregating intersections """
    s = RT.Sphere()
    i1 = RT.Intersection(1, s)
    i2 = RT.Intersection(2, s)
    xs = RT.Intersections(i1, i2)
    assert len(xs) == 2
    assert xs[0].t  == 1
    assert xs[1].t == 2

  def test_hit_intersections_positive(self):
    """ The hit, when all intersections have positive t """
    s = RT.Sphere()
    i1 = RT.Intersection(1, s)
    i2 = RT.Intersection(2, s)
    xs = RT.Intersections(i2, i1)
    i = xs.hit()
    assert i == i1

  def test_hit_intersections_some_negative(self):
    """ The hit, when some intersections have negative t """
    s = RT.Sphere()
    i1 = RT.Intersection(-1, s)
    i2 = RT.Intersection(2, s)
    xs = RT.Intersections(i2, i1)
    i = xs.hit()
    assert i == i2

  def test_hit_intersections_all_negative(self):
    """ The hit, when all intersections have negative t """
    s = RT.Sphere()
    i1 = RT.Intersection(-2, s)
    i2 = RT.Intersection(-1, s)
    xs = RT.Intersections(i2, i1)
    i = xs.hit()
    assert i is None

  def test_hit_intersections_lowest_non_negative(self):
    """ The hit is always the lowest nonnegative intersection """
    s = RT.Sphere()
    i1 = RT.Intersection(5, s)
    i2 = RT.Intersection(7, s)
    i3 = RT.Intersection(-3, s)
    i4 = RT.Intersection(2, s)
    xs = RT.Intersections(i1, i2, i3, i4)
    i = xs.hit()
    assert i == i4

  def test_precompute_intersection(self):
    """ Precomputing the state of an intersection """
    r = RT.Ray(RT.Point(0, 0, -5), RT.Vector(0, 0, 1))
    shape = RT.Sphere()
    i = RT.Intersection(4, shape)
    comps = i.prepare_computations(r)
    assert comps.t == i.t
    assert comps.object == i.object
    assert comps.point == RT.Point(0, 0, -1)
    assert comps.eyev == RT.Vector(0, 0, -1)
    assert comps.normalv == RT.Vector(0, 0, -1)
