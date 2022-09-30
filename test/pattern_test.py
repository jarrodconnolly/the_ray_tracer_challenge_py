""" Pattern Tests """
from rt.colour import Colour
from rt.matrix import Matrix
from rt.pattern import Checker, Gradient, Ring, Stripe, UnitTestPattern
from rt.sphere import Sphere
from rt.tuple import Point


class TestPattern:
  """ features/patterns.feature """

  def test_colour_constants(self):
    """ colour constants """
    assert Colour.Black() == Colour(0, 0, 0)
    assert Colour.White() == Colour(1, 1, 1)

  def test_stripe_pattern(self):
    """ Creating a stripe pattern """
    pattern = Stripe(Colour.White(), Colour.Black())
    assert pattern.a == Colour.White()
    assert pattern.b == Colour.Black()

  def test_stripe_pattern_y(self):
    """ A stripe pattern is constant in y """
    pattern = Stripe(Colour.White(), Colour.Black())
    assert pattern.pattern_at(Point(0, 0, 0)) == Colour.White()
    assert pattern.pattern_at(Point(0, 1, 0)) == Colour.White()
    assert pattern.pattern_at(Point(0, 2, 0)) == Colour.White()

  def test_stripe_pattern_z(self):
    """ A stripe pattern is constant in z """
    pattern = Stripe(Colour.White(), Colour.Black())
    assert pattern.pattern_at(Point(0, 0, 0)) == Colour.White()
    assert pattern.pattern_at(Point(0, 0, 1)) == Colour.White()
    assert pattern.pattern_at(Point(0, 0, 2)) == Colour.White()

  def test_stripe_pattern_x(self):
    """ A stripe pattern alternates in x """
    pattern = Stripe(Colour.White(), Colour.Black())
    assert pattern.pattern_at(Point(0, 0, 0)) == Colour.White()
    assert pattern.pattern_at(Point(0.9, 0, 1)) == Colour.White()
    assert pattern.pattern_at(Point(1, 0, 0)) == Colour.Black()
    assert pattern.pattern_at(Point(-0.1, 0, 0)) == Colour.Black()
    assert pattern.pattern_at(Point(-1, 0, 0)) == Colour.Black()
    assert pattern.pattern_at(Point(-1.1, 0, 0)) == Colour.White()

  def test_pattern_object_transform(self):
    """ A pattern with an object transformation """
    o = Sphere()
    o.transform = Matrix.scaling(2, 2, 2)
    pattern = UnitTestPattern()
    c = pattern.pattern_at_shape(o, Point(2, 3, 4))
    assert c == Colour(1, 1.5, 2)

  def test_pattern_transform(self):
    """ A pattern with a pattern transformation """
    o = Sphere()
    pattern = UnitTestPattern()
    pattern.transform = Matrix.scaling(2, 2, 2)
    c = pattern.pattern_at_shape(o, Point(2, 3, 4))
    assert c == Colour(1, 1.5, 2)

  def test_pattern_object_pattern_transform(self):
    """ Stripes with a pattern transformation """
    o = Sphere()
    o.transform = Matrix.scaling(2, 2, 2)
    pattern = UnitTestPattern()
    pattern.transform = Matrix.translation(0.5, 1, 1.5)
    c = pattern.pattern_at_shape(o, Point(2.5, 3, 3.5))
    assert c == Colour(0.75, 0.5, 0.25)

  def test_base_pattern_transform(self):
    """ The default pattern transformation """
    pattern = UnitTestPattern()
    assert pattern.transform == Matrix.identity()

  def test_base_pattern_assign_transform(self):
    """ Assigning a transformation """
    pattern = UnitTestPattern()
    pattern.transform = Matrix.translation(1, 2, 3)
    assert pattern.transform == Matrix.translation(1, 2, 3)

  def test_gradient(self):
    """ gradient pattern """
    pattern = Gradient(Colour.White(), Colour.Black())
    assert pattern.pattern_at(Point(0, 0, 0)) == Colour.White()
    assert pattern.pattern_at(Point(0.25, 0, 0)) == Colour(0.75, 0.75, 0.75)
    assert pattern.pattern_at(Point(0.5, 0, 0)) == Colour(0.5, 0.5, 0.5)
    assert pattern.pattern_at(Point(0.75, 0, 0)) == Colour(0.25, 0.25, 0.25)

  def test_ring(self):
    """ ring pattern """
    pattern = Ring(Colour.White(), Colour.Black())
    assert pattern.pattern_at(Point(0, 0, 0)) == Colour.White()
    assert pattern.pattern_at(Point(1, 0, 0)) == Colour.Black()
    assert pattern.pattern_at(Point(0, 0, 1)) == Colour.Black()
    assert pattern.pattern_at(Point(0.708, 0, 0.708)) == Colour.Black()

  def test_checker_repeat_x(self):
    """ Checkers should repeat in x """
    pattern = Checker(Colour.White(), Colour.Black())
    assert pattern.pattern_at(Point(0, 0, 0)) == Colour.White()
    assert pattern.pattern_at(Point(0.99, 0, 0)) == Colour.White()
    assert pattern.pattern_at(Point(1.01, 0, 0)) == Colour.Black()

  def test_checker_repeat_y(self):
    """ Checkers should repeat in y """
    pattern = Checker(Colour.White(), Colour.Black())
    assert pattern.pattern_at(Point(0, 0, 0)) == Colour.White()
    assert pattern.pattern_at(Point(0, 0.99, 0)) == Colour.White()
    assert pattern.pattern_at(Point(0, 1.01, 0)) == Colour.Black()

  def test_checker_repeat_z(self):
    """ Checkers should repeat in z """
    pattern = Checker(Colour.White(), Colour.Black())
    assert pattern.pattern_at(Point(0, 0, 0)) == Colour.White()
    assert pattern.pattern_at(Point(0, 0, 0.99)) == Colour.White()
    assert pattern.pattern_at(Point(0, 0, 1.01)) == Colour.Black()
