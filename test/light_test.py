""" Light Tests """
import ray as Ray

class TestPointLight:
  """ features/lights.feature """

  def test_point_light(self):
    """ A point light has a position and intensity """
    intensity = Ray.Colour(1, 1, 1)
    position = Ray.Point(0, 0, 0)
    light = Ray.PointLight(position, intensity)
    assert light.position == position
    assert light.intensity == intensity
