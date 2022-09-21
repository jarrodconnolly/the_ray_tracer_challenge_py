""" Intersection Tests """
import ray as Ray

class TestIntersection:
  """ features/intersections.feature """

  def test_intersection(self):
    """ An intersection encapsulates t and object """
    s = Ray.Sphere()
    i = Ray.Intersection(3.5, s)
    assert i.t == 3.5
    assert i.object == s

  def test_intersections(self):
    """ Aggregating intersections """
    s = Ray.Sphere()
    i1 = Ray.Intersection(1, s)
    i2 = Ray.Intersection(2, s)
    xs = Ray.Intersections(i1, i2)
    assert len(xs) == 2
    assert xs[0].t  == 1
    assert xs[1].t == 2

  def test_hit_intersections_positive(self):
    """ The hit, when all intersections have positive t """
    s = Ray.Sphere()
    i1 = Ray.Intersection(1, s)
    i2 = Ray.Intersection(2, s)
    xs = Ray.Intersections(i2, i1)
    i = xs.hit()
    assert i == i1

  def test_hit_intersections_some_negative(self):
    """ The hit, when some intersections have negative t """
    s = Ray.Sphere()
    i1 = Ray.Intersection(-1, s)
    i2 = Ray.Intersection(2, s)
    xs = Ray.Intersections(i2, i1)
    i = xs.hit()
    assert i == i2

  def test_hit_intersections_all_negative(self):
    """ The hit, when all intersections have negative t """
    s = Ray.Sphere()
    i1 = Ray.Intersection(-2, s)
    i2 = Ray.Intersection(-1, s)
    xs = Ray.Intersections(i2, i1)
    i = xs.hit()
    assert i is None

  def test_hit_intersections_lowest_non_negative(self):
    """ The hit is always the lowest nonnegative intersection """
    s = Ray.Sphere()
    i1 = Ray.Intersection(5, s)
    i2 = Ray.Intersection(7, s)
    i3 = Ray.Intersection(-3, s)
    i4 = Ray.Intersection(2, s)
    xs = Ray.Intersections(i1, i2, i3, i4)
    i = xs.hit()
    assert i == i4

  def test_precompute_intersection(self):
    """ Precomputing the state of an intersection """
    r = Ray.Ray(Ray.Point(0, 0, -5), Ray.Vector(0, 0, 1))
    shape = Ray.Sphere()
    i = Ray.Intersection(4, shape)
    comps = i.prepare_computations(r)
    assert comps.t == i.t
    assert comps.object == i.object
    assert comps.point == Ray.Point(0, 0, -1)
    assert comps.eyev == Ray.Vector(0, 0, -1)
    assert comps.normalv == Ray.Vector(0, 0, -1)
