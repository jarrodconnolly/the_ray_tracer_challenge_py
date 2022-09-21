""" Light Tests """
import rt as RT

class TestPointLight:
  """ features/lights.feature """

  def test_point_light(self):
    """ A point light has a position and intensity """
    intensity = RT.Colour(1, 1, 1)
    position = RT.Point(0, 0, 0)
    light = RT.PointLight(position, intensity)
    assert light.position == position
    assert light.intensity == intensity
