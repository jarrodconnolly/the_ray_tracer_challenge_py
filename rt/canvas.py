"""
Canvas module
"""
from __future__ import annotations

import binascii
import zlib
from io import StringIO, TextIOWrapper
from typing import BinaryIO

#import rt
from rt.colour import Colour


class Canvas:
  """
  Canvas
  """
  def __init__(self, width: int, height: int) -> None:
    self.width = width
    self.height = height
    colour = Colour(0, 0, 0)
    self._canvas = [colour for x in range(self.width * self.height)]
    # data size: width * (3bytes R G B) + (1 byte per row for PNG filter method)
    self._data = bytearray((self.width * 3 + 1) * self.height)

  def write_pixel(self, x: int, y: int, colour: Colour) -> None:
    """ write a pixel to the canvas """
    self._canvas[y * self.width + x] = colour

  def write_pixel_png(self, x: int, y: int, colour: Colour) -> None:
    """ write a pixel to the PNG canvas """
    pos = y * (self.width * 3 + 1) + (x * 3) + 1

    # clamp colour bytes to 0-1 and scale to 0-255
    self._data[pos] = round(max(min(1, colour.red), 0) * 255)
    self._data[pos + 1] = round(max(min(1, colour.green), 0) * 255)
    self._data[pos + 2] = round(max(min(1, colour.blue), 0) * 255)

  def pixel_at(self, x: int, y: int) -> Colour:
    """ read a pixel from the canvas """
    return self._canvas[y * self.width + x]

  def canvas_to_png(self, output_stream: BinaryIO) -> None:
    """ output canvas in PNG format"""

    def write_chunk(chunk_type: str, chunk_data: bytes) -> None:
      """ chunk """
      chunk_data_length = len(chunk_data)
      output_stream.write(chunk_data_length.to_bytes(4, "big"))

      chunk_type_bytes = bytes(chunk_type, "ascii")
      output_stream.write(chunk_type_bytes)
      output_stream.write(chunk_data)

      crc = binascii.crc32(chunk_type_bytes)
      crc = binascii.crc32(chunk_data, crc)
      output_stream.write(crc.to_bytes(4, "big"))

    # PNG Header
    output_stream.write(b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A")

    # IHDR
    ihdr_data = bytearray() # (13 data bytes total)
    ihdr_data.extend(self.width.to_bytes(4, "big")) # width (4 bytes)
    ihdr_data.extend(self.height.to_bytes(4, "big")) # height (4 bytes)
    ihdr_data.extend((8).to_bytes(1, "big")) # bit depth (1 byte, values 1, 2, 4, 8, or 16)
    ihdr_data.extend((2).to_bytes(1, "big")) # 2 (010) red, green and blue: rgb/truecolor
    ihdr_data.extend((0).to_bytes(1, "big")) # compression method (1 byte, value 0)
    ihdr_data.extend((0).to_bytes(1, "big")) # filter method (1 byte, value 0)
    ihdr_data.extend((0).to_bytes(1, "big")) # interlace method (1 byte, values 0 "no interlace" or 1 "Adam7 interlace")
    write_chunk("IHDR", bytes(ihdr_data))

    # IDAT
    # write filter method 0 byte to start each scanline
    for y in range(0, self.height):
      pos = y * (self.width * 3 + 1) + 0
      self._data[pos] = 0

    compressed_data = zlib.compress(self._data)
    write_chunk("IDAT", compressed_data)

    # IEND
    write_chunk("IEND", bytes())

  def canvas_to_ppm(self, output_stream: StringIO|TextIOWrapper) -> None:
    """ output canvas in PPM format """
    output_stream.write("P3\n")
    output_stream.write(f"{self.width} {self.height}\n")
    output_stream.write("255\n")

    row_counter = 0
    row_max = 70

    def write_value(value: float, row_counter: int) -> int:
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
