from pycat.core import Window, Sprite, Color, Label, KeyCode, RotationMode
from enum import Enum, auto
from random import choice
from os.path import dirname


w = Window(enforce_window_limits=False)


time = 0
with open(dirname(__file__) + '/fastest_time_sealedvessel.txt', 'r') as file:
    fastest_time = int(file.readline())


class PlayerState(Enum):
    WAIT = auto()
    JUMP = auto()
    WALK = auto()
    FLY = auto()
    ATTACK = auto()

class BossState1(Enum):
    WAIT = auto()
    MOVE = auto()
    ATTACK1 = auto()
    ATTACK2 = auto()
    ATTACK3 = auto()
    ATTACK4 = auto()
    ATTACK5 = auto()
    ATTACK6 = auto()

bossattack1 = [BossState1.ATTACK1,BossState1.ATTACK2,BossState1.ATTACK3,BossState1.ATTACK4,BossState1.ATTACK5]


class Health(Label):

    def on_update(self, dt):
        self.text = 'HP:' + str(player.health)
        if player.health < 1 or boss1.health < 1:
            self.delete()

    
class BossHealth(Label):

    def on_update(self, dt):
        self.text = 'BOSS:' + str(boss1.health)
        if player.health < 1 or boss1.health < 1:
            self.delete()


class Time(Label):

    def on_create(self):
        self.d = 0

    def on_update(self, dt):
        global time
        self.d += dt
        if self.d > 1:
            time += 1
            self.d = 0
        self.text = 'Time:' + str(time)
        if player.health < 1 or boss1.health < 1:
            self.delete()


class FastestTime(Label):

    def on_create(self):
        self.text = 'FastestTime:' + str(fastest_time)
    def on_update(self, dt):
        if player.health < 1 or boss1.health < 1:
            self.delete()



class End1(Label):

    def on_create(self):
        self.text = 'YOU WIN'


class End2(Label):

    def on_create(self):
        self.text = 'YOU LOSE'



class HollowKnight(Sprite):


    def on_create(self):
        self.scale = 50
        self.color = Color.AMBER
        self.state = PlayerState.JUMP
        self.g = 0.2
        self.y_speed = 0
        self.jump_time = 0
        self.speed = 10
        self.rotation = 90
        self.rotation_mode = RotationMode
        self.health = 100
    
    def on_update(self, dt):
        if self.health < 1:
            w.create_label(End2, x=300, y=400, font_size=100)
            self.delete()
        if boss1.health < 1:
            self.delete()
        if w.is_key_down(KeyCode.C):
            self.x += 200*self.rotation/90
        if w.is_key_down(KeyCode.X):
            self.color = Color.PURPLE
            if self.is_touching_sprite(boss1):
                boss1.health += -1
            self.color = Color.AMBER
        if self.state is PlayerState.JUMP:
            self.y -= self.y_speed
            if w.is_key_pressed(KeyCode.RIGHT) or w.is_key_pressed(KeyCode.LEFT):
                self.state = PlayerState.FLY
            if w.is_key_down(KeyCode.Z) and self.jump_time < 2:
                self.y_speed = -8
                self.jump_time += 1
            if self.y_speed < 10:
                self.y_speed += self.g
            if self.is_touching_any_sprite_with_tag('floor') and self.y_speed>0:
                self.state = PlayerState.WAIT
                self.y_speed = 0
                self.jump_time = 0

        # wait state
        if self.state is PlayerState.WAIT:
            if w.is_key_down(KeyCode.Z):
                self.state = PlayerState.JUMP
                self.y_speed = -8
                self.jump_time += 1
            if self.move_left_right_if_press_keys():
                self.state = PlayerState.WALK
        
        # walk state
        if self.state is PlayerState.WALK:
            if w.is_key_pressed(KeyCode.Z):
                self.state = PlayerState.FLY
            if not self.move_left_right_if_press_keys():
                self.state = PlayerState.WAIT

        # fly 
        if self.state is PlayerState.FLY:
            self.y -= self.y_speed
            if w.is_key_down(KeyCode.Z) and self.jump_time < 2:
                self.y_speed = -8
                self.jump_time += 1
            if self.y_speed < 10:
                self.y_speed += self.g
            
            if not self.move_left_right_if_press_keys():
                self.state = PlayerState.JUMP
            if self.is_touching_any_sprite_with_tag('floor') and self.y_speed>0:
                self.state = PlayerState.WAIT
                self.y_speed = 0
                self.jump_time = 0

        if w.is_key_down(KeyCode.X):
            self.add_tag('attack')
        else:
            self.color = Color.AMBER
            if 'attack' in self.tags:
                self.remove_tag('attack')


    def move_left_right_if_press_keys(self):
        if w.is_key_pressed(KeyCode.LEFT):
            self.x -= self.speed
            self.rotation = -90
            return True
        if w.is_key_pressed(KeyCode.RIGHT):
            self.x += self.speed
            self.rotation = 90
            return True
        return False

