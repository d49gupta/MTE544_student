from math import atan2, asin, sqrt, remainder
import re

M_PI=3.1415926535

class Logger:
    
    def __init__(self, filename, headers=["e", "e_dot", "e_int", "stamp"]):
        
        self.filename = filename

        with open(self.filename, 'w') as file:
            
            header_str=""

            for header in headers:
                header_str+=header
                header_str+=", "
            
            header_str+="\n"
            
            file.write(header_str)


    def log_values(self, values_list):

        with open(self.filename, 'a') as file:
            
            vals_str=""
            
            for value in values_list:
                vals_str+=f"{value}, "
            
            vals_str+="\n"
            
            file.write(vals_str)
            

    def save_log(self):
        pass

class FileReader:
    def __init__(self, filename):
        self.filename = filename

    def read_file(self):
        headers = []
        table = []
        read_headers = False

        time_pattern = re.compile(r"sec=(\d+),\s*nanosec=(\d+)")

        with open(self.filename, 'r') as file:
            for line in file:
                # skip empty or whitespace-only lines
                if not line.strip():
                    continue

                values = [v.strip() for v in line.strip().split(',') if v.strip()]

                # Header
                if not read_headers:
                    headers = values
                    read_headers = True
                    continue

                row = []
                skip_next = False
                for i, val in enumerate(values):
                    if skip_next:
                        skip_next = False
                        continue

                    # handle time fields that may be split into 2 columns
                    if "builtin_interfaces.msg.Time" in val:
                        # join with next part if it exists
                        if i + 1 < len(values) and "nanosec" in values[i + 1]:
                            val = val + ", " + values[i + 1]
                            skip_next = True

                        match = time_pattern.search(val)
                        if match:
                            sec = int(match.group(1))
                            nsec = int(match.group(2))
                            row.append(sec + nsec * 1e-9)
                        else:
                            row.append(0.0)
                    else:
                        # Normal numeric value
                        try:
                            row.append(float(val))
                        except ValueError:
                            row.append(0.0)

                if row:
                    table.append(row)

        return headers, table

    
    


# TODO Part 3: Implement the conversion from Quaternion to Euler Angles
def euler_from_quaternion(quat):
    """
    Convert quaternion (w in last place) to euler roll, pitch, yaw.
    quat = [x, y, z, w]
    """

    # just unpack yaw
    yaw = atan2(2 * (quat.w * quat.z + quat.x * quat.y), 1 - 2 * (quat.y**2 + quat.z**2))
    return yaw


#TODO Part 4: Implement the calculation of the linear error
def calculate_linear_error(current_pose, goal_pose):
        
    # Compute the linear error in x and y
    # Remember that current_pose = [x,y, theta, time stamp] and goal_pose = [x,y]
    # Remember to use the Euclidean distance to calculate the error.
    x_curr, y_curr = current_pose[0], current_pose[1]
    x_goal, y_goal = goal_pose[0], goal_pose[1]

    error_linear = sqrt((x_goal - x_curr)**2 + (y_goal - y_curr)**2)
    return error_linear

#TODO Part 4: Implement the calculation of the angular error
def calculate_angular_error(current_pose, goal_pose):

    # Compute the linear error in x and y
    # Remember that current_pose = [x,y, theta, time stamp] and goal_pose = [x,y]
    # Use atan2 to find the desired orientation
    # Remember that this function returns the difference in orientation between where the robot currently faces and where it should face to reach the goal
    x_goal, y_goal = goal_pose[0], goal_pose[1]
    x_curr, y_curr, theta_curr = current_pose[0], current_pose[1], current_pose[2]
    theta_goal = atan2(y_goal - y_curr, x_goal - x_curr)

    # Remember to handle the cases where the angular error might exceed the range [-π, π]
    error_angular = theta_goal - theta_curr
    error_angular = remainder(error_angular, 2 * M_PI)
    
    return error_angular
