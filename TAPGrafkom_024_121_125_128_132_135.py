from ursina import *
import random as r

app = Ursina()

camera.orthographic = True
camera.fov = 15
world = Entity(model='quad', texture='assets\street',scale=(50,35), collider = 'box', z=1, tag='world')

pohon1  = Sprite(model='quad',texture='assets\puun',scale=0.75, collider = 'box', position=(7,8,0), rotation_z=0, tag="pohon")
pohon2  = Sprite(model='quad',texture='assets\puun',scale=0.75, collider = 'box', position=(7,-8,0), rotation_z=0, tag="pohon")
pohon3  = Sprite(model='quad',texture='assets\puun',scale=0.75, collider = 'box', position=(-7,8,0), rotation_z=0, tag="pohon")
pohon4  = Sprite(model='quad',texture='assets\puun',scale=0.75, collider = 'box', position=(-7,-8,0), rotation_z=0, tag="pohon")
pohon5  = Sprite(model='quad',texture='assets\puun',scale=0.75, collider = 'box', position=(21,15,0), rotation_z=0, tag="pohon")
pohon6  = Sprite(model='quad',texture='assets\puun',scale=0.75, collider = 'box', position=(21,-15,0), rotation_z=0, tag="pohon")
pohon7  = Sprite(model='quad',texture='assets\puun',scale=0.75, collider = 'box', position=(-21,15,0), rotation_z=0, tag="pohon")
pohon8  = Sprite(model='quad',texture='assets\puun',scale=0.75, collider = 'box', position=(-21,-15,0), rotation_z=0, tag="pohon")

# entity player
player = Entity(position=(0,-8))
man = Animation("assets\walking", parent = player, scale=1.5, autoplay=False)
animman = Animator( animations = {
  'idleman': Entity(model='quad',parent=player, scale=1.5,texture='assets\walking_0', tag='player'),
  'walkingman': man,
})

follow = SmoothFollow(target=player, offset=[0,0,-4], speed=8)
camera.add_script(follow)

npcs = []
for i in range(6):
  if i < 3:
    val = -1
    rot = 180
  else:
    rot = 0
    val = 1
  npc = Animation("assets\\npc", x=4, autoplay=True, rotation_z=rot,
                  collider='box', scale=1.5, position=(r.randint(-20,20),r.randint(-20,20)),tag='npc')
  npcs.append((npc,val))

rusab = []
for i in range(4):
  if i < 2:
    val = -1
    rot = 180
  else:
    rot = 0
    val = 1
  rusag = Animation('assets\\usag', x = 5, autoplay=True, rotation_z=rot, collider='box', scale=1.5, position=(r.randint(-20,20),r.randint(-20,20)),tag='npc')
  rusab.append((rusag,val))

bike_mode = False
rusa_makan = False
front_stuck = False
back_stuck = False

bike = Entity(model='quad',texture='assets\ike+org',collider='box', scale=2.5,
         rotation_z=0, y = -10, tag='bike')
bike_speed = 2

def blink():
  if not bike_mode and distance(bike, player) < 1.5:
    dust = Entity(model=Circle(), scale=.3, color=color.smoke, position=bike.position, tag='circle')
    dust.animate_scale(3, duration=.5, curve=curve.linear)
    dust.fade_out(duration=.5)
  invoke(blink, delay=1)
blink()

def update():
  global front_stuck, back_stuck, bike_speed, rusa_makan
  for npc, v in npcs:
    npc.y += v*time.dt
    if v == 1:
      if npc.y > 20:
        npc.y = -20
    else:
      if npc.y < -20:
        npc.y = 20
  for rusag, v in rusab:
    rusag.y += v*time.dt
    if v == 1:
      if rusag.y > 20:
        rusag.y = -20
    else:
      if rusag.y < -20:
        rusag.y = 20
  if bike_mode:
    if bike.tag == 'bike':
      bike.texture = 'assets\ike+org copy'
    player.position = bike.position
    if held_keys['w']:
      bike.rotation_z -= held_keys['a'] * 100 * time.dt
      bike.rotation_z += held_keys['d'] * 100 * time.dt
    elif held_keys['s']:
      bike.rotation_z += held_keys['a'] * 100 * time.dt
      bike.rotation_z -= held_keys['d'] * 100 * time.dt
    else:
      bike_speed = 2
    head_ray = raycast(bike.position,
                       (math.cos(math.radians(360-bike.rotation_z)),math.sin(math.radians(360-bike.rotation_z)),0),
                                 ignore=(bike,),distance=1.5)
    back_ray = raycast(bike.position,
                       (-1*math.cos(math.radians(360-bike.rotation_z)),-1*math.sin(math.radians(360-bike.rotation_z)),0),
                                 ignore=(bike,),distance=0.5)
    if not head_ray.hit or back_stuck or (head_ray.hit and head_ray.entity.tag == 'npc'):
      bike_speed += 0.02
      bike_speed = min(bike_speed, 10)
      bike.x +=held_keys['w']*bike_speed*time.dt * math.cos(math.radians(bike.rotation_z))
      bike.y +=held_keys['w']*-bike_speed*time.dt * math.sin(math.radians(bike.rotation_z))
      front_stuck = False
      if head_ray.hit and head_ray.entity.tag == 'npc':
        Entity(model="quad", texture='assets\corpse', color=color.random_color(),
               scale=0.7, position = head_ray.entity.position, tag='corpse', z=0.5)
        head_ray.entity.disable()
    else:
      front_stuck = True
    if not back_ray.hit or front_stuck or (back_ray.hit and back_ray.entity.tag == 'npc'):
      bike_speed += 0.02
      bike_speed = min(bike_speed, 10)
      bike.x -=held_keys['s']*bike_speed*time.dt * math.cos(math.radians(bike.rotation_z))
      bike.y -=held_keys['s']*-bike_speed*time.dt * math.sin(math.radians(bike.rotation_z))
      back_stuck = False
      if back_ray.hit and back_ray.entity.tag == 'npc':
        Entity(model="quad", texture='assets\corpse', color=color.random_color(),
               scale=0.7, position = back_ray.entity.position, tag='corpse', z=0.5)
        back_ray.entity.disable()
    else:
      back_stuck = True
  else:
    bike.texture = 'assets\ike+org'
    if held_keys['w'] or held_keys['a'] or held_keys['s'] or held_keys['d']:
      player.y += held_keys['w'] * 2 * time.dt
      player.y -= held_keys['s'] * 2 * time.dt
      player.x -= held_keys['a'] * 2 * time.dt
      player.x += held_keys['d'] * 2 * time.dt
      animman.state = 'walkingman'
    else:
      animman.state = 'idleman'
    if held_keys['s']:
      player.rotation_z = 180
    if held_keys['w']:
      player.rotation_z = 0
    if held_keys['d']:
      player.rotation_z = 90
    if held_keys['a']:
      player.rotation_z = 270
    if held_keys['w'] and held_keys['d']:
      player.rotation_z = 45
    if held_keys['w'] and held_keys['a']:
      player.rotation_z = 315
    if held_keys['a'] and held_keys['s']:
      player.rotation_z = 225
    if held_keys['d'] and held_keys['s']:
      player.rotation_z = 135

def input(key):
  global bike_mode, rusa_makan
  if key=='q':
    quit()
  if key == 'b':
    if distance(bike, player) < 1.5:
      if bike_mode:
        bike_mode = False
        player.position = bike.position - (0, 1, 0)
        player.visible = True
        follow.target = player
      else:
        bike_mode = True
        player.visible = False
        follow.target = bike

app.run()