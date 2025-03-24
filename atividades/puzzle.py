import random
import math
import time
from collections import deque

class Puzzle:
    def __init__(self):
        self.goal = ['1', '2', '3', '4', '5', '6', '7', '8', '0']
        self.start = self.goal[:]
        self.fronts = []

    def shuffle(self):
        for _ in range(50):
            self.move_randomly()

    def move_randomly(self):
        zero_idx = self.start.index('0')
        neighbors = self.get_neighbors(zero_idx)
        new_index = random.choice(neighbors)
        self.start[zero_idx], self.start[new_index] = self.start[new_index], self.start[zero_idx]

    def get_neighbors(self, index):
        neighbors = []
        if index % 3 > 0: neighbors.append(index - 1)  
        if index % 3 < 2: neighbors.append(index + 1) 
        if index // 3 > 0: neighbors.append(index - 3) 
        if index // 3 < 2: neighbors.append(index + 3)
        return neighbors

    def is_solved(self):
        return self.start == self.goal

    def horizontal_search(self):
        queue = deque([(self.start, [])])
        visited = set()
        states_expanded = 0
        start_time = time.time()

        while queue:
            current, moves = queue.popleft()
            visited.add(tuple(current))
            states_expanded += 1

            if current == self.goal:
                elapsed_time = time.time() - start_time
                return states_expanded, elapsed_time, moves
            
            zero_idx = current.index('0')
            for neighbor in self.get_neighbors(zero_idx):
                next_state = current[:]
                next_state[zero_idx], next_state[neighbor] = next_state[neighbor], next_state[zero_idx]
                if tuple(next_state) not in visited:
                    queue.append((next_state, moves + [self.format_move(zero_idx, neighbor)]))

        return states_expanded, time.time() - start_time, []

    def heuristic_search(self):
        queue = [(self.start, 0, [])]
        visited = set()
        states_expanded = 0
        start_time = time.time()

        while queue:
            current, g, moves = queue.pop(0)
            visited.add(tuple(current))
            states_expanded += 1

            if current == self.goal:
                elapsed_time = time.time() - start_time
                return states_expanded, elapsed_time, moves

            zero_idx = current.index('0')
            for neighbor in self.get_neighbors(zero_idx):
                next_state = current[:]
                next_state[zero_idx], next_state[neighbor] = next_state[neighbor], next_state[zero_idx]
                if tuple(next_state) not in visited:
                    h = self.manhattan_distance(next_state)
                    queue.append((next_state, g + 1 + h, moves + [self.format_move(zero_idx, neighbor)]))
                    queue.sort(key=lambda x: x[1])

        return states_expanded, time.time() - start_time, []

    def manhattan_distance(self, state):
        distance = 0
        for i in range(9):
            if state[i] != '0':
                goal_index = self.goal.index(state[i])
                distance += abs(goal_index % 3 - i % 3) + abs(goal_index // 3 - i // 3)
        return distance

    def format_move(self, from_idx, to_idx):
        """ Formata o movimento como uma string. """
        moves_dict = {1: "Esquerda", -1: "Direita", 3: "Cima", -3: "Baixo"}
        return f"{moves_dict[to_idx - from_idx]} ({from_idx}, {to_idx})"

    def execute_moves(self, moves):
        """ Executa e exibe cada movimento na sequência encontrada. """
        current = self.start[:]
        for move in moves:
            print(f"Movimento: {move}")
            zero_idx = current.index('0')
            direction, (from_idx, to_idx) = move.split()[0], map(int, move.split("(")[1].strip(")").split(", "))
            current[zero_idx], current[to_idx] = current[to_idx], current[zero_idx]
            print_puzzle(current)
            time.sleep(0.5)

def print_puzzle(puzzle):
    for i in range(0, 9, 3):
        print(f"{' '.join(puzzle[i:i+3])}")
    print()

def main():
    puzzle = Puzzle()
    puzzle.shuffle()
    print("Quebra-cabeça embaralhado:")
    print_puzzle(puzzle.start)

    while True:
        choice = input("Escolha a busca (h para horizontal, s para heurística, r para reiniciar, q para sair): ").lower()
        if choice == 'h':
            states, elapsed, moves = puzzle.horizontal_search()
            print(f"Busca Horizontal: Estados Expandidos: {states}, Tempo: {elapsed:.2f}s")
            print("Executando Movimentos:")
            puzzle.execute_moves(moves)
        elif choice == 's':
            states, elapsed, moves = puzzle.heuristic_search()
            print(f"Busca Heurística: Estados Expandidos: {states}, Tempo: {elapsed:.2f}s")
            print("Executando Movimentos:")
            puzzle.execute_moves(moves)
        elif choice == 'r':
            puzzle = Puzzle()
            puzzle.shuffle()
            print("Quebra-cabeça reiniciado:")
            print_puzzle(puzzle.start)
        elif choice == 'q':
            print("Saindo...")
            break
        else:
            print("Escolha inválida. Tente novamente.")

if __name__ == '__main__':
    main()
