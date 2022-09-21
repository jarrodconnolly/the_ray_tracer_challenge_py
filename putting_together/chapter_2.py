""" Putting It Together - Chapter 2 """
from rt.canvas import Canvas
from rt.colour import Colour
from rt.tuple import Point, Vector


def run():
  """ main entrypoint """
  projectile_position = Point(0, 1, 0)
  projectile_velocity = Vector(1, 1.8 ,0).normalize() * 11.25

  environment_gravity = Vector(0, -0.1, 0)
  environment_wind = Vector(-0.01, 0, 0)

  canvas_width = 900
  canvas_height = 550
  canvas = Canvas(canvas_width, canvas_height)

  def tick(position: Point, velocity: Vector, gravity: Vector, wind: Vector):
    """ move the projectile """
    new_position = position + velocity
    pixel_x = max(min(canvas_width - 1, round(new_position.x)), 0)
    pixel_y = max(min(canvas_height - 1, canvas_height - round(new_position.y)), 0)
    canvas.write_pixel(pixel_x, pixel_y, Colour(0, 0, 1))
    new_velocity = velocity + gravity + wind
    return (new_position, new_velocity)

  while projectile_position.y > 0:
    (projectile_position, projectile_velocity) = tick(
      projectile_position,
      projectile_velocity,
      environment_gravity,
      environment_wind)
    print(f"{projectile_position.x}, {projectile_position.y}, {projectile_position.z}")

  with open("chapter_2.ppm", "w", encoding="utf-8") as ppm_file:
    canvas.canvas_to_ppm(ppm_file)

if __name__ == '__main__':
  run()
