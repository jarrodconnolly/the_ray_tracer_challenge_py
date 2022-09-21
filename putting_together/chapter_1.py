""" Putting It Together - Chapter 1 """
from rt.tuple import Point, Vector


def run():
  """ main entrypoint """
  projectile_position = Point(0, 1, 0)
  projectile_velocity = Vector(1, 1 ,0).normalize()

  environment_gravity = Vector(0, -0.1, 0)
  environment_wind = Vector(-0.01, 0, 0)

  def tick(position, velocity, gravity, wind):
    """ move the projectile """
    new_position = position + velocity
    new_velocity = velocity + gravity + wind
    return (new_position, new_velocity)

  while projectile_position.y > 0:
    (projectile_position, projectile_velocity) = tick(
      projectile_position,
      projectile_velocity,
      environment_gravity,
      environment_wind)
    print(f"{projectile_position.x}, {projectile_position.y}, {projectile_position.z}")

if __name__ == '__main__':
  run()
