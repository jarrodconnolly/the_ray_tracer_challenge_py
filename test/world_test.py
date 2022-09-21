""" World Tests """
import rt as RT

class TestWorld:
  """ features/world.feature """

  def test_create_world(self):
    """ Creating a world """
    w = RT.World()
    assert len(w.objects) == 0
    assert len(w.lights) == 0

  def test_default_world(self):
    """ The default world """
    w = RT.World.DefaultWorld()
    assert w.lights[0] == RT.PointLight(RT.Point(-10, 10, -10), RT.Colour(1, 1, 1))

    assert w.objects[0] == RT.Sphere(material=RT.Material(
      colour=RT.Colour(0.8, 1.0, 0.6),
      diffuse=0.7,
      specular=0.2))

    assert w.objects[1] == RT.Sphere(transform=RT.Matrix.scaling(0.5, 0.5, 0.5))

  def test_intersect_world_ray(self):
    """ Intersect a world with a ray """
    w = RT.World.DefaultWorld()
    r = RT.Ray(RT.Point(0, 0, -5), RT.Vector(0, 0, 1))
    xs = w.intersect(r)

    assert len(xs) == 4
    assert xs[0].t == 4
    assert xs[1].t == 4.5
    assert xs[2].t == 5.5
    assert xs[3].t == 6
