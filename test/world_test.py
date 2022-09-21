""" World Tests """
import ray as Ray

class TestWorld:
  """ features/world.feature """

  def test_create_world(self):
    """ Creating a world """
    w = Ray.World()
    assert len(w.objects) == 0
    assert len(w.lights) == 0

  def test_default_world(self):
    """ The default world """
    w = Ray.World.DefaultWorld()
    assert w.lights[0] == Ray.PointLight(Ray.Point(-10, 10, -10), Ray.Colour(1, 1, 1))

    assert w.objects[0] == Ray.Sphere(material=Ray.Material(
      colour=Ray.Colour(0.8, 1.0, 0.6),
      diffuse=0.7,
      specular=0.2))

    assert w.objects[1] == Ray.Sphere(transform=Ray.Matrix.scaling(0.5, 0.5, 0.5))

  def test_intersect_world_ray(self):
    """ Intersect a world with a ray """
    w = Ray.World.DefaultWorld()
    r = Ray.Ray(Ray.Point(0, 0, -5), Ray.Vector(0, 0, 1))
    xs = w.intersect(r)

    assert len(xs) == 4
    assert xs[0].t == 4
    assert xs[1].t == 4.5
    assert xs[2].t == 5.5
    assert xs[3].t == 6
