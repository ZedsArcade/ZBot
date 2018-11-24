import math
import array

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
from roles import *


class ZBot(BaseAgent):

    team_members = [None] * 3

    def initialize_agent(self):
        #This runs once before the bot starts up
        self.controller_state = SimpleControllerState()
        #Need to initialise role and team on roles.py file hehe
        

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        ball_location = Vector2(packet.game_ball.physics.location.x, packet.game_ball.physics.location.y)

        my_car = packet.game_cars[self.index]
        car_location = Vector2(my_car.physics.location.x, my_car.physics.location.y)
        car_direction = get_car_facing_vector(my_car)
        car_to_ball = ball_location - car_location

        steer_correction_radians = car_direction.correction_to(car_to_ball)

        if steer_correction_radians > 0:
            # Positive radians in the unit circle is a turn to the left.
            turn = -1.0  # Negative value for a turn to the left.
        else:
            turn = 1.0

        self.controller_state.throttle = 1.0
        self.controller_state.steer = turn
        self.controller_state.boost = True
        
        print("Role is " + str(car_role[self.index]))
        get_team(self, packet)
        
        print("I am " + str(self.index) + " and my team members are: " + str(self.team_members[0]) + ' ' + str(self.team_members[1]) + ' ' + str(self.team_members[2]))
        return self.controller_state


class Vector2:
    def __init__(self, x=0, y=0):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, val):
        return Vector2(self.x + val.x, self.y + val.y)

    def __sub__(self, val):
        return Vector2(self.x - val.x, self.y - val.y)

    def correction_to(self, ideal):
        # The in-game axes are left handed, so use -x
        current_in_radians = math.atan2(self.y, -self.x)
        ideal_in_radians = math.atan2(ideal.y, -ideal.x)

        correction = ideal_in_radians - current_in_radians

        # Make sure we go the 'short way'
        if abs(correction) > math.pi:
            if correction < 0:
                correction += 2 * math.pi
            else:
                correction -= 2 * math.pi

        return correction


def get_car_facing_vector(car):
    pitch = float(car.physics.rotation.pitch)
    yaw = float(car.physics.rotation.yaw)

    facing_x = math.cos(pitch) * math.cos(yaw)
    facing_y = math.cos(pitch) * math.sin(yaw)

    return Vector2(facing_x, facing_y)

def assign_role(self):
    if car_role[self.index] == 1:
        # Since you have just started, check who should be what to start off

        # Who is closest to the ball
        # Closest becomes attacker
        # Further becomes defender
        # Mid becomes Roamer
        # If there is a tie check role of other tied car
        
        print("Role is now " + str(car_role[self.index]))
    return car_role[self.index]

def get_team(self, packet: GameTickPacket) -> SimpleControllerState:
    
    j = 0
    i = 0
    for vehicles in packet.game_cars:
        #print("value one is " + str(vehicles.team))
        #print("value two is " + str(packet.game_cars[self.index].team))
        if i < 3:
            if vehicles.team == packet.game_cars[self.index].team:
                #print("This is true")
                #print("value im trying to add next is " + str(j))
                self.team_members[i] = j
                i = i + 1
            j = j + 1
        



    

        

#def distance_to_ball(car):

#    return 