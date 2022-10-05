"""
Material module
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from rt.colour import Colour

if TYPE_CHECKING:
  from rt.light import PointLight
  from rt.pattern import Pattern
  from rt.shape import Shape
  from rt.tuple import Point, Vector

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
    shininess: float = 200.0,
    reflective: float = 0.0,
    transparency: float = 0.0,
    refractive_index: float = 1.0,
    pattern: Pattern = None) -> Material:
    self.colour = colour
    self.ambient = ambient
    self.diffuse = diffuse
    self.specular = specular
    self.shininess = shininess
    self.reflective = reflective
    self.transparency = transparency
    self.refractive_index = refractive_index
    self.pattern = pattern

  def __eq__(self, other: Material):
    if isinstance(other, Material):
      if(
        self.colour == other.colour and
        self.ambient == other.ambient and
        self.diffuse == other.diffuse and
        self.specular == other.specular and
        self.shininess == other.shininess and
        self.reflective == other.reflective and
        self.transparency == other.transparency and
        self.refractive_index == other.refractive_index and
        self.pattern == other.pattern
      ):
        return True
    return False

  def lighting(
    self,
    obj: Shape,
    light: PointLight,
    point: Point,
    eyev: Vector,
    normalv: Vector,
    in_shadow: bool = False) -> Colour:
    """ lighting calculation """

    colour = self.colour
    if self.pattern is not None:
      colour = self.pattern.pattern_at_shape(obj, point)

    # combine the surface color with the light's color/intensity
    effective_colour = colour * light.intensity

    # compute the ambient contribution
    ambient = effective_colour * self.ambient

    if in_shadow is True:
      return ambient

    # find the direction to the light source
    lightv = (light.position - point).normalize()

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
