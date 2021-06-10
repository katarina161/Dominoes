import random

from collections import defaultdict
# Write your code here

domino_set = []
for i in range(7):
    for j in range(7):
        if [j, i] in domino_set:
            continue
        domino_set.append([i, j])


def remove_elements_from_list(list_of_elements: list, *elements_to_remove):
    for el in elements_to_remove:
        list_of_elements.remove(el)


def deal_dominoes():
    stock_pieces = random.sample(domino_set, 14)
    remove_elements_from_list(domino_set, *stock_pieces)

    computer_pieces = random.sample(domino_set, 7)
    remove_elements_from_list(domino_set, *computer_pieces)

    player_pieces = domino_set.copy()
    domino_set.clear()

    return stock_pieces, computer_pieces, player_pieces


def find_double_max(pieces):
    maximum = [-1, -1]
    for p in pieces:
        if p[0] == p[1] and p[0] > maximum[0]:
            maximum = p

    return maximum if sum(maximum) != -2 else None


def determine_starting_piece(comp_pieces, p_pieces):
    c_max = find_double_max(comp_pieces)
    p_max = find_double_max(p_pieces)

    if (c_max and not p_max) or (c_max and c_max > p_max):
        comp_pieces.remove(c_max)
        return c_max
    elif (p_max and not c_max) or (p_max and p_max > c_max):
        p_pieces.remove(p_max)
        return p_max


def possible_to_continue_playing(dominoes):
    num = dominoes[0][0]
    if dominoes[-1][-1] != num:
        return True

    count = 0
    for d in dominoes:
        if num in d:
            count += 1
    return not count == 8


def add_selected_domino_to_snake(d_index, dominoes):
    if not -len(dominoes) <= d_index <= len(dominoes):
        raise ValueError

    if d_index == 0:
        if stock_pieces:
            domino_from_stock = random.choice(stock_pieces)
            dominoes.append(domino_from_stock)
            stock_pieces.remove(domino_from_stock)
        return True

    selected_domino = dominoes[abs(d_index) - 1]
    if d_index > 0:
        if snake[-1][-1] not in selected_domino:
            return False
        if snake[-1][-1] == selected_domino[0]:
            snake.append(selected_domino)
        else:
            snake.append(selected_domino[::-1])
    else:
        selected_domino = dominoes[abs(d_index) - 1]
        if snake[0][0] not in selected_domino:
            return False
        if snake[0][0] == selected_domino[-1]:
            snake.insert(0, selected_domino)
        else:
            snake.insert(0, selected_domino[::-1])

    dominoes.remove(selected_domino)
    return True


def add_domino_by_computer(domino):
    if snake[-1][-1] not in domino and snake[0][0] not in domino:
        return False

    if snake[-1][-1] in domino:
        if snake[-1][-1] == domino[0]:
            snake.append(domino)
        else:
            snake.append(domino[::-1])
    elif snake[0][0] in domino:
        if snake[0][0] == domino[-1]:
            snake.insert(0, domino)
        else:
            snake.insert(0, domino[::-1])
    computer_pieces.remove(domino)
    return True


def get_domino_scores(dominoes):
    num_scores = defaultdict(int)
    for num in [n for d in dominoes for n in d]:
        num_scores[num] += 1
    for num in [n for d in snake for n in d]:
        num_scores[num] += 1

    domino_scores = {}
    for d in dominoes:
        domino_scores[tuple(d)] = num_scores[d[0]] + num_scores[d[1]]

    return domino_scores


started = False
while not started:
    snake = []
    stock_pieces, computer_pieces, player_pieces = deal_dominoes()
    first_domino = determine_starting_piece(computer_pieces, player_pieces)
    if not first_domino:
        continue

    started = True
    snake.append(first_domino)

    player_turn = (len(player_pieces) == 7)
    end = False
    winner = None

    while not end:
        print("=" * 70)
        print(f"Stock size: {len(stock_pieces)}")
        print(f"Computer pieces: {len(computer_pieces)}")

        print()
        # Print first and last 3 dominoes in the snake
        for domino in snake:
            if not 2 < snake.index(domino) < len(snake) - 3:
                print(domino, end="")
            elif snake.index(domino) == 3:
                print("...", end="")

        print("\n")
        print("Your pieces:")
        for order_num, domino in enumerate(player_pieces, start=1):
            print(f"{order_num}:{domino}")

        # print("Comp: " + ", ".join([str(d) for d in computer_pieces]) + "\n")

        if not possible_to_continue_playing(snake):
            print("\nStatus: The game is over. It's a draw!")
            break

        if winner == "player":
            print("\nStatus: The game is over. You won!")
            break
        elif winner == "computer":
            print("\nStatus: The game is over. The computer won!")
            break

        print()
        if not player_turn:
            # Computers turn
            input("Status: Computer is about to make a move. Press Enter to continue...\n")
            played = False
            while not played:
                for d in sorted(get_domino_scores(computer_pieces), key=lambda item: item[1], reverse=True):
                    valid = add_domino_by_computer(list(d))
                    if valid:
                        played = True
                        break
                else:
                    add_selected_domino_to_snake(0, computer_pieces)
                    played = True
                    break
                # domino_index = random.randint(-len(computer_pieces), len(computer_pieces))
                # valid = add_selected_domino_to_snake(domino_index, computer_pieces)

            player_turn = True

            if not computer_pieces:
                winner = "computer"

        else:
            # Players turn
            print("Status: It's your turn to make a move. Enter your command.")
            valid = False
            while not valid:
                try:
                    domino_index = int(input())
                    valid = add_selected_domino_to_snake(domino_index, player_pieces)
                    if not valid:
                        print("Illegal move. Please try again.")
                except ValueError:
                    print("Invalid input. Please try again.")

            player_turn = False

            if not player_pieces:
                winner = "player"
