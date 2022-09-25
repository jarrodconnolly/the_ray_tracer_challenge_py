""" Shape Tests """

from rt.material import Material
from rt.matrix import Matrix
from rt.shape import UnitTestShape


class TestShape:
  """ features/shapes.feature """

  def test_default_transform(self):
    """ The default transformation """
    s = UnitTestShape()
    assert s.transform == Matrix.identity()

  def test_assign_transform(self):
    """ Assigning a transformation """
    s = UnitTestShape()
    s.transform = Matrix.translation(2, 3, 4)
    assert s.transform == Matrix.translation(2, 3, 4)

  def test_default_material(self):
    """ The default material """
    s = UnitTestShape()
    assert s.material == Material()

  def test_assign_material(self):
    """ Assigning a material """
    s = UnitTestShape()
    m = Material()
    m.ambient = 1

    s.material = m
    assert s.material == m
