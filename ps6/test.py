# Problem Set 6: Simulating robots
# Name:
# Collaborators:
# Time:

import math
import random

import ps6_visualize
import pylab

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

# === Problems 1

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.tiles = {}
        for x in range(self.width):
            for y in range(self.height):
                tile = (x,y)
                self.tiles[tile] = 0
        
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        x = int(pos.getX())
        y = int(pos.getY())
        tile = (x,y)
        self.tiles[tile]=1
    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        if self.tiles[(m,n)]==1:
            return True
        else:
            return False
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width*self.height

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        clean_tiles = 0
        for x in self.tiles:
            if self.tiles[x] == 1:
                clean_tiles +=1
        return clean_tiles

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        x = round(random.random()*self.width,1)
        y = round(random.random()*self.height,1)
        pos = Position(x,y)
        return pos

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        x = pos.getX()
        y = pos.getY()
        if x <= self.width and x >= 0 and y <= self.height and y >= 0:
            return True
        else:
            return False


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.direction = random.randint(0,360)
        self.position = self.room.getRandomPosition()
        self.room.cleanTileAtPosition(self.position)

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError


# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        temp_position = self.position.getNewPosition(self.direction, self.speed)
        if self.room.isPositionInRoom(temp_position):
            self.setRobotPosition(temp_position)
            self.room.cleanTileAtPosition(temp_position)
        else:
            self.setRobotDirection(random.randint(0,360))

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials, robot_type):
    anim = ps6_visualize.RobotVisualization(num_robots,width,height)
    time_steps = 0
    for x in range(num_trials):
        time_step = 0
        room = RectangularRoom(width,height)
        robots = []
        min_tiles = int(room.getNumTiles()*min_coverage)
        for y in range(num_robots):
            robot = robot_type(room, speed)
            robots.append(robot)
        while room.getNumCleanedTiles()< min_tiles:
            anim.update(room, robots)
            for w in robots:
                w.updatePositionAndClean()
            time_step+=1
        time_steps += time_step
        anim.done()
    return time_steps/num_trials  

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    x_axis = []
    y_axis = []
    for x in range(1,11):
        y = runSimulation(x,1.0,20,20,.8,10,StandardRobot)
        x_axis.append(x)
        y_axis.append(y)
    pylab.plot(x_axis,y_axis,'bo')
    pylab.xlabel('Roombas')
    pylab.ylabel('Time/Steps')
    pylab.title('Time to clean 80% of a 20x20 room with each of 1-10 roombas')
    pylab.show()
def showPlot2():
    room_size = [(20,20),(25,16),(40,10),(50,8),(80,5),(100,4)]
    y_axis = []
    x_axis=[]
    for x in room_size:
        y = runSimulation(2,1.0,x[0],x[1],.8,10,StandardRobot)
        y_axis.append(y)
        x_axis.append(x[0])
    pylab.plot(x_axis,y_axis,'bo')
    pylab.xlabel('Room Width')
    pylab.ylabel('Time/Steps')
    pylab.title('Time to clean 80% of a square room with 2 robots, for various room sizes')
    pylab.show()
class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        self.setRobotDirection(random.randint(0,360))
        temp_position = self.position.getNewPosition(self.direction, self.speed)
        if self.room.isPositionInRoom(temp_position):
            self.setRobotPosition(temp_position)
            self.room.cleanTileAtPosition(temp_position)
        else:
            self.setRobotDirection(random.randint(0,360))
