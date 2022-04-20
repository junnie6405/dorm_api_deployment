#Pledge: “I have neither given nor received unauthorized aid on this program.”

from collections import defaultdict
import math
import sys
import heapq

class State:

    def __init__(self, parent=None, location=None):
        self.parent = None
        self.location = None
        self.road_name = None
        self.speed_limit = None
        self.time_taken = None
        self.dist = None

        self.g_cost = 0
        self.h_cost = 0
        self.f_cost = 0

def distance_on_unit_sphere(lat1, long1, lat2, long2):

    degrees_to_radians = math.pi/180.0

    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians

    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians

    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
    math.cos(phi1)*math.cos(phi2))
    arc = math.acos(cos)

    return arc * 3960

def getBearing(lat1, long1, lat2, long2):

    lat1 *= math.pi / 180
    lat2 *= math.pi / 180
    long1 *= math.pi / 180
    long2 *= math.pi / 180

    y = math.sin(long2 - long1) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(long2 - long1)
    angle = math.atan2(y, x)
    bearing = (angle * 180 / math.pi + 360) % 360

    return bearing

def text_reading(text_file):

    try:
        file = open(text_file)
        locations = defaultdict(list)
        roads = defaultdict(list)

        for line in file:

            info = line.split("|")
            info[-1] = info[-1].strip() #removing the newline character

            if info[0] == "location":
                vertex, lat, long = info[1], info[2], info[3]
                locations[vertex] = [lat, long]

            else: #meaning this line stores info regarding road
                point_a, point_b, speed, road = info[1], info[2], info[3], info[4]

                lat1, long1 = float(locations[point_a][0]), float(locations[point_a][1])
                lat2, long2 = float(locations[point_b][0]), float(locations[point_b][1])

                dist = distance_on_unit_sphere(lat1, long1, lat2, long2)
                dist_per_sec = int(speed) / 3600
                time = str(dist / dist_per_sec)

                roads[point_a].append([point_b, speed, road, time, dist])
                roads[point_b].append([point_a, speed, road, time, dist])

        return locations, roads

    except FileNotFoundError:
        print("This text file does not exist or is typed incorrectly.Try Again.")
        # Could end the program. But ask the user to type the text file again.
        file_name = input("Enter the name of the text file. Can't find the file? Type Enter to end.")
        if not file_name:
            sys.exit("no file.")
        text_reading(file_name)

def path_print(initial_state, goal_state):
    route = []
    curr = goal_state
    road_names = []
    node_list = []

    while curr:
        route.append(curr.location)
        road_names.append(curr.road_name)
        node_list.append(curr)
        curr = curr.parent

    return route[::-1], road_names[::-1], node_list[::-1]

def route_printing(path, roads):
    print("Route found is:")
    for i in range(len(path)):
        print('{} ({})'.format(path[i], roads[i]))
    print("")

def calculate_direction(angle):
    dir = ""

    if (angle >= 0 and angle < 22.5) or (angle >= 337.5 and angle <= 360):
        dir = "North"
    elif angle >= 22.5 and angle < 67.5:
        dir = "NorthEast"
    elif angle >= 67.5 and angle < 112.5:
        dir = "East"
    elif angle >= 112.5 and angle < 157.5:
        dir = "SouthEast"
    elif angle >= 157.5 and angle < 202.5:
        dir = "South"
    elif angle >= 202.5 and angle < 247.5:
        dir = "SouthWest"
    elif angle >= 247.5 and angle < 292.5:
        dir = "West"
    else:
        dir = "NorthWest"

    return dir

def calculate_time_distance(node_list, index):
    time = node_list[index].time_taken
    dist = node_list[index].dist

    return time, dist

def calculate_turn(bearing1, bearing2):

    if bearing1 > bearing2:
        if bearing1 - bearing2 < 180:
            left = True
        else:
            left = False
    else:
        if bearing2 - bearing1 < 180:
            left = False
        else:
            left = True

    return "left" if left else "right"

