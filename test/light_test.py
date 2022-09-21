""" Light Tests """
from rt.colour import Colour
from rt.light import PointLight
from rt.tuple import Point


class TestPointLight:
  """ features/lights.feature """

  def test_point_light(self):
    """ A point light has a position and intensity """
    intensity = Colour(1, 1, 1)
    position = Point(0, 0, 0)
    light = PointLight(position, intensity)
    assert light.position == position
    assert light.intensity == intensity
