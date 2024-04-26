import heapq
import numpy as np


class puzzle:
    def __init__(self, board, goal, moves=0, prev=None, heuristic="manhattan"):

        # set the initial state of the puzzle
        self.board = np.array(board)
        self.prev = prev
        self.moves = moves
        self.goal = goal
        self.empty_pos = (
            np.where(self.board == 0)[0][0],
            np.where(self.board == 0)[1][0],
        )
        self.dimension = self.board.shape[0]
        self.heuristic = heuristic

        # calculate the heuristic value
        if heuristic == "manhattan":
            self.heuristic_value = self.calculate_manhattan_distance()
        elif heuristic == "hamming":
            self.heuristic_value = self.calculate_hamming_distance()
        elif heuristic == "linear_conflict":
            self.heuristic_value = self.calculate_linear_conflict()
        self.f = self.moves + self.heuristic_value

    def calculate_linear_conflict(self):
        manhattan_distance = self.calculate_manhattan_distance()
        linear_conflict = 0

        # Check rows for linear conflict
        for i in range(self.dimension):
            current_row = []
            goal_row = []
            for j in range(self.dimension):
                if self.board[i][j] != 0 and (self.board[i][j] in self.goal[i]):
                    current_row.append(self.board[i][j])
                if self.goal[i][j] != 0:
                    goal_row.append(self.goal[i][j])
            linear_conflict += self.count_conflicts(current_row, goal_row)

        # Check columns for linear conflict
        for j in range(self.dimension):
            current_col = []
            goal_col = []
            for i in range(self.dimension):
                if self.board[i][j] != 0:
                    current_col.append(self.board[i][j])
                if self.goal[i][j] != 0:
                    goal_col.append(self.goal[i][j])

            # Filter current_col to only include elements that are also in goal_col
            current_col = [x for x in current_col if x in goal_col]
            linear_conflict += self.count_conflicts(current_col, goal_col)

        return manhattan_distance + 2 * linear_conflict

    def count_conflicts(self, current, goal):
        conflict = 0
        for i in range(len(current)):
            for j in range(i + 1, len(current)):
                if goal.index(current[i]) > goal.index(current[j]):
                    conflict += 1
        return conflict

    def calculate_manhattan_distance(self):
        distance = 0
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.board[i, j] != 0:
                    x, y = np.where(self.goal == self.board[i, j])
                    distance += abs(x - i) + abs(y - j)
        return distance

    def calculate_hamming_distance(self):
        print("hamming")
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
                new_board[x, y], new_board[nx, ny] = \
                    new_board[nx, ny], new_board[x, y]
                successors.append(
                    puzzle(
                        new_board,
                        self.goal,
                        self.moves + 1,
                        self,
                        heuristic=self.heuristic,
                    )
                )
        return successors

    def __lt__(self, other):
        return self.f < other.f

    def __repr__(self):
        return f"puzzle(moves={self.moves}, heuristic={self.heuristic_value}, \
            board=\n{self.board})"


def a_star_search(initial, goal, heuristic="manhattan"):
    # to check algorithm efficiency
    total_states_selected = 0
    max_states_in_memory = 0

    open_set = []
    closed_set = set()
    initial_state = puzzle(initial, goal, heuristic=heuristic)
    heapq.heappush(open_set, initial_state)
    while open_set:
        current_state = heapq.heappop(open_set)
        total_states_selected += 1
        if np.array_equal(current_state.board, goal):
            return current_state, total_states_selected, max_states_in_memory
        closed_set.add(tuple(map(tuple, current_state.board)))
        for successor in current_state.generate_successors():
            if tuple(map(tuple, successor.board)) in closed_set:
                continue
            heapq.heappush(open_set, successor)
        max_states_in_memory = max(
            max_states_in_memory, len(open_set) + len(closed_set)
        )
    return None, total_states_selected, max_states_in_memory
