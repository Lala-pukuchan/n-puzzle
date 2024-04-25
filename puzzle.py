import heapq
import numpy as np
from queue import PriorityQueue
import sys


class puzzle:
    def __init__(self, board, goal, moves=0, prev=None, heuristic="manhattan"):
        self.board = np.array(board)
        self.prev = prev
        self.moves = moves
        self.goal = goal
        self.empty_pos = (
            np.where(self.board == 0)[0][0],
            np.where(self.board == 0)[1][0],
        )
        self.dimension = self.board.shape[0]
        if heuristic == "manhattan":
            self.heuristic_value = self.calculate_manhattan_distance()
        elif heuristic == "hamming":
            self.heuristic_value = self.calculate_hamming_distance()
        elif heuristic == "linear_conflict":
            self.heuristic_value = self.calculate_linear_conflict()
        self.f = self.moves + self.heuristic_value

    def calculate_linear_conflict(self):
        distance = 0
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.board[i, j] != 0:
                    x, y = np.where(self.goal == self.board[i, j])
                    distance += abs(x - i) + abs(y - j)
        return distance

    def calculate_manhattan_distance(self):
        distance = 0
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.board[i, j] != 0:
                    x, y = np.where(self.goal == self.board[i, j])
                    distance += abs(x - i) + abs(y - j)
        return distance

    def calculate_hamming_distance(self):
        return (
            np.sum(self.board != self.goal) - 1
            if 0 in self.goal
            else np.sum(self.board != self.goal)
        )

    def generate_successors(self):
        successors = []
        x, y = self.empty_pos
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.dimension and 0 <= ny < self.dimension:
                new_board = self.board.copy()
                new_board[x, y], new_board[nx, ny] = new_board[nx, ny], new_board[x, y]
                successors.append(puzzle(new_board, self.goal, self.moves + 1, self))
        return successors

    def __lt__(self, other):
        return self.f < other.f

    def __repr__(self):
        return f"puzzle(moves={self.moves}, heuristic={self.heuristic_value}, board=\n{self.board})"


def a_star_search(initial, goal, heuristic="manhattan"):
    open_set = []
    closed_set = set()
    initial_state = puzzle(initial, goal, heuristic=heuristic)
    heapq.heappush(open_set, initial_state)
    while open_set:
        current_state = heapq.heappop(open_set)
        if np.array_equal(current_state.board, goal):
            return current_state
        closed_set.add(tuple(map(tuple, current_state.board)))
        for successor in current_state.generate_successors():
            if tuple(map(tuple, successor.board)) in closed_set:
                continue
            heapq.heappush(open_set, successor)
    return None

