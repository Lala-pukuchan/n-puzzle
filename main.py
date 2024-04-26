import sys
from puzzle import a_star_search


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


# def print_solution(solution, total_states_selected, max_states_in_memory):
#    path, move_count = solution
#    print(f"Total number of states selected: {total_states_selected}")
#    print(f"Maximum number of states in memory: {max_states_in_memory}")
#    print(f"Number of moves: {len(path) - 1}")
#    for move, state in enumerate(reversed(path)):
#        print(f"Move {move}:")
#        print(state)
#        print()


def check_exist_solution(input_array, goal_array):
    input_array = [item for sublist in input_array for item in sublist]
    goal_array = [item for sublist in goal_array for item in sublist]
    inv_count_input = 0
    inv_count_goal = 0
    for i in range(len(input_array)):
        for j in range(i + 1, len(input_array)):
            if input_array[i] and input_array[j] \
                    and input_array[i] > input_array[j]:
                inv_count_input += 1
            if goal_array[i] and goal_array[j] \
                    and goal_array[i] > goal_array[j]:
                inv_count_goal += 1
    if inv_count_input % 2 == inv_count_goal % 2:
        return True
    return False


def generate_snail_goal(n):
    goal_array = [[0] * n for _ in range(n)]
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    cur_dir = 0
    x, y = 0, 0
    for i in range(1, n * n):
        goal_array[x][y] = i
        next_x, next_y = x + directions[cur_dir][0], y + directions[cur_dir][1]
        if not (
            0 <= next_x < n
            and 0 <= next_y < n
            and goal_array[next_x][next_y] == 0
        ):
            cur_dir = (cur_dir + 1) % 4
            next_x, next_y = (
                x + directions[cur_dir][0],
                y + directions[cur_dir][1],
            )
        x, y = next_x, next_y
    goal_array[x][y] = 0
    return goal_array


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    input_array = []
    goal_array = []

    with open(filename, "r") as file:
        lines = file.readlines()
        n = 0
        read_lines = 0
        for line in lines:
            line = line.strip()
            if line.startswith("#") or not line:
                continue
            if n == 0:
                n = int(line)
                goal_array = generate_snail_goal(n)
            else:
                if read_lines < n:
                    row = [int(x) for x in line.split() if x.isdigit()]
                    input_array.append(row)
                    read_lines += 1

    print("Input Array:")
    for row in input_array:
        print(row)
    print("Goal Array:")
    for row in goal_array:
        print(row)

    if not check_exist_solution(input_array, goal_array):
        print("Unsolvable puzzle.")
        sys.exit(0)

    solution = a_star_search(input_array, goal_array, heuristic="hamming")
    if solution:
        print_solution(solution)
    else:
        print("No solution found.")

    # solution, total_states_selected, max_states_in_memory = a_star_search(
    #    input_array, goal_array, heuristic="hamming"
    # )
    # if solution:
    #    print_solution(solution, total_states_selected, max_states_in_memory)
    # else:
    #    print("No solution found.")
    #    sys.exit(0)


if __name__ == "__main__":
    main()
