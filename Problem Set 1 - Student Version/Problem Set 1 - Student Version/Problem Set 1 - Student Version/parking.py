from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point
from helpers.utils import NotImplemented

#TODO: (Optional) Instead of Any, you can define a type for the parking state
ParkingState = Any

# An action of the parking problem is a tuple containing an index 'i' and a direction 'd' where car 'i' should move in the direction 'd'.
ParkingAction = Tuple[int, Direction]

# This is the implementation of the parking problem
class ParkingProblem(Problem[ParkingState, ParkingAction]):
    passages: Set[Point]    # A set of points which indicate where a car can be (in other words, every position except walls).
    cars: Tuple[Point]      # A tuple of points where state[i] is the position of car 'i'. 
    slots: Dict[Point, int] # A dictionary which indicate the index of the parking slot (if it is 'i' then it is the lot of car 'i') for every position.
                            # if a position does not contain a parking slot, it will not be in this dictionary.
    width: int              # The width of the parking lot.
    height: int             # The height of the parking lot.

    # This function should return the initial state
    def get_initial_state(self) -> ParkingState:
        # ==> Returns the initial state of the parking problem, which is represented by the positions of the cars.
        return self.cars 
    
    # This function should return True if the given state is a goal. Otherwise, it should return False.
    def is_goal(self, state: ParkingState) -> bool:

        # ==> For each car in the given state, we check if it is in a parking slot
        for car_index, car_position in enumerate(state):
            # ==> Checks if the car is in a parking slot
            if car_position in self.slots:
                # ==> Checks if the car is in its corresponding parking slot
                if self.slots[car_position] != car_index: 
                    return False
            else: 
                # ==> If the car is not in a parking slot, then the state is not a goal state
                return False

        # ==> If all cars are in their corresponding parking slots, then the state is a goal state
        return True
    
    # This function returns a list of all the possible actions that can be applied to the given state
    def get_actions(self, state: ParkingState) -> List[ParkingAction]:

        actions : list = []

        # ==> For each car in the given state, we check if it can move in any direction
        for car_index, car_position in enumerate(state):
            # ==> For each direction, we check if the car can move in that direction
            for direction in Direction:
                new_car_position = car_position + direction.to_vector()
                # ==> If the car is in its corresponding parking slot, then it cannot move
                if new_car_position in state: continue 
                # ==> If the car is not in a passage, then it cannot move
                if new_car_position not in self.passages: continue 
                # ==> If the car can move in that direction, then we add the action to the list of actions
                actions.append((car_index, direction))

        # ==> Returns the list of actions
        return actions

    
    # This function returns a new state which is the result of applying the given action to the given state
    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:
        direction : Direction = action[1] 
        new_state : list = list(state) 

        # ==> Returns the new state after applying the given action
        new_state[action[0]] = state[action[0]] + direction.to_vector() 

        # ==> Returns the new state as a tuple
        return tuple(new_state) 
    
    # This function returns the cost of applying the given action to the given state
    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:
        direction: Direction = action[1]
        
        # ==> the new position of the car after applying the given action
        new_car_position: Point = state[action[0]] + direction.to_vector()

        # ==> The action cost depends on the rank of the employee whose car is moved by the action. 
        # ==> The rank is A will cost 26 till Z whose action costs 1. 
        # ==> if any action moves a car into another employee's parking slot, the action cost goes up by 100.                 

        if new_car_position in self.slots:  
            # ==> If the car is not in its corresponding parking slot, then the action cost is 100 + 26 - action[0] , action[0] = 0 for A, 1 for B, etc.
            if self.slots[new_car_position] != action[0]: 
                return 100 + 26 - action[0]

        # ==> If the car is in its corresponding parking slot, then the action cost is 26 - action[0] , action[0] = 0 for A, 1 for B, etc.
        return 26 - action[0]
        
     # Read a parking problem from text containing a grid of tiles
    @staticmethod
    def from_text(text: str) -> 'ParkingProblem':
        passages =  set()
        cars, slots = {}, {}
        lines = [line for line in (line.strip() for line in text.splitlines()) if line]
        width, height = max(len(line) for line in lines), len(lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != "#":
                    passages.add(Point(x, y))
                    if char == '.':
                        pass
                    elif char in "ABCDEFGHIJ":
                        cars[ord(char) - ord('A')] = Point(x, y)
                    elif char in "0123456789":
                        slots[int(char)] = Point(x, y)
        problem = ParkingProblem()
        problem.passages = passages
        problem.cars = tuple(cars[i] for i in range(len(cars)))
        problem.slots = {position:index for index, position in slots.items()}
        problem.width = width
        problem.height = height
        return problem

    # Read a parking problem from file containing a grid of tiles
    @staticmethod
    def from_file(path: str) -> 'ParkingProblem':
        with open(path, 'r') as f:
            return ParkingProblem.from_text(f.read())
    
