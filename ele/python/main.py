"""

Lobby buttons:
    - up, down only
    - The button is a toggle switch. When a user presses it. It is turned on.
      And the 'light' on the button is on too.
      User cannot unpress it.
      Only the computer and turn off the state of the button.
Elevator buttons:
    - tied to number of floors
    - user can only turn on the button for a floor - user cannot turn it off.
    - what about open/close elevator door button?

Computer has access to the following information:
    - lobby buttons            : read-write
    - lobby door               : read-write
    - elevator buttons         : read-write
    - elevator floor sensor    : read
    - elevator door open       : read
    - elevator door close      : read
    - elevator door obstruction: read
    - elevator door motor speed: read-write
    - elevator door motor state: read-write
    - elevator load sensor     : read
    - elevator max load        : read

Measuring performance:
    - waiting time for each user (from joining queue to exiting elevator)
    - total distances traveled by elevators
      - measure angle turned by motor and also change of direction
    - handling obstruction
    - smoothness of ride (and door?)
    - how close to lobby door

Simulating failure:
    - brakes? detection?
    - permanent doorway obstruction?
    - power failure?

"""

"""
Simulator class:
    - main method is Simulator.run(dt)
    - Simulator.run(dt) will call run on all objects in its container.
    - Simulator will handle side effects between objects. For instance if an
      elevator motor turns in a certain direction and at a certain speed, then
      the Simulator and modify the vertical position of the affected elevator
      accordingly. (Or I can 
"""

from math import cos, sin
import random; random.seed()

class Motor:
    """
    Every motor has a speed control. There is a three way switch: STOP, CLOCKWISE, ANTICLOCKWISE.
    """
    STOP = 0
    CLOCKWISE = 1
    ANTICLOCKWISE = 2
    STATES = [STOP, CLOCKWISE, ANTICLOCKWISE]
    
    def __init__(self, radius=1.0):
        self.speed = 0.0     # This is the angular speed
        self.radius = radius # Cannot be changed
        self.state = Motor.STOP

        self.angle = 0.0 # This is for drawing
        self.x = 0
        self.y = 0
        
    def get_state(self):
        return self.state
    def set_state(self, x):
        if x not in Motor.STATES:
            raise ValueError("ERROR in Motor.set_state: invalid state %s" % x)
        self.state = x

    def get_speed(self):
        return self.speed
    def set_speed(self, s):
        if s < 0:
            raise ValueError("ERROR in Motor.set_state: invalid state %s" % x)
        self.speed = s

    def get_radius(self):
        return self.radius
    def run(self, dt=0):
        """ Record energy used """
        if self.state == Motor.STOP:
            pass
        elif self.state == Motor.CLOCKWISE:
            self.angle += self.speed * dt
        elif self.state == Motor.ANTICLOCKWISE:
            self.angle -= self.speed * dt
            
    def __str__(self):
        return "<Motor id:%s, speed:%s, radius:%s, state:%s>" % (id(self), self.speed, self.radius, self.state)


class Door:
    """
    The motor of the door is setup so that
    - Motor.CLOCKWISE -> open
    - Motor.ANTICLOCKWISE -> close
    """    
    def __init__(self):
        self.motor = Motor()
        self.conversion = 1.0 # Conversion from motor angle to door open/close distance
        self.obstruction = False
        self.__gap = 0.0           # 0.0 for door fully closed, 1.0 for door fully opened
        self.log = []

    def open(self):
        return self.__gap == 1
    def close(self):
        return self.__gap == 0
    
    def get_motor_state(self):
        return self.motor.get_state()
    def set_motor_state(self, x):
        self.motor.set_state(x)
        
    def get_motor_speed(self):
        return self.motor.get_speed()
    def set_motor_speed(self, x):
        return self.motor.set_speed(x)
        
    def get_obstruction(self):
        return self.obstruction
    
    def run(self, dt=0):
        if dt == 0: return
        motor_state = self.motor.get_state()
        if motor_state == Motor.STOP:
            pass
        elif motor_state == Motor.CLOCKWISE:
            self.__gap += self.motor.get_speed() * dt * self.conversion
            if self.__gap > 1:
                self.log.append("gap > 1. Reset to 1.")
                self.__gap = 1
        elif motor_state == Motor.ANTICLOCKWISE:
            self.__gap -= self.motor.get_speed() * dt * self.conversion
            if self.__gap < 0:
                self.log.append("gap < 0. Reset to 0.")
                self.__gap = 0
    def __str__(self):
        if self.log == []:
            return """<Door id:%s, open:%s, close:%s, obstruction:%s, gap:%s
    motor:%s,
    log:None
>""" % \
               (id(self), 
                self.open(), self.close(),
                self.obstruction, self.__gap, self.motor,)
        else:
            return """<Door id:%s, open:%s, close:%s, obstruction:%s, gap:%s
    motor:%s, 
    log:
        %s
>""" % \
    (id(self), self.open(), self.close(),
     self.obstruction, self.__gap, self.motor, '\n        '.join([x for x in self.log]))

