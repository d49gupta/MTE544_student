# Type of planner
import numpy as np
POINT_PLANNER = 0; TRAJECTORY_PLANNER = 1
PARABOLA = 0; SIGMOID = 1


class planner:
    def __init__(self, type_):

        self.type=type_

    
    def plan(self, goalPoint=[-1.0, -1.0]):
        
        if self.type==POINT_PLANNER:
            return self.point_planner(goalPoint)
        
        elif self.type==TRAJECTORY_PLANNER:
            return self.trajectory_planner(goalPoint)


    def point_planner(self, goalPoint):
        x = goalPoint[0]
        y = goalPoint[1]
        return x, y

    # TODO Part 6: Implement the trajectories here
    def trajectory_planner(self, pathType):
        # the return should be a list of trajectory points: [ [x1,y1], ..., [xn,yn]]
        # return
        trajectory = []

        # use equation for parabola and sigmoid to generate points
        if pathType == PARABOLA:
            for x in np.arange(0, 1.5, 0.01):
                y = x * x
                trajectory.append([x, y])
        elif pathType == SIGMOID:
            for x in np.arange(0, 2.5, 0.01):
                y = 2 / (1 + np.exp(-2*x)) - 1
                trajectory.append([x, y])

        return trajectory