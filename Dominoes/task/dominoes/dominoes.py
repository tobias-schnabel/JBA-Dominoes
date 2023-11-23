import random

def create_domino_set():
    return [[i, j] for i in range(7) for j in range(i, 7)]

def shuffle_and_distribute(domino_set):
    random.shuffle(domino_set)
    return domino_set[0:14], domino_set[14:21], domino_set[21:28]

def find_starting_piece(player_pieces, computer_pieces):
    highest_double = -1
    starting_piece = []
    status = ""
    for piece in player_pieces:
        if piece[0] == piece[1] and piece[0] > highest_double:
            highest_double = piece[0]
            starting_piece = piece
            status = "player"
    for piece in computer_pieces:
        if piece[0] == piece[1] and piece[0] > highest_double:
            highest_double = piece[0]
            starting_piece = piece
            status = "computer"
    return starting_piece, status

def print_game_state(stock_pieces, computer_pieces, player_pieces, domino_snake):
    print('=' * 70)
    print(f"Stock size: {len(stock_pieces)}")
    print(f"Computer pieces: {len(computer_pieces)}\n")

    # Snake printing
    if len(domino_snake) > 6:
        domino_snake_display = ''.join(str(domino) for domino in domino_snake[:3]) + '...' + ''.join(str(domino) for domino in domino_snake[-3:])
    else:
        domino_snake_display = ''.join(str(domino) for domino in domino_snake)
    print(domino_snake_display + "\n")

    print("Your pieces:")
    for i, piece in enumerate(player_pieces, 1):
        print(f"{i}:{piece}")



def get_player_input(player_pieces, domino_snake):
    while True:
        try:
            move = int(input("> "))
            if move != 0:
                move_idx = abs(move) - 1
                if move_idx >= len(player_pieces):
                    raise ValueError
                if not can_place_domino(domino_snake, player_pieces[move_idx], move):
                    print("Illegal move. Please try again.")
                    continue
            return move
        except ValueError:
            print("Invalid input. Please try again.")

def can_place_domino(domino_snake, piece, side):
    if side < 0:
        return domino_snake[0][0] in piece
    else:
        return domino_snake[-1][1] in piece

def update_domino_snake(domino_snake, piece, side):
    if side < 0:
        if domino_snake[0][0] != piece[1]:
            piece.reverse()
        domino_snake.insert(0, piece)
    else:
        if domino_snake[-1][1] != piece[0]:
            piece.reverse()
        domino_snake.append(piece)

def is_draw_condition_met(domino_snake):
    ends = [domino_snake[0][0], domino_snake[-1][1]]
    count = sum(ends[0] == piece[i] or ends[1] == piece[i] for piece in domino_snake for i in range(2))
    return count >= 8 and ends[0] == ends[1]

def count_numbers(computer_pieces, domino_snake):
    counts = [0] * 7  # For numbers 0 through 6
    for piece in computer_pieces + domino_snake:
        for number in piece:
            counts[number] += 1
    return counts

def calculate_domino_scores(computer_pieces, counts):
    scores = []
    for piece in computer_pieces:
        score = counts[piece[0]] + counts[piece[1]]
        scores.append((score, piece))
    return scores

def computer_move(computer_pieces, domino_snake, stock_pieces):
    counts = count_numbers(computer_pieces, domino_snake)
    scored_pieces = calculate_domino_scores(computer_pieces, counts)

    # Sort the pieces by score in descending order
    scored_pieces.sort(reverse=True)

    for _, piece in scored_pieces:
        # Try to place the piece on either side
        for side in [-1, 1]:
            if can_place_domino(domino_snake, piece, side):
                computer_pieces.remove(piece)
                update_domino_snake(domino_snake, piece, side)
                return True  # Indicate a successful move

    # If no move is possible, draw from the stock if available
    if stock_pieces:
        computer_pieces.append(stock_pieces.pop())
    return False  # Indicate no move was made


# # Main execution
def main():
    # Initialization
    domino_set = create_domino_set()
    stock_pieces, player_pieces, computer_pieces = shuffle_and_distribute(domino_set)
    starting_piece, status = find_starting_piece(player_pieces, computer_pieces)

    while not starting_piece:
        stock_pieces, player_pieces, computer_pieces = shuffle_and_distribute(domino_set)
        starting_piece, status = find_starting_piece(player_pieces, computer_pieces)

    if status == "player":
        player_pieces.remove(starting_piece)
        status = "computer"
    else:
        computer_pieces.remove(starting_piece)
        status = "player"

    domino_snake = [starting_piece]

    # Print initial game state
    print_game_state(stock_pieces, computer_pieces, player_pieces, domino_snake)

    # Game Loop
    while True:
        if status == "player":
            print("\nStatus: It's your turn to make a move. Enter your command.")
            move = get_player_input(player_pieces, domino_snake)
            if move != 0:
                piece = player_pieces.pop(abs(move) - 1)
                update_domino_snake(domino_snake, piece, move)
            else:
                if stock_pieces:
                    player_pieces.append(stock_pieces.pop())
            status = "computer"
        else:
            print("\nStatus: Computer is about to make a move. Press Enter to continue...")
            input()  # Wait for the user to press Enter
            computer_move(computer_pieces, domino_snake, stock_pieces)
            status = "player"

        # Print updated game state after each turn
        print_game_state(stock_pieces, computer_pieces, player_pieces, domino_snake)

        # Check for end-game conditions
        if not player_pieces:
            print("Status: The game is over. You won!")
            break
        elif not computer_pieces:
            print("Status: The game is over. The computer won!")
            break
        elif is_draw_condition_met(domino_snake):
            print("Status: The game is over. It's a draw!")
            break


# Call the main function
if __name__ == "__main__":
    main()