class ElevatorDoor(Door):
    def __init__(self):
        Door.__init__(self)
    def __str__(self):
        s = Door.__str__(self)
        s = s.replace("Door", "ElevatorDoor")
        return s
    
class LobbyDoor(Door):
    def __init__(self):
        Door.__init__(self)
    def __str__(self):
        s = Door.__str__(self)
        s = s.replace("Door", "LobbyDoor")
        return s

    
class ElevatorCar:
    """
    An elevator car has sensors that reads where they are. When the sensors reads 0.0, it means that the
    elevator is at floor 1. When it reads 1.0, it is at floor 2. Etc. The information of the maximum
    number of floors for an elevator is not stored here but is configured in the elevator control
    software.
    -- MORE GENERALLY: Let sensors measure distance of fixed units -- meters.
    """
    def __init__(self):
        self.door = ElevatorDoor()
        self.max_load = 1000
        self.load_sensor = 0
        self.floor_sensor = 0.0
        self.max_floor_sensor = 10.0

        self.w = 3
        self.h = 3
        self.x, self.y = 0, 0 # Bottom left 
        
    def get_load_sensor(self):
        return self.load_sensor
    def get_max_load(self):
        return self.max_load
    
    def get_floor_sensor(self):
        return self.floor_sensor
    def set_floor_sensor(self, x):
        self.floor_sensor = x
        
    def set_door_motor_state(self, x):
        door.set_motor_state(x)
    def get_door_motor_state(self):
        return door.get_motor_state()
    def get_door_motor_speed(self, x):
        return self.door.motor.get_speed()
    def set_door_motor_speed(self, x):
        return self.door.motor.set_speed(x)
    
    def get_door_obstruction(self):
        return door.obstruction()

    def __str__(self):
        s = str(self.door)
        s = '\n    '.join(s.split('\n'))
        return """<ElevatorCar id:%s, max_load:%s, load_sensor:%s, floor_sensor:%s
    door:%s
>""" % (id(self), self.max_load, self.load_sensor, self.floor_sensor, s)

    def run(self, dt):
        self.door.run(dt)

class ElevatorCarMotor(Motor):
    """
    CLOCKWISE -> up
    ANTICLOCKWISE -> down
    """
    def __init__(self):
        Motor.__init__(self)
        assert isinstance(car, ElevatorCar)
        self.car = None
        self.conversion = 1.0 # Conversion factor from angle to vertical distance
    def attach_car(self, car):
        self.car = car
    def run(self, dt=0):
        Motor.run(self, dt)
        state = self.get_state()
        speed = self.get_speed()
        car = self.car
        if self.state == Motor.STOP:
            pass
        elif self.state == Motor.CLOCKWISE:
            car.y += (self.radius * self.speed * dt)
            car.set_floor_sensor(car.y)
        elif self.state == Motor.ANTICLOCKWISE:
            car.y -= (self.radius * self.speed * dt)
            car.set_floor_sensor(car.y)
            
        # boundary checks: hardcoded for now
        if car.y < 0:
            car.y = 0
            self.state = Motor.CLOCKWISE
        if car.y > (NUM_FLOORS - 2) * CAR_HEIGHT:
            car.y = (NUM_FLOORS - 2) * CAR_HEIGHT
            self.state = Motor.ANTICLOCKWISE

    def __str__(self):
        s = Motor.__str__(self).replace("Motor", "ElevatorCarMotor")
        return s



class Building:
    """
    This is for containing the components of the simulation.
    This is important for drawing since the 
    """
    pass

    
