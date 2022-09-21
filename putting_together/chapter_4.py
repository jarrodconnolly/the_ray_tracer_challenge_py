""" Putting It Together - Chapter 4 """
# import math
import ray as Ray

CANVAS_PIXELS = 128
WALL_Z = 10
WALL_SIZE = 7.0

def run():
  """ main entrypoint """
  canvas = Ray.Canvas(CANVAS_PIXELS, CANVAS_PIXELS)

  colour = Ray.Colour(1, 0, 0)

  ray_origin = Ray.Point(0, 0, -5)


  pixel_size = WALL_SIZE / CANVAS_PIXELS
  half = WALL_SIZE / 2

  shape = Ray.Sphere()

  # shrink y
  #shape.transform = Ray.Matrix.scaling(1, 0.5, 1)
  # shrink x
  #shape.transform = Ray.Matrix.scaling(0.5, 1, 1)
  # shrink it, and rotate it!
  #shape.transform = Ray.Matrix.rotation_z(math.pi / 4) * Ray.Matrix.scaling(0.5, 1, 1)
  # shrink it, and skew it!
  #shape.transform = Ray.Matrix.shearing(1, 0, 0, 0, 0, 0) * Ray.Matrix.scaling(0.5, 1, 1)

  for y in range(0, CANVAS_PIXELS):
    world_y = half - pixel_size * y
    for x in range(0, CANVAS_PIXELS):
      world_x = -half + pixel_size * x
      position = Ray.Point(world_x, world_y, WALL_Z)

      ray = Ray.Ray(ray_origin, (position - ray_origin).normalize())
      xs = shape.intersect(ray)

      if xs.hit() is not None:
        canvas.write_pixel(x, y, colour)

  with open("chapter_4.ppm", "w", encoding="utf-8") as ppm_file:
    canvas.canvas_to_ppm(ppm_file)

if __name__ == '__main__':
  run()
