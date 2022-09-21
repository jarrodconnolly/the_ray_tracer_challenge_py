""" Colour Tests """
import rt as RT

class TestColour:
  """ features/tuples.feature """

  def test_colour(self):
    """ Colors are (red, green, blue) tuples """
    c = RT.Colour(-0.5, 0.4, 1.7)
    assert c.red == -0.5
    assert c.green == 0.4
    assert c.blue == 1.7

  def test_add_colours(self):
    """ Adding colors """
    c1 = RT.Colour(0.9, 0.6, 0.75)
    c2 = RT.Colour(0.7, 0.1, 0.25)
    assert c1 + c2 == RT.Colour(1.6, 0.7, 1.0)

  def test_subtract_colours(self):
    """ Subtracting colors """
    c1 = RT.Colour(0.9, 0.6, 0.75)
    c2 = RT.Colour(0.7, 0.1, 0.25)
    assert c1 - c2 == RT.Colour(0.2, 0.5, 0.5)

  def test_multiply_colour_scalar(self):
    """ Multiplying a color by a scalar """
    c = RT.Colour(0.2, 0.3, 0.4)
    assert c * 2 == RT.Colour(0.4, 0.6, 0.8)

  def test_multiply_colourd(self):
    """ Multiplying colors """
    c1 = RT.Colour(1, 0.2, 0.4)
    c2 = RT.Colour(0.9, 1, 0.1)
    assert c1 * c2 == RT.Colour(0.9, 0.2, 0.04)
