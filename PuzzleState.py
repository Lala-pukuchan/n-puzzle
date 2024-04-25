import heapq
import numpy as np


class PuzzleState:
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
        self.f = self.moves + self.heuristic_value

    def calculate_manhattan_distance(self):
        distance = 0
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.board[i, j] != 0:
                    x, y = divmod(self.board[i, j] - 1, self.dimension)
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
                successors.append(
                    PuzzleState(new_board, self.goal, self.moves + 1, self)
                )
        return successors

    def __lt__(self, other):
        return self.f < other.f

    def __repr__(self):
        return f"PuzzleState(moves={self.moves}, heuristic={self.heuristic_value}, board=\n{self.board})"


def a_star_search(initial, goal, heuristic="manhattan"):
    open_set = []
    closed_set = set()
    initial_state = PuzzleState(initial, goal, heuristic=heuristic)
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


def print_solution(solution):
    path = []
    while solution:
        path.append(solution.board)
        solution = solution.prev
    move_count = 0
    for step in reversed(path):
        print(f"Move {move_count}:")
        print(step)
        print()
        move_count += 1


# Example usage
initial = [[2, 8, 3], [1, 6, 4], [7, 0, 5]]
goal = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]
solution = a_star_search(initial, goal, heuristic="hamming")
# if solution:
#    print_solution(solution)
# else:
#    print("No solution found.")