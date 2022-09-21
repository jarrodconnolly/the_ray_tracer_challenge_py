""" Ray Tests """
import rt as RT

class TestRay:
  """ features/rays.feature """

  def test_ray(self):
    """ Creating and querying a ray """
    origin = RT.Point(1, 2, 3)
    direction = RT.Vector(4, 5, 6)
    r = RT.Ray(origin, direction)
    assert r.origin == origin
    assert r.direction == direction

  def test_ray_position(self):
    """ Computing a point from a distance """
    r = RT.Ray(RT.Point(2, 3, 4), RT.Vector(1, 0, 0))
    assert r.position(0) == RT.Point(2, 3, 4)
    assert r.position(1) == RT.Point(3, 3, 4)
    assert r.position(-1) == RT.Point(1, 3, 4)
    assert r.position(2.5) == RT.Point(4.5, 3, 4)

  def test_ray_translate(self):
    """ Translating a ray """
    r = RT.Ray(RT.Point(1, 2, 3), RT.Vector(0, 1, 0))
    m = RT.Matrix.translation(3, 4, 5)
    r2 = r.transform(m)
    assert r2.origin == RT.Point(4, 6, 8)
    assert r2.direction == RT.Vector(0,  1, 0)

  def test_ray_scale(self):
    """ Scaling a ray """
    r = RT.Ray(RT.Point(1, 2, 3), RT.Vector(0, 1, 0))
    m = RT.Matrix.scaling(2, 3, 4)
    r2 = r.transform(m)
    assert r2.origin == RT.Point(2, 6, 12)
    assert r2.direction == RT.Vector(0,  3, 0)
