"""
Canvas module
"""
from __future__ import annotations
from io import StringIO
from .colour import Colour

class Canvas:
  """
  Canvas
  """
  def __init__(self, width: int, height: int) -> Canvas:
    self.width = width
    self.height = height
    colour = Colour(0, 0, 0)
    self._canvas = [colour for x in range(self.width * self.height)]

  def write_pixel(self, x: int, y: int, colour: Colour) -> None:
    """ write a pixel to the canvas """
    self._canvas[y * self.width + x] = colour

  def pixel_at(self, x: int, y: int) -> Colour:
    """ read a pixel from the canvas """
    return self._canvas[y * self.width + x]

  def canvas_to_ppm(self, output_stream: StringIO) -> None:
    """ output canvas in PPM format """
    output_stream.write("P3\n")
    output_stream.write(f"{self.width} {self.height}\n")
    output_stream.write("255\n")

    row_counter = 0
    row_max = 70

    def write_value(value: float, row_counter: int) -> None:
      value = max(min(1, value), 0)
      value = round(value * 255)
      value_str = str(value)
      if row_counter > 0:
        value_str = " " + value_str

      if row_counter + len(value_str) > row_max:
        output_stream.write("\n")
        row_counter = 0
        value_str = value_str.lstrip()

      output_stream.write(value_str)
      row_counter += len(value_str)

      return row_counter

    for y in range(0, self.height):
      for x in range(0, self.width):
        pixel = self.pixel_at(x, y)
        row_counter = write_value(pixel.red, row_counter)
        row_counter = write_value(pixel.green, row_counter)
        row_counter = write_value(pixel.blue, row_counter)
      output_stream.write("\n")
      row_counter = 0
    output_stream.write("\n")
