import numpy as np
import heapq

def heuristic(a, b): # Annan h funktion för icke diagonal stig
    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

# https://www.analytics-link.com/post/2018/09/14/applying-the-a-path-finding-algorithm-in-python-part-1-2d-square-grid
def astar(array, start, goal):
    # neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)] # Diagonalt!
    neighbors = [(0,1),(0,-1),(1,0),(-1,0)]

    close_set = set()
    came_from = {}
    gscore = {start:0}
    fscore = {start:heuristic(start, goal)}
    oheap = []
    heapq.heappush(oheap, (fscore[start], start))
    
    while oheap:
        current = heapq.heappop(oheap)[1]
        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j            
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:                
                    if array[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue
            if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))

def koordTillCell(x, y):
    pass

def stigTillKoords(stig, bins, x_edges, y_edges): # TODO Gör så funktionen gör det den faktiskt ska göra smh
    '''
    Mappa stegen till olika kooridnater i koordinatsystemet.  
    '''
    max_x, min_x = max(x_edges), min(x_edges)
    max_y, min_y = max(y_edges), min(y_edges)
    print('max_x:', max_x)
    print('min_x:', min_x)
    print('max_y:', max_y)
    print('min_y:', min_y)
    
    x_koords = [steg[0] for steg in stig]
    y_koords = [steg[1] for steg in stig]

    d_x = (max_x - min_x) / bins
    d_y = (max_y - min_y) / bins
    print('varje x-ruta(cm): ', d_x)
    print('varje y-ruta(cm): ', d_y)

    return x_koords, y_koords