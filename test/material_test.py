""" Material Tests """
from math import sqrt
from ray import Colour, Material, Point, PointLight, Vector

class TestMaterial:
  """ features/materials.feature """

  def test_default_material(self):
    """ The default material """
    m = Material()
    assert m.colour == Colour(1, 1, 1)
    assert m.ambient == 0.1
    assert m.diffuse == 0.9
    assert m.specular == 0.9
    assert m.shininess == 200.0

  def test_lighting_eye_between_light_surface(self):
    """ Lighting with the eye between the light and the surface """
    m = Material()
    position = Point(0, 0, 0)
    eyev = Vector(0, 0, -1)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 0, -10), Colour(1, 1, 1))
    result = m.lighting(light, position, eyev, normalv)
    assert result == Colour(1.9, 1.9, 1.9)

  def test_lighting_eye_between_light_surface_45(self):
    """ Lighting with the eye between light and surface, eye offset 45° """
    m = Material()
    position = Point(0, 0, 0)
    eyev = Vector(0, sqrt(2) / 2, -sqrt(2) / 2)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 0, -10), Colour(1, 1, 1))
    result = m.lighting(light, position, eyev, normalv)
    assert result == Colour(1.0, 1.0, 1.0)

  def test_lighting_eye_opposite_surface_light_45(self):
    """ Lighting with eye opposite surface, light offset 45° """
    m = Material()
    position = Point(0, 0, 0)
    eyev = Vector(0, 0, -1)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 10, -10), Colour(1, 1, 1))
    result = m.lighting(light, position, eyev, normalv)
    assert result == Colour(0.7364, 0.7364, 0.7364)

  def test_lighting_eye_path_reflection_vector(self):
    """ Lighting with eye in the path of the reflection vector """
    m = Material()
    position = Point(0, 0, 0)
    eyev = Vector(0, -sqrt(2) / 2, -sqrt(2) / 2)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 10, -10), Colour(1, 1, 1))
    result = m.lighting(light, position, eyev, normalv)
    assert result == Colour(1.6364, 1.6364, 1.6364)

  def test_lighting_behind_surface(self):
    """ Lighting with the light behind the surface """
    m = Material()
    position = Point(0, 0, 0)
    eyev = Vector(0, 0, -1)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 0, 10), Colour(1, 1, 1))
    result = m.lighting(light, position, eyev, normalv)
    assert result == Colour(0.1, 0.1, 0.1)
