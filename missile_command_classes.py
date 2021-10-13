from kandinsky import *
from ion import *
from random import randint, choice

class Pos:
  def __init__(self, pos):
      self.x = pos[0]
      self.y = pos[1]

class Color:
  background = (0, 0, 0)
  ground = (255, 255, 0)
  cursor = (255, 255, 255)
  silo = (0, 255, 0)
  city = (0, 0, 255)
  lock = (255, 255, 255)
  text = (255, 255, 255)
  gray = (50, 50, 50)
  missile = (100, 255, 0)
  anti_missile = (100, 0, 255)
  explosion = [(255, 255, 255), (255, 0, 212)]

  
class Silo:
  def __init__(self, pos, num_of_missiles):
    self.pos = Pos(pos)
    self.num_of_missile = num_of_missiles
    self.size = Pos([30, 10])
    self.cooldown = 0
  
  def draw(self):
    fill_rect(self.pos.x, self.pos.y, self.size.x, self.size.y, Color.silo)
  
  def draw_num_of_missiles(self):
    draw_string(str(self.num_of_missiles), self.pos.x, 1, Color.text, Color.background)
  
  def delete(self):
    fill_rect(self.pos.x, self.pos.y, self.size.x, self.size.y, Color.background)


class Missile:
  def __init__(self, available_targets, speed):
    self.pos = Pos([randint(10, 310), 0])
    self.start_pos = Pos([self.pos.x, self.pos.y])
    self.target_pos = Pos([choice(available_targets).pos.x, choice(available_targets).pos.y])
    self.speed = speed
    self.movement = (self.target_pos.x - self.pos.x) / (self.target_pos.y - self.pos.y) * self.speed
    self.summon_frame = randint(1, 2500)
    
  def draw(self):
    set_pixel(round(self.pos.x), round(self.pos.y), Color.missile)

  def delete(self):
    delete_pos = [self.start_pos.x, self.start_pos.y]
    for i in range(self.pos.y / self.speed):
      delete_pos.x += self.movement.x
      delete_pos.y += self.movement.y
      set_pixel(round(delete_pos.x), round(delete_pos.y))

  def move(self):
    self.pos.x = self.movement.x
    self.pos.y = self.movement.y
    self.draw()


class AntiMissile:
  def __init__(self, pos, target_pos) -> None:
    self.pos = Pos(pos)
    self.start_pos = Pos(pos)
    self.target_pos = Pos(target_pos)
    self.lock = LockOnTarget(target_pos)
    self.movement = Pos([None, None])
    self.exploded = False
    self.num_of_moves = 0
    self.explosion_width = 0
    self.explosion_frame_index = 1

    if abs(self.target_pos.x - self.pos.x) > abs(self.target_pos.y - self.pos.y):
      if self.target_pos.x - self.pos.x < 0:
        self.movement.x = -1
      else:
        self.movement.x = 1
      self.movement.y = (self.target_pos.y - self.pos.y) / abs(self.target_pos.x - self.pos.x)
    else:
      self.movement.y = -1
      self.movement.x = (self.target_pos.x - self.pos.x) / abs(self.target_pos.y - self.pos.y)

  def move(self):
    for i in range(0, 2):
      self.pos.x += self.movement.x
      self.pos.y += self.movement.y
      self.draw()
      self.num_of_moves += 1
    
  def draw(self):
    set_pixel(round(self.pos.x), round(self.pos.y), Color.anti_missile)
  
  def delete(self):
    delete = self.start_pos
    for i in self.num_of_moves:
      delete.x += self.movement.x
      delete.y += self.movement.y
      set_pixel(round(delete.x), round(delete.y), Color.background)
    self.exploded = True

  def draw_explosion(self):
    self.explosion_width += 1 if self.explosion_width < 20 else 0
    fill_rect(
      round(self.pos.x - self.explosion_width / 2),
      round(self.pos.y - self.explosion_width / 2),
      self.explosion_width,
      self.explosion_width,
      Color.explosion[self.explosion_frame_index // 2]
    )
    self.explosion_frame_index += 1

  def delete_explosion(self):
    fill_rect(
      round(self.pos.x - self.explosion_width / 2),
      round(self.pos.y - self.explosion_width / 2),
      self.explosion_width,
      self.explosion_width,
      Color.background
    )


class City:
  def __init__(self, pos, destroyed=False) -> None:
    self.pos = Pos(pos)
    self.size = Pos([25, 7])
    self.destroyed = destroyed

  def draw(self):
    fill_rect(self.pos.x, self.pos.y, self.size.x, self.size.y, Color.city)
  
  def delete(self):
    fill_rect(self.pos.x, self.pos.y, self.size.x, self.size.y, Color.background)


class Cursor:
  def __init__(self, pos, size) -> None:
    self.pos = Pos(pos)
    self.last_pos = Pos(pos)
    self.size = size
  
  def draw(self):
    fill_rect(self.pos.x, self.pos.y - self.size, 1, self.size, Color.cursor)
    fill_rect(self.pos.x, self.pos.y + 1, 1, self.size, Color.cursor)
    fill_rect(self.pos.x + 1, self.pos.y, self.size, 1, Color.cursor)
    fill_rect(self.pos.x - self.size, self.pos.y, self.size, 1, Color.cursor)
  
  def delete(self):
    fill_rect(self.last_pos.x, self.last_pos.y - self.size, 1, self.size, Color.cursor)
    fill_rect(self.last_pos.x, self.last_pos.y + 1, 1, self.size, Color.cursor)
    fill_rect(self.last_pos.x + 1, self.last_pos.y, self.size, 1, Color.cursor)
    fill_rect(self.last_pos.x - self.size, self.last_pos.y, self.size, 1, Color.cursor)

  def move(self):
    self.last_pos = Pos([self.pos.x, self.pos.y])
    if keydown(KEY_RIGHT) and self.pos.x < 320 - self.size:
      self.pos.x += 1
    if keydown(KEY_LEFT) and self.pos.x > self.size:
      self.pos.x -= 1
    if keydown(KEY_UP) and self.pos.y > self.size:
      self.pos.y -= 1
    if keydown(KEY_DOWN) and self.pos.y < 222 - 30:
      self.pos.y += 1
    
    if self.last_pos.x != self.pos.x and self.last_pos.y != self.pos.y:
      self.delete()
    self.draw()


class LockOnTarget:
  def __init__(self, pos) -> None:
    self.pos = Pos(pos)
    self.size = 6
    self.frames = 0

  def draw(self):
    if self.frames % 4 == 0:
      for i in range(0, self.size):
        set_pixel(i + self.pos.x - 4, i - self.pos.y + 4, Color.lock)
        set_pixel(i - self.pos.x + 4, i - self.pos.y + 4, Color.lock)
    elif self.frames % 4 == 2:
      for i in range(0, self.size):
        set_pixel(i + self.pos.x - 4, i - self.pos.y + 4, Color.background)
        set_pixel(i - self.pos.x + 4, i - self.pos.y + 4, Color.background)
    self.frames += 1