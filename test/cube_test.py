""" Cube Tests """
from rt.cube import Cube
from rt.ray import Ray
from rt.tuple import Point, Vector


class TestCube:
  """ features/cubes.feature """

  def test_cube_intersect(self):
    """ A ray intersects a cube """
    tests = [
      [Point(5, 0.5, 0), Vector(-1, 0, 0), 4, 6],
      [Point(-5, 0.5, 0), Vector(1, 0, 0), 4, 6],
      [Point(0.5, 5, 0), Vector(0, -1, 0), 4, 6],
      [Point(0.5, -5, 0), Vector(0, 1, 0), 4, 6],
      [Point(0.5, 0, 5), Vector(0, 0, -1), 4, 6],
      [Point(0.5, 0, -5), Vector(0, 0, 1), 4, 6],
      [Point(0, 0.5, 0), Vector(0, 0, 1), -1, 1],
    ]
    for test in tests:
      origin = test[0]
      direction = test[1]
      t1 = test[2]
      t2 = test[3]
      c = Cube()
      r = Ray(origin, direction)
      xs = c.intersect(r)
      assert len(xs) == 2
      assert xs[0].t == t1
      assert xs[1].t == t2

  def test_cube_misses(self):
    """ A ray misses a cube """
    tests = [
      [Point(-2, 0, 0), Vector(0.2673, 0.5345, 0.8018)],
      [Point(0, -2, 0), Vector(0.8018, 0.2673, 0.5345)],
      [Point(0, 0, -2), Vector(0.5345, 0.8018, 0.2673)],
      [Point(2, 0, 2), Vector(0, 0, -1)],
      [Point(0, 2, 2), Vector(0, -1, 0)],
      [Point(2, 2, 0), Vector(-1, 0, 0)]
    ]
    for test in tests:
      origin = test[0]
      direction = test[1]
      c = Cube()
      r = Ray(origin, direction)
      xs = c.intersect(r)
      assert len(xs) == 0

  def test_cube_normal(self):
    """ The normal on the surface of a cube """
    tests = [
      [Point(1, 0.5, -0.8), Vector(1, 0, 0)],
      [Point(-1, -0.2, 0.9), Vector(-1, 0, 0)],
      [Point(-0.4, 1, -0.1), Vector(0, 1, 0)],
      [Point(0.3, -1, -0.7), Vector(0, -1, 0)],
      [Point(-0.6, 0.3, 1), Vector(0, 0, 1)],
      [Point(0.4, 0.4, -1), Vector(0, 0, -1)],
      [Point(1, 1, 1), Vector(1, 0, 0)],
      [Point(-1, -1, -1), Vector(-1, 0, 0)]
    ]
    for test in tests:
      c = Cube()
      p = test[0]
      normal = c.local_normal_at(p)
      assert normal == test[1]
