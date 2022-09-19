"""
Material module
"""
from typing import Self
from .colour import Colour
from .tuple import Point, Vector
from .light import PointLight

class Material:
  """
  Material
  """
  def __init__(
    self,
    colour: Colour = Colour(1, 1, 1),
    ambient: float = 0.1,
    diffuse: float = 0.9,
    specular: float = 0.9,
    shininess: float = 200.0) -> Self:
    self.colour = colour
    self.ambient = ambient
    self.diffuse = diffuse
    self.specular = specular
    self.shininess = shininess

  def __eq__(self, other: Self):
    if isinstance(other, Material):
      if(
        self.colour == other.colour and
        self.ambient == other.ambient and
        self.diffuse == other.diffuse and
        self.specular == other.specular and
        self.shininess == other.shininess
      ):
        return True
    return False

  def lighting(
    self,
    light: PointLight,
    point: Point,
    eyev: Vector,
    normalv: Vector) -> Colour:
    """ lighting calculation """

    # combine the surface color with the light's color/intensity
    effective_colour = self.colour * light.intensity

    # find the direction to the light source
    lightv = (light.position - point).normalize()

    # compute the ambient contribution
    ambient = effective_colour * self.ambient

    # light_dot_normal represents the cosine of the angle between the
    # light vector and the normal vector. A negative number means the
    # light is on the other side of the surface.
    light_dot_normal = lightv.dot(normalv)
    if light_dot_normal < 0:
      diffuse = Colour(0, 0, 0)
      specular = Colour(0, 0, 0)
    else:
      # compute the diffuse contribution
      diffuse = effective_colour * self.diffuse * light_dot_normal

      # reflect_dot_eye represents the cosine of the angle between the
      # reflection vector and the eye vector. A negative number means the
      # light reflects away from the eye.
      reflectv = (-lightv).reflect(normalv)
      reflect_dot_eye = reflectv.dot(eyev)

      if reflect_dot_eye <= 0:
        specular = Colour(0, 0, 0)
      else:
        factor = pow(reflect_dot_eye, self.shininess)
        specular = light.intensity * self.specular * factor

    return ambient + diffuse + specular
