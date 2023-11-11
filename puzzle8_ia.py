import random
from node import *
import copy
import os, sys
import time


def main():
    final_state = [
                    [1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 0]
                ]


    def check_possibility_of_solution(state): # verifica a paridade do estado, caso for par, então há solução
        arr_state = []
        parity = 0
        for arr in state:
            for n in arr:
                if n != 0:
                    arr_state.append(n)

        for i in range(0, 8):
            for j in range(i + 1, 8):
                if arr_state[i] > arr_state[j]:
                    parity += 1

        if parity % 2 == 0:
            return True
        else:
            return False


    def shuffle_numbers():
        numbers = []

        while True:
            initial_state = [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0]
                ]

            while len(numbers) != 8: 
                for m in range(0, 3):
                    for n in range(0, 3):
                        drawn_number = random.randrange(1, 9)
                        if drawn_number not in numbers and initial_state[m][n] == 0:
                            initial_state[m][n] = drawn_number
                            numbers.append(drawn_number)
            if check_possibility_of_solution(initial_state) and initial_state != final_state:
                return initial_state

        return 0

    
    def find_element(state, element=0):
        for i in range(0, 3):
            for j in range(0, 3):
                if state[i][j] == element:
                    return i, j


    def distance_between_elements(state, final_state):
        heuristic = 0

        for row in state:
            for element in row:
                i, j = find_element(state, element)
                i_final, j_final = find_element(final_state, element)
                heuristic += abs(i - i_final) + abs(j - j_final)

        return heuristic


    def print_state(state):
        for row in state:
            print(row)


    #funções de movimento no tabuleiro
    def move_down(state):
        i, j = find_element(state, 0)
        if i < 2:
            state[i][j] = state[i+1][j]
            state[i+1][j] = 0
        return state


    def move_up(state):
        i, j = find_element(state, 0)
        if i > 0:
            state[i][j] = state[i-1][j]
            state[i-1][j] = 0
        return state


    def move_right(state):
        i, j = find_element(state, 0)
        if j < 2:
            state[i][j] = state[i][j+1]
            state[i][j+1] = 0
        return state


    def move_left(state):
        i, j = find_element(state, 0)
        if j > 0:
            state[i][j] = state[i][j-1]
            state[i][j-1] = 0
        return state


    #criando no
    def create_node(state, parent_node, g=0):
        h = g + distance_between_elements(state, final_state)
        return Node(state, parent_node, g, h)


    def insert_node_in_border(node, border):
        if node in border:
            return border
        border.append(node)
        key = border[-1]
        j = len(border) - 2

        while border[j].h > key.h and j >= 0:
            border[j+1] = border[j]
            border[j] = key
            j -= 1
        
        return border


    def calculate_successors(node):
        state = node.state
        parent_node = node.parent_node

        if parent_node:
            parent_state = parent_node.state
        else:
            parent_state = None

        successor_list = []
        move1 = move_up(copy.deepcopy(state))
        if move1 != state:
            successor_list.append(move1)

        move2 = move_down(copy.deepcopy(state))
        if move2 != state:
            successor_list.append(move2)

        move3 = move_right(copy.deepcopy(state))
        if move3 != state:
            successor_list.append(move3)

        move4 = move_left(copy.deepcopy(state))
        if move4 != state:
            successor_list.append(move4)

        return successor_list


    def ai_search(initial_node, final_state):
        n_movements = 0
        edge = [initial_node]

        while edge:
            node = edge.pop(0)
            if node.state == final_state:
                solution = []
                while True:
                    solution.append(node.state)
                    node = node.parent_node
                    if not node: break
                solution.reverse()
                return solution, n_movements
            n_movements += 1
            successor_list = calculate_successors(node)
            for s in successor_list:
                insert_node_in_border(create_node(s, node, node.g+1), edge)
        
        return 0, n_movements


    # comandos:
    while True:
        os.system("clear")
        initial_state = shuffle_numbers()
        print("O estado inicial do seu 8 Puzzle game é: ")
        print_state(initial_state)
        print("\nPara que a IA comece a resolver o puzzle, pressione 'Enter'...")
        print("\nCaso deseja fechar o programa aperte 'Ctrl + c'")
        input()

        os.system("clear")
        print("A IA está calculando as possibilidades e encontrando a solução...")
        time.sleep(3)

        initial_node = create_node(initial_state, None)
        solution_list, n_movements = ai_search(initial_node, final_state)

        os.system("clear")
        print("Os passos para a solução do seu Puzzle são: ")

        if solution_list == 0:
            print("A solução não foi encontrada, aperte 'Enter' para tentar novamente...")
        else:
            n = 1
            for solution in solution_list:
                print(f"\n{n}° estado: ")
                print_state(solution)
                n += 1
                time.sleep(1)
            
            print("\nSolução encontrada, para rodar novamente pressione 'Enter'...")

        input()


if __name__ == "__main__":
    main()