class Backgound_floor(Sprite):


    def on_create(self):
        self.height = 300
        self.width = 2000
        self.color = Color.WHITE
        self.add_tag('floor')

    def on_update(self, dt):
        if player.health < 1 or boss1.health < 1:
            self.delete()

class PureVessel(Sprite):

    def on_create(self):
        self.height = 100
        self.width = 100
        self.color = Color.CYAN
        self.state = BossState1.WAIT
        self.time = 0
        self.rotation_mode = RotationMode
        self.way = -1
        self.health = 40

    def on_update(self, dt):
        if self.health < 1:
            w.create_label(End1, x=300, y=400, font_size=100)
            if time < fastest_time:
                with open(dirname(__file__) + '/fastest_time_sealedvessel.txt', 'w') as file:
                    fastest_time = time
                    file.write(str(fastest_time))
            self.delete()
        if player.health < 1:
            self.delete()
        if self.x > 1800:
            self.x = 1800
        if self.x < -100:
            self.x = -100
        if self.y < 100:
            self.y = 100
        if self.state is BossState1.WAIT:
            self.color = Color.CYAN
            self.time += dt
            if self.time > 0.5:
                self.color = Color.RED
            if self.time > 1:
                self.state = choice(bossattack1)
                if player.x < self.x:
                    self.way = -1
                else:
                    self.way = 1
                if self.state is BossState1.ATTACK5:
                    self.x = player.x
                    self.y = 500
                self.time = 0
        if self.state is BossState1.ATTACK1:
            self.x += 6*self.way
            self.time += dt
            self.color = Color.PURPLE
            if self.is_touching_sprite(player):
                player.health += -1
            if self.time > 0.7:
                self.state = BossState1.WAIT
                self.time = 0
        if self.state is BossState1.ATTACK2:
            self.x += 20*self.way
            self.time += dt
            self.color = Color.PURPLE
            if self.is_touching_sprite(player):
                player.health += -1
            if self.time > 0.5:
                self.state = BossState1.WAIT
                self.time = 0
        if self.state is BossState1.ATTACK3:
            w.create_sprite(Bullet, position=self.position)
            self.time += dt
            if self.time > 0.5:
                self.state = BossState1.WAIT
                self.time = 0
        if self.state is BossState1.ATTACK4:
            self.x = player.x
            self.state = BossState1.WAIT
        if self.state is BossState1.ATTACK5:
            self.y += -10
            self.time += dt
            self.color = Color.PURPLE
            if self.is_touching_sprite(player):
                player.health += -1
            if self.time > 0.7:
                self.y = 100
                self.state = BossState1.WAIT
                self.time = 0

class Bullet(Sprite):


    def on_create(self):
        self.scale = 30
        self.color = Color.PURPLE
        self.time = 0
        self.rotation = boss1.way*90
    def on_update(self, dt):
        self.x += 10*self.rotation/90
        self.time += dt
        if player.health < 1 or boss1.health < 1:
            self.delete()
        if self.is_touching_sprite(player):
            player.health += -1
            self.delete()
        if self.is_touching_window_edge():
            self.delete()

        


            

hp = w.create_label(Health)
bosshp = w.create_label(BossHealth, y=600)
timelabel = w.create_label(Time, y=bosshp.y*2-hp.y)
fastesttimelabel = w.create_label(FastestTime, y=timelabel.y*2-bosshp.y)
player = w.create_sprite(HollowKnight, x=200, y=300)
boss1 = w.create_sprite(PureVessel, x=800, y=100)
backgound_floor = w.create_sprite(Backgound_floor, x=500, y=-100)


w.run()