def gps_direction(location, roads, l_map, node_list):

    print("GPS directions:")

    accumulated_dist = 0
    accumulated_time = 0

    for i in range(1, len(roads)):
        prev_loc, cur_loc = location[i - 1], location[i]
        prev_road, cur_road = roads[i - 1], roads[i]

        time, dist = calculate_time_distance(node_list, i)
        lat1, long1 = float(l_map[prev_loc][0]), float(l_map[prev_loc][1])
        lat2, long2 = float(l_map[cur_loc][0]), float(l_map[cur_loc][1])

        if i == 1:  # initial turn

            new_bearing = getBearing(lat1, long1, lat2, long2)
            direction = calculate_direction(new_bearing)

            accumulated_dist += dist
            accumulated_time += time

            print("Head {} on {}".format(direction, roads[1]))

        else:

            if prev_road != cur_road: #meaning there must be a turn

                old_bearing = new_bearing
                new_bearing = getBearing(lat1, long1, lat2, long2)

                turn = calculate_turn(old_bearing, new_bearing)

                accumulated_dist = round(accumulated_dist, 2)
                accumulated_time = round(accumulated_time, 2)

                print("   Drive for {} miles ({} seconds)".format(str(accumulated_dist), str(accumulated_time)))

                accumulated_time = time # reset the accumulated time and distance
                accumulated_dist = dist

                print("Turn {} onto {}".format(turn, roads[i]))

            else:
                accumulated_time += time
                accumulated_dist += dist

    accumulated_dist = round(accumulated_dist, 2)
    accumulated_time = round(accumulated_time, 2)

    print("   Drive for {} miles ({} seconds)".format(str(accumulated_dist), str(accumulated_time)))
    print("You have arrived!")

def calculate_h_cost(lat1, long1, lat2, long2):
    dist = distance_on_unit_sphere(float(lat1), float(long1), float(lat2), float(long2))
    dist_per_sec = 65 / 3600
    cost = dist / dist_per_sec
    return cost

def debugging_print(cur_state, visit, skip):

    state = cur_state.location
    parent = cur_state.parent

    if not parent:
        parent_name = "None"
    else:
        parent_name = parent.location

    g = cur_state.g_cost
    h = cur_state.h_cost
    f = cur_state.f_cost

    if visit:
        print("Visiting ", end='')
    elif skip:
        print("     Skipping ", end='')
    else:
        print("     Adding ", end='')

    print("[State={}, parent={}, g={}, h={}, f={}]".format(state, parent_name, g, h, f))

def a_star(initial, goal, locations, roads, debug):
    start = State()
    start.location = initial
    start.road_name = "starting location"

    start_lat, start_long = locations[initial][0], locations[initial][1]
    end_lat, end_long = locations[goal][0], locations[goal][1]

    start.g_cost = 0
    start.h_cost = calculate_h_cost(start_lat, start_long, end_lat, end_long)
    start.f_cost = start.g_cost + start.h_cost

    frontier = []
    reached = defaultdict(float)
    reached[start.location] = start.f_cost

    heapq.heappush(frontier, (start.f_cost, start))
    count = 0  # counting the number of nodes visited.

    while frontier:
        cur_f, cur_state = heapq.heappop(frontier)
        count += 1

        if debug == 'y':
            debugging_print(cur_state, True, False)

        cur_location = cur_state.location

        if cur_location == goal:
            print("Total travel time in seconds: ", cur_state.f_cost)
            print("Number of nodes visited: ", count)
            print("")
            return path_print(initial, cur_state)

        child_list = [] # child_node collecion list

        for edge in roads[cur_location]:
            child_loc, speed, road_name, time, dist = edge[0], edge[1], edge[2], edge[3], edge[4]
            child_state = State()

            #initialize the child_state's info.
            child_state.location = child_loc
            child_state.road_name = road_name
            child_state.speed_limit = int(speed)
            child_state.time_taken = float(time)
            child_state.dist = float(dist)
            child_state.parent = cur_state
            child_state.g_cost = cur_state.g_cost + float(time)

            #calculate h cost

            child_lat, child_long = locations[child_loc][0], locations[child_loc][1]
            child_state.h_cost = calculate_h_cost(child_lat, child_long, end_lat, end_long)
            child_state.f_cost = child_state.g_cost + child_state.h_cost

            child_list.append(child_state)

        for child in child_list:

            skip = True # boolean variable needed for debugging information

            if child.location not in reached or child.f_cost < reached[child.location]:
                skip = False
                reached[child.location] = child.f_cost
                heapq.heappush(frontier, (child.f_cost, child))

            if debug == 'y':
                debugging_print(child, False, skip)
                
def main():
    file_name = input("Enter the name of the text file ")
    locations, roads = text_reading(file_name)

    start_loc = input("Enter a starting location ID: ")
    if start_loc not in locations:
        print("The inital state does not exist.")
        return
    end_loc = input("Enter ending location ID: ")
    if end_loc not in locations:
        print("The goal state does not exist.")
        return
    debugging = input("Do you want debugging information? (y/n)? ")

    path, road_names, node_list = a_star(start_loc, end_loc, locations, roads, debugging)

    route_printing(path, road_names)

    gps_direction(path, road_names, locations, node_list)

if __name__ == "__main__":
    main()
