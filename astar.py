
class Node:


    def __init__(self, parent=None, position=None):

        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self,other):
        return self.position == other.position


class Astar():

    def __init__(self):
        self.visited = []


    def search(self,maze,cost,start,end):
        start_node = Node(None, tuple(start))
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, tuple(end))
        end_node.g = end_node.h = end_node.f = 0

        yet_to_visit_list = []
        visited_list = []

        yet_to_visit_list.append(start_node)

        outer_iterations = 0
        max_iterations = (len(maze) // 2) ** 10

        move  =  [[-1, 0 ], # go up
                 [ 0, -1], # go left
                 [ 1, 0 ], # go down
                 [ 0, 1 ]] # go right
        no_rows = len(maze)
        no_columns = len(maze[0])

        while len(yet_to_visit_list) > 0:
            outer_iterations += 1
            current_node = yet_to_visit_list[0]
            current_index = 0

            for index, item in enumerate(yet_to_visit_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            if outer_iterations > max_iterations:
                print ("giving up on pathfinding too many iterations")
                return self.return_path(self.visited,current_node,maze)
            
            yet_to_visit_list.pop(current_index)
            visited_list.append(current_node)

            if current_node == end_node:
                return self.return_path(self.visited,current_node,maze)

            children = []

            for new_position in move:
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                if (node_position[0] > (no_rows - 1) or
                    node_position[0] < 0 or
                    node_position[1] > (no_columns -1) or 
                    node_position[1] < 0):
                    continue

                if maze[node_position[0]][node_position[1]] != 0:
                    continue

                new_node = Node(current_node, node_position)

                children.append(new_node)
                self.visited.append(new_node) #use this to animate

            for child in children:
                if len([visited_child for visited_child in visited_list if visited_child == child]) > 0:
                    continue

                child.g = current_node.g + cost
                child.h =3* int(abs(child.position[0] - end_node.position[0])) + int(abs(child.position[1] - end_node.position[1]))
                # child.h = (((child.position[0] - end_node.position[0]) ** 2) +
                #             ((child.position[1] - end_node.position[1]) ** 2))
                print(child.h)

                child.f = child.g + child.h

                if len([i for i in yet_to_visit_list if child == i and child.g > i.g]) > 0:
                    continue
                if child not in yet_to_visit_list:
                    yet_to_visit_list.append(child)

    def return_path(self,visited,current_node,maze):
        path = []
        no_rows = len(maze)
        no_columns = len(maze[0])
        result = [[-1 for i in range(no_columns)] for j in range(no_rows)]
        current = current_node
        while current is not None:
            path.append(current.position)
            current = current.parent
        path = path[::-1]
        start_value = 0
        for i in range(len(path)):
            result[path[i][0]][path[i][1]] = start_value
            start_value += 1
        return visited,result