if __name__ == '__main__':

    """
    print "Testing Door ..."
    door = Door()
    print door
    
    print
    print "set motor to CLOCKWISE"
    door.set_motor_state(Motor.CLOCKWISE)
    door.set_motor_speed(0.1)
    door.run(1)
    print door
    door.run(1)
    print door
    door.run(1)
    print door
    
    print
    print "set motor to ANTICLOCKWISE"
    door.set_motor_state(Motor.ANTICLOCKWISE)
    door.run(1)
    print door
    door.run(1)
    print door

    print
    car = ElevatorCar()
    print car

    print
    emotor = ElevatorCarMotor(car)
    emotor.set_speed(0.1)
    print emotor
    print car
    
    emotor.set_state(Motor.CLOCKWISE)
    emotor.run(1)
    car.run(1)
    print emotor
    print car
    
    emotor.run(1)
    car.run(1)
    print emotor
    print car 
    """
    
    # Conversion factor for draw:
    SCALE = 10 # real scale, i.e., for 3m tall elevator, length used for drawing is 30 pixels

    def draw_elevator(surface, car):
        floor_sensor = car.get_floor_sensor()
        h = car.h * SCALE
        w = car.w * SCALE
        x, y = car.x * SCALE, HEIGHT - car.y *SCALE - car.h * SCALE
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(surface, (255,255,255), rect, 1)

    def draw_elevator_motor(surface, emotor):
        r = emotor.radius * SCALE
        t = emotor.angle
        x = emotor.x * SCALE
        y = HEIGHT - emotor.y * SCALE
        pygame.draw.circle(surface, (255,255,255), (int(x),int(y)), int(r), 1)
        x0, y0 = x + r * cos(t), y + r * sin(t)
        pygame.draw.line(surface, (255,255,255), (int(x),int(y)), (int(x0),int(y0)), 1)
        
    def draw_elevator_cable(surface, emotor, car):
        mr = emotor.radius * SCALE
        mt = emotor.angle * SCALE
        mx = emotor.x * SCALE
        my = HEIGHT - emotor.y * SCALE
        mx = mx - mr
        # cable attach is point is (mx, my)
        
        ch = car.h * SCALE
        cw = car.w * SCALE
        cx, cy = car.x * SCALE, HEIGHT - car.y * SCALE - car.h * SCALE
        cx = cx + cw/2.0
        # cable attach point is (cx,cy)
        
        pygame.draw.line(surface, (255,0,0), (int(mx),int(my)), (int(cx),int(cy)), 1)
        
        
    class Elevator:
        def __init__(self):
            self.car = ElevatorCar()
            self.emotor = ElevatorCarMotor(self.car)

    # Set drawing surface to 680x480
    WIDTH = 700
    HEIGHT = 640
    SIZE = (WIDTH, HEIGHT)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    
    N = 5             # number of elevators
    SHAFT_WIDTH = 5.0
    SHAFT_HEIGHT = 64.0
    CAR_WIDTH = 3.0
    CAR_HEIGHT = 3.0
    NUM_FLOORS = 20

    EMOTOR_RADIUS = 1.0
    EMOTOR_HEIGHT = (NUM_FLOORS) * CAR_HEIGHT # should depend on number of floors

    # Initialize Pygame
    import pygame, sys
    pygame.init()
    surface = pygame.display.set_mode(SIZE)
    
    cars = []
    emotors = []

    for i in range(N):    
        car = ElevatorCar()
        car.x = 1 + i * SHAFT_WIDTH      # 1m from left side to allow for
                                         # shaft
        car.y = random.randrange(0, 50)  # init elevator to random heights
        car.w = CAR_WIDTH                # 3m wide
        car.h = CAR_HEIGHT               # 3m wide
        
        emotor = ElevatorCarMotor()
        emotor.set_speed(0.02)
        emotor.set_state(Motor.CLOCKWISE)
        emotor.radius = EMOTOR_RADIUS
        emotor.x = car.x + emotor.radius + car.w / 2.0
        emotor.y = EMOTOR_HEIGHT
        emotor.attach_car(car)

        cars.append(car)
        emotors.append(emotor)
        
    while 1:
        
        # Exit if window is closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        dt = 1.0 # in seconds

        for i in range(N):
            emotors[i].run(dt) # motor is attached to car, this will modify
                               # car.y and car.floor_sensor
            cars[i].run(dt)

        # Draw surface
        surface.fill(BLACK)
        
        for i in range(N):
            draw_elevator_cable(surface, emotors[i], cars[i])
            draw_elevator(surface, emotors[i].car)
            draw_elevator_motor(surface, emotors[i])

        # draw elevator shaft
        for i in range(N):
            rect = pygame.Rect(SCALE * (cars[i].x - 1), # -1 for width
                               HEIGHT - (NUM_FLOORS * CAR_HEIGHT)*SCALE,
                               SCALE * (cars[i].w + 2),
                               SCALE * SHAFT_HEIGHT)
            pygame.draw.rect(surface, WHITE, rect, 2)

        # draw floors
        for y in range(0, NUM_FLOORS):
            rect = pygame.Rect(SCALE * ((N)* SHAFT_WIDTH),
                               HEIGHT - CAR_HEIGHT * y * SCALE,
                               32 * SCALE,
                               CAR_HEIGHT * SCALE)
            pygame.draw.rect(surface, WHITE, rect, 2)
            
        pygame.display.flip()
