from ursina import *

app = Ursina()

sky = Sky()

plane_size = 20
plane = Entity(
    model='plane',
    scale=plane_size,
    color=color.green,
    collider='box'
)

player = Entity(
    model='sphere',
    color=color.red,
    scale=2,
    position=(0, 1, 0),
    collider='sphere'
)

speed = 5

def update():
    move = Vec3(
        held_keys["d"] - held_keys["a"],
        0,
        held_keys["s"] - held_keys["w"]
    ).normalized() * speed * time.dt

    future_position = player.position + move

    # Edge detection logic (half plane size because origin is center)
    boundary = plane.scale_x / 2
    if abs(future_position.x) <= boundary and abs(future_position.z) <= boundary:
        player.position = future_position
        player.color = color.red
    else:
        player.color = color.yellow  # Color on edge collision

DirectionalLight()
EditorCamera()

app.run()
