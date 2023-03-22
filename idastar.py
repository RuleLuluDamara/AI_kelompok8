import math

def city_distance(city1, city2):
    x1, y1 = city_coordinates[city1]
    x2, y2 = city_coordinates[city2]
    distance = math.sqrt((x1 - x2)*2 + (y1 - y2)*2)
    # print("distance between ", city1, " to ", city2, " is ", distance)
    return distance

def iterative_deepening_a_star(start_city, goal_city):
    bound = city_distance(start_city, goal_city)
    rute = [start_city]
    while True:
        # print("rute: ", rute)
        result, new_bound = search(rute, 0, bound, goal_city)
        print("============result new bound ", result, " ", new_bound)
        if result == 'found':
            return rute
        if new_bound == float('inf'):
            return None
        bound = new_bound


def search(rute, g, bound, goal_city):
    city = rute[-1]
    # print("city bro: ", city)
    f = g + city_distance(city, goal_city)
    # print("estimate from ", city, " to ", goal_city, " is ", f)
    if f > bound:
        # print("returnnnnnnnnnnn karena f lebih besar dari bound\n")
        return 'fail', f
    if city == goal_city:
        return 'found', f
    min_cost = float('inf')
    print("min_const ", min_cost)
    for neighbor, cost in graph_heuristic[city].items():
        # print("neighbor cost ", neighbor, cost)
        if neighbor not in rute:
            rute.append(neighbor)
            print("rute ", rute)
            result, new_cost = search(rute, g + cost, bound, goal_city)
            if result == 'found':
                # print("FOUNDDDDDDDDD")
                return 'found', new_cost
            if new_cost < min_cost:
                print("update min_cosst ", new_cost)
                min_cost = new_cost
            rute.pop()
        else :
            print("ada di rute")
    return 'fail', min_cost

city_index = {
  1: 'Arad',
  2: 'Bucharest',
  3: 'Craiova',
  4: 'Drobeta',
  5: 'Eforie',
  6: 'Fagaras',
  7: 'Giurgiu',
  8: 'Hirsova',
  9: 'Iasi',
  10: 'Lugoj',
  11: 'Mehadia',
  12: 'Neamt',
  13: 'Oradea',
  14: 'Pitesti',
  15: 'Rimnicu Vilcea',
  16: 'Sibiu',
  17: 'Timisoara',
  18: 'Urziceni',
  19: 'Vaslui',
  20: 'Zerind'
 }


city_coordinates = {
    'Arad': (91, 492),
    'Bucharest': (400, 327),
    'Craiova': (253, 288),
    'Drobeta': (165, 299),
    'Eforie': (562, 293),
    'Fagaras': (305, 449),
    'Giurgiu': (375, 270),
    'Hirsova': (534, 350),
    'Iasi': (473, 506),
    'Lugoj': (165, 379),
    'Mehadia': (168, 339),
    'Neamt': (406, 537),
    'Oradea': (131, 571),
    'Pitesti': (320, 368),
    'Rimnicu Vilcea': (233, 410),
    'Sibiu': (207, 457),
    'Timisoara': (94, 410),
    'Urziceni': (456, 350),
    'Vaslui': (509, 444),
    'Zerind': (108, 531)
}

graph_heuristic = {
    'Arad': {'Zerind': 75, 'Timisoara': 118, 'Sibiu': 140},
    'Zerind': {'Oradea': 71, 'Arad': 75},
    'Oradea': {'Zerind': 71, 'Sibiu': 151},
    'Timisoara': {'Arad': 118, 'Lugoj': 111},
    'Lugoj': {'Timisoara': 111, 'Mehadia': 70},
    'Mehadia': {'Lugoj': 70, 'Drobeta': 75},
    'Drobeta': {'Mehadia': 75, 'Craiova': 120},
    'Sibiu': {'Arad': 140, 'Oradea': 151, 'Fagaras': 99, 'Rimnicu Vilcea': 80},
    'Fagaras': {'Sibiu': 99, 'Bucharest': 211},
    'Rimnicu Vilcea': {'Sibiu': 80, 'Craiova': 146, 'Pitesti': 97},
    'Craiova': {'Drobeta': 120, 'Rimnicu Vilcea': 146, 'Pitesti': 138},
    'Pitesti': {'Rimnicu Vilcea': 97, 'Craiova': 138, 'Bucharest': 101},
    'Bucharest': {'Fagaras': 211, 'Pitesti': 101, 'Giurgiu': 90, 'Urziceni': 85},
    'Giurgiu': {'Bucharest': 90},
    'Urziceni': {'Bucharest': 85, 'Hirsova': 98, 'Vaslui': 142},
    'Hirsova': {'Urziceni': 98, 'Eforie': 86},
    'Eforie': {'Hirsova': 86},
    'Vaslui': {'Urziceni': 142, 'Iasi': 92},
    'Iasi': {'Vaslui': 92, 'Neamt': 87},
    'Neamt': {'Iasi': 87}
}



def input_user():    
  print("======LIST OF CITY(S)===========")
  for i in range(1, len(city_index)):
      print(i, city_index[i])
  start_city_index = int(input("start city: "))
  goal_city_index = int(input("goal city: "))
  start_city = city_index[start_city_index]
  goal_city = city_index[goal_city_index]
  rute = iterative_deepening_a_star(start_city, goal_city)
  if rute is None:
      print(f"Tidak ditemukan jalur dari {start_city} ke {goal_city}.")
  else:
      print(f"Jalur terpendek dari {start_city} ke {goal_city} adalah:")
      print(' -> '.join(rute))
  
if __name__ == "__main__":
    input_user()