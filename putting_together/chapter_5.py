""" Putting It Together - Chapter 4 """
import ray as Ray

def run():
  """ main entrypoint """
  canvas_pixels = 512
  canvas = Ray.Canvas(canvas_pixels, canvas_pixels)

  ray_origin = Ray.Point(0, 0, -5)
  wall_z = 10
  wall_size = 7.0

  pixel_size = wall_size / canvas_pixels
  half = wall_size / 2

  material = Ray.Material()
  material.colour = Ray.Colour(0, 0.2, 1)
  shape = Ray.Sphere(material=material)

  light_position = Ray.Point(-10, 10, -10)
  light_colour = Ray.Colour(1, 1, 1)
  light = Ray.PointLight(light_position, light_colour)

  for y in range(0, canvas_pixels):
    world_y = half - pixel_size * y
    for x in range(0, canvas_pixels):
      world_x = -half + pixel_size * x
      position = Ray.Point(world_x, world_y, wall_z)

      ray = Ray.Ray(ray_origin, (position - ray_origin).normalize())
      xs = shape.intersect(ray)

      hit = xs.hit()
      if hit is not None:
        point = ray.position(hit.t)
        normal = hit.object.normal_at(point)
        eye = -ray.direction
        colour = hit.object.material.lighting(light, point, eye, normal)
        canvas.write_pixel(x, y, colour)

  with open("chapter_5.ppm", "w", encoding="utf-8") as ppm_file:
    canvas.canvas_to_ppm(ppm_file)

if __name__ == '__main__':
  run()
