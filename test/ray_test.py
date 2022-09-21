""" Ray Tests """
import ray as Ray

class TestRay:
  """ features/rays.feature """

  def test_ray(self):
    """ Creating and querying a ray """
    origin = Ray.Point(1, 2, 3)
    direction = Ray.Vector(4, 5, 6)
    r = Ray.Ray(origin, direction)
    assert r.origin == origin
    assert r.direction == direction

  def test_ray_position(self):
    """ Computing a point from a distance """
    r = Ray.Ray(Ray.Point(2, 3, 4), Ray.Vector(1, 0, 0))
    assert r.position(0) == Ray.Point(2, 3, 4)
    assert r.position(1) == Ray.Point(3, 3, 4)
    assert r.position(-1) == Ray.Point(1, 3, 4)
    assert r.position(2.5) == Ray.Point(4.5, 3, 4)

  def test_ray_translate(self):
    """ Translating a ray """
    r = Ray.Ray(Ray.Point(1, 2, 3), Ray.Vector(0, 1, 0))
    m = Ray.Matrix.translation(3, 4, 5)
    r2 = r.transform(m)
    assert r2.origin == Ray.Point(4, 6, 8)
    assert r2.direction == Ray.Vector(0,  1, 0)

  def test_ray_scale(self):
    """ Scaling a ray """
    r = Ray.Ray(Ray.Point(1, 2, 3), Ray.Vector(0, 1, 0))
    m = Ray.Matrix.scaling(2, 3, 4)
    r2 = r.transform(m)
    assert r2.origin == Ray.Point(2, 6, 12)
    assert r2.direction == Ray.Vector(0,  3, 0)
