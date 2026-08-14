# agent.py

import random
from collections import deque
import heapq



class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        pos = percept['agent_pos']
        return random.choice(self.actions_pool)


class SearchAgent:

    def __init__(self):
        self.plan = []
        self.active_algo = 'BFS'  # Change to 'DFS' or 'UCS' for testing

    def get_neighbors(self, state, grid_size, walls):
        x, y = state
        width, height = grid_size

        neighbors = []

        directions = [
            (0, 1),   # Up
            (0, -1),  # Down
            (-1, 0),  # Left
            (1, 0)    # Right
        ]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if (
                0 <= nx < width and
                0 <= ny < height and
                (nx, ny) not in walls
            ):
                neighbors.append((nx, ny))

        return neighbors

    def path_to_actions(self, path):
        actions = []

        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]

            if x2 == x1 + 1:
                actions.append("Right")
            elif x2 == x1 - 1:
                actions.append("Left")
            elif y2 == y1 + 1:
                actions.append("Up")
            elif y2 == y1 - 1:
                actions.append("Down")

        return actions

    def bfs_search(self, start, goal, grid_size, walls):

        frontier = deque([(start, [start])])
        reached = {start}

        while frontier:

            state, path = frontier.popleft()

            if state == goal:
                return path

            for neighbor in self.get_neighbors(
                    state,
                    grid_size,
                    walls):

                if neighbor not in reached:
                    reached.add(neighbor)
                    frontier.append(
                        (neighbor, path + [neighbor])
                    )

        return None

    def dfs_search(self, start, goal, grid_size, walls):

        frontier = [(start, [start])]
        reached = {start}

        while frontier:

            state, path = frontier.pop()

            if state == goal:
                return path

            for neighbor in self.get_neighbors(
                    state,
                    grid_size,
                    walls):

                if neighbor not in reached:
                    reached.add(neighbor)
                    frontier.append(
                        (neighbor, path + [neighbor])
                    )

        return None

    def ucs_search(self, start, goal, grid_size, walls):

        frontier = []
        heapq.heappush(frontier, (0, start, [start]))

        reached = {start}

        while frontier:

            cost, state, path = heapq.heappop(frontier)

            if state == goal:
                return path

            for neighbor in self.get_neighbors(
                    state,
                    grid_size,
                    walls):

                if neighbor not in reached:
                    reached.add(neighbor)

                    heapq.heappush(
                        frontier,
                        (
                            cost + 1,
                            neighbor,
                            path + [neighbor]
                        )
                    )

        return None

    def sense_and_act(self, percept):

        if not self.plan:

            food_list = percept['all_food']

            if not food_list:
                return 'Up'

            start = percept['agent_pos']
            walls = set(percept['walls'])
            grid_size = percept['grid_size']

            # Find closest pellet using Manhattan distance
            goal = min(
                food_list,
                key=lambda food:
                abs(food[0] - start[0]) +
                abs(food[1] - start[1])
            )

            if self.active_algo == 'BFS':
                path = self.bfs_search(
                    start,
                    goal,
                    grid_size,
                    walls
                )

            elif self.active_algo == 'DFS':
                path = self.dfs_search(
                    start,
                    goal,
                    grid_size,
                    walls
                )

            elif self.active_algo == 'UCS':
                path = self.ucs_search(
                    start,
                    goal,
                    grid_size,
                    walls
                )

            else:
                path = []

            if path:
                self.plan = self.path_to_actions(path)

        if self.plan:
            return self.plan.pop(0)

        return 'Up'