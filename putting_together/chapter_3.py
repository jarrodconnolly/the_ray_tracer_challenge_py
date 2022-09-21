""" Putting It Together - Chapter 3 """
import math
import ray as Ray

def run():
  """ main entrypoint """
  canvas_size = 1024
  clock_radius = canvas_size * (3/8)
  canvas = Ray.Canvas(canvas_size, canvas_size)
  tick_colour = Ray.Colour(0, 0, 1)
  start = Ray.Point(0, 1, 0)

  for hour in range(0, 12):
    rotation = Ray.Matrix.rotation_z(hour * math.pi / 6)
    position = rotation * start

    x = round(position.x * clock_radius + canvas_size / 2)
    y = round(position.y * clock_radius + canvas_size / 2)

    canvas.write_pixel(x, y, tick_colour)
    canvas.write_pixel(x + 1, y, tick_colour)
    canvas.write_pixel(x - 1, y, tick_colour)
    canvas.write_pixel(x, y + 1, tick_colour)
    canvas.write_pixel(x, y - 1, tick_colour)

  with open("chapter_3.ppm", "w", encoding="utf-8") as ppm_file:
    canvas.canvas_to_ppm(ppm_file)

if __name__ == '__main__':
  run()
