class Node:
    def __init__(self, parent=None, position=None):

        self.parent = parent
        self.position = position

    def __eq__(self, other):
        return self.position == other.position


class Bfs():
    def __init__(self):
        self.visited = []
        self.queue = []

    def search(self, maze, start, end):
        start_node = Node(None, tuple(start))
        end_node = Node(None, tuple(end))

        self.queue.append(start_node)

        no_rows = len(maze)
        no_columns = len(maze[0])

        move = [[-1, 0], [0, -1], [1, 0], [0, 1]]

        while (len(self.queue) > 0):
            children = []
            current_node = self.queue.pop(0)

            if current_node.position not in self.visited:

                self.visited.append(current_node.position)

            for new_position in move:
                node_position = (current_node.position[0] + new_position[0],
                                 current_node.position[1] + new_position[1])

                if (node_position[0] > (no_rows - 1) or node_position[0] < 0
                        or node_position[1] > (no_columns - 1)
                        or node_position[1] < 0):
                    continue
                if maze[node_position[0]][node_position[1]] != 0:
                    continue
                if node_position in self.visited:
                    continue

                new_node = Node(current_node, node_position)

                if new_node not in self.queue:
                    self.queue.append(new_node)

                if new_node.position == end_node.position:
                    return self.return_path(self.visited, current_node, maze)

    def return_path(self, visited, current_node, maze):
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
        return visited, result
