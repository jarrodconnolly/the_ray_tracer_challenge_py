""" Canvas Tests """
from io import StringIO
from ray import Canvas, Colour

class TestCanvas:
  """ features/canvas.feature """

  def test_canvas(self):
    """ Creating a canvas """
    c = Canvas(10, 20)
    assert c.width == 10
    assert c.height == 20
    for x in range(0, 10):
      for y in range(0, 20):
        assert c.pixel_at(x, y) == Colour(0, 0, 0)

  def test_write_pixel(self):
    """ Writing pixels to a canvas """
    c = Canvas(10, 20)
    red = Colour(1, 0, 0)
    c.write_pixel(2, 3, red)
    assert c.pixel_at(2, 3) == red

  def test_ppm_header(self):
    """ Constructing the PPM header """
    c = Canvas(5, 3)
    ppm_data = StringIO(newline="\n")
    c.canvas_to_ppm(ppm_data)
    ppm_data.seek(0)
    ppm_lines = [ line.rstrip("\n") for line in ppm_data ]
    assert ppm_lines[0] == "P3"
    assert ppm_lines[1] == "5 3"
    assert ppm_lines[2] == "255"
    ppm_data.close()

  def test_ppm_data(self):
    """ Constructing the PPM pixel data """
    c = Canvas(5, 3)
    c1 = Colour(1.5, 0, 0)
    c2 = Colour(0, 0.5, 0)
    c3 = Colour(-0.5, 0, 1)
    c.write_pixel(0, 0, c1)
    c.write_pixel(2, 1, c2)
    c.write_pixel(4, 2, c3)

    ppm_data = StringIO(newline="\n")
    c.canvas_to_ppm(ppm_data)
    ppm_data.seek(0)
    ppm_lines = [ line.rstrip("\n") for line in ppm_data ]

    assert ppm_lines[3] == "255 0 0 0 0 0 0 0 0 0 0 0 0 0 0"
    assert ppm_lines[4] == "0 0 0 0 0 0 0 128 0 0 0 0 0 0 0"
    assert ppm_lines[5] == "0 0 0 0 0 0 0 0 0 0 0 0 0 0 255"

    ppm_data.close()

  def test_ppm_long_lines(self):
    """ Splitting long lines in PPM files """
    c = Canvas(10, 2)
    for x in range(0, 10):
      for y in range(0, 2):
        c.write_pixel(x, y, Colour(1, 0.8, 0.6))

    ppm_data = StringIO()
    c.canvas_to_ppm(ppm_data)
    ppm_data.seek(0)
    ppm_lines = [ line.rstrip("\n") for line in ppm_data ]
    assert ppm_lines[3] == "255 204 153 255 204 153 255 204 153 255 204 153 255 204 153 255 204"
    assert ppm_lines[4] == "153 255 204 153 255 204 153 255 204 153 255 204 153"
    assert ppm_lines[5] == "255 204 153 255 204 153 255 204 153 255 204 153 255 204 153 255 204"
    assert ppm_lines[6] == "153 255 204 153 255 204 153 255 204 153 255 204 153"
