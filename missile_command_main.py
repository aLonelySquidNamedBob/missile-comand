from ion import *
from kandinsky import *
from random import randint, choice
from missile_command_classes import *

'''
move() sets new position, renders it, and deletes the old position
draw() renders the new position
delete() removes the old render
'''

def draw_background():
  fill_rect(0, 0, 320, 218, Color.background)
  fill_rect(0, 219, 340, 5, Color.ground)

def create_cities():
  possible_x_positions = [46, 79, 112, 183, 216, 249]
  cities = []
  for pos in possible_x_positions:
    city = City([pos, 210])
    city.draw()
    cities.append(city)
  return cities

def create_silos():
  possible_x_positions = [8, 145, 282]
  silos = []
  for pos in possible_x_positions:
    silo = Silo([pos, 208], 10)
    silos.append(silo)
  return silos

# Setup
draw_background()
cursor = Cursor([100, 100], 3)
cities = create_cities()
silos = create_silos()
targets = cities + silos

# Main Loop
while True:

  # Reset Silos
  for silo in silos:
    silo.draw()
    silo.missiles = 10
    silo.cooldown = 0
  antimissiles = []
  active_silo = silos[0]
  
  # Initialise missiles
  active_missiles = []
  inactive_missiles = []
  for i in range(randint(15, 23)):
    missile = Missile(targets, 0.25)
    inactive_missiles.append(missile)

  # Wave Loop
  for frame in range(3000):
    for silo in silos:
      silo.cooldown += 1
    
    # Summon missiles
    for missile in inactive_missiles:
      if missile.summon_frame == frame:
        active_missiles.append(missile)
        inactive_missiles.remove(missile)

    # Move and Draw missiles
    for missile in active_missiles:
      missile.move()

    # Shoot antimissiles
    if keydown(KEY_ONE) == True and silos[0].missiles > 0 and silos[0].cooldown >= 10: 
      active_silo = silos[0]
    if keydown(KEY_TWO) == True and silos[1].missiles > 0 and silos[1].cooldown >= 10: 
      active_silo = silos[1]
    if keydown(KEY_THREE) == True and silos[2].missiles > 0 and silos[2].cooldown >= 10: 
      active_silo = silos[2]
    
    antimissile = AntiMissile([active_silo.pos.x + 15, active_silo.pos.y], [cursor.pos.x, cursor.pos.y])
    antimissiles.append(antimissile)
    silo.cooldown = 0
    silo.missiles -= 1

    # Move antimissiles
    for am in antimissiles:
      if not am.exploded:
        am.move()
        if am.target_pos.x - 1 < am.pos.x < am.target_pos.x + 1 and am.target_pos.y - 1 < am.pos.y < am.target_pos.y + 1:
          am.delete()
      else:
        am.draw_explosion()
        if am.explosion_frame_index > 70:
          am.delete_explosion()
          antimissiles.remove(am)
          del am
      
      # Collision
      for missile in active_missiles:
        if am.pos.x - am.explosion_width / 2 < missile.pos.x < am.pos.x + am.explosion_width and am.pos.y - am.explosion_width / 2 < missile.pos.y < am.pos.y + am.explosion_width:
          missile.delete()
          active_missiles.remove(missile)
          del missile
          
    for missile in active_missiles:
      missile.move()

    # City Loop
    for city in cities:
      for missile in active_missiles:
        if missile.pos.y >= city.pos.y and city.pos.x <= missile.pos.x <= city.pos.x + city.size.x:
          city.delete()
          city.destroyed = True
          missile.delete()
          active_missiles.remove(missile)
          del missile
    
    # Silo Loop
    for silo in silos:
      if frame % 10 == 0:
        silo.draw_num_of_missiles()
      for missile in active_missiles:
        if missile.pos.y >= silo.pos.y and silo.pos.x <= missile.pos.x <= silo.pos.x + silo.size.x:
          silo.delete()
          silo.missiles = 0
          missile.delete()
          active_missiles.remove(missile)
          del missile
    
    # Cursor
    cursor.move()
    for am in antimissiles:
      am.lock.draw()
