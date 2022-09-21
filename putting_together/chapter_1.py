""" Putting It Together - Chapter 1 """
import ray as Ray

def run():
  """ main entrypoint """
  projectile_position = Ray.Point(0, 1, 0)
  projectile_velocity = Ray.Vector(1, 1 ,0).normalize()

  environment_gravity = Ray.Vector(0, -0.1, 0)
  environment_wind = Ray.Vector(-0.01, 0, 0)

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
