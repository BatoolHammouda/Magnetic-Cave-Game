import time

# Initialize the board
board = [[' ' for _ in range(8)] for _ in range(8)]


# Function to print the board
def print_board(board):
    for row in board:
        print(' | '.join(row))
        print('-' * 31)


# Function to check if a player has won
def check_winner(board, player):
    directions = [(1, 0), (0, 1), (1, 1), (-1, 1)]  # Down, Right, Diagonal, Reverse Diagonal

    for row in range(8):
        for col in range(8):
            if board[row][col] != " ":
                symbol = board[row][col]
                for direction in directions:
                    dx, dy = direction
                    count = 1
                    for i in range(1, 5):
                        new_row = row + i * dx
                        new_col = col + i * dy
                        if (
                                new_row < 0 or new_row >= 8 or
                                new_col < 0 or new_col >= 8 or
                                board[new_row][new_col] != symbol
                        ):
                            break
                        count += 1
                    if count == 5:
                        return True

    return False

# Function to check if the board is full
def is_board_full(board):
   return all(board[row][col] != ' ' for row in range(8) for col in range(8))




    # Heuristic function to evaluate the board
def evaluate_board(board):
    score = 0

    # Check rows
    for row in board:
        for i in range(4):
            window = row[i:i + 5]
            score += evaluate_window(window)

    # Check columns
    for col in range(8):
        for i in range(4):
            window = [board[row][col] for row in range(i, i + 5)]
            score += evaluate_window(window)

    # Check diagonals
    for i in range(4):
        for j in range(4):
            window = [board[i + k][j + k] for k in range(5)]
            score += evaluate_window(window)

            window = [board[i + k][j + 4 - k] for k in range(5)]
            score += evaluate_window(window)

    return score


# Heuristic function to evaluate a window of 5 bricks
def evaluate_window(window):
    score = 0

    if window.count('■') == 5:
        score += 1000
    elif window.count('■') == 4 and window.count(' ') == 1:
        score += 100
    elif window.count('■') == 3 and window.count(' ') == 2:
        score += 10

    if window.count('□') == 5:
        score -= 1000
    elif window.count('□') == 4 and window.count(' ') == 1:
        score -= 100
    elif window.count('□') == 3 and window.count(' ') == 2:
        score -= 10

    return score


def minimax(isMaximizing, depth, board):
    if depth == 3 or check_winner(board, '■') or check_winner(board, '□') or is_board_full(board):
        return evaluate_board(board)

    if isMaximizing:
        bestScore = float('-inf')
        for move in board.get_possible_moves():
            board.make_move(move)
            score = minimax(False, depth + 1, board)
            board.undo()
            bestScore = max(score, bestScore)
        return bestScore
    else:
        bestScore = float('inf')
        for move in board.get_possible_moves():
            board.make_move(move)
            score = minimax(True, depth + 1, board)
            board.undo()
            bestScore = min(score, bestScore)
        return bestScore


# Function to make the AI player's move
def compmove(board):
    start_time = time.time()
    best_score = float('-inf')
    best_move = (0, 0)

    for row in range(len(board)):
        for col in range(len(board[row])):
            if (
                (col == 0 or board[row][col - 1] != ' ') or
                (col == 7 or board[row][col + 1] != ' ')
            ) and board[row][col] == ' ':
                board[row][col] = '□'
                score = minimax(False, 3, board)
                board[row][col] = ' '

                if score > best_score:
                    best_score = score
                    best_move = (row, col)

                if time.time() - start_time >= 3:
                    return best_move

    return best_move


# Function to play the game
def play_game():
    current_player = '■'  # Player ■ starts the game

    while True:
        print_board(board)
        print("It's", current_player, "turn.")

        if current_player == '■':
            # Get the player's move
            valid_move = False
            while not valid_move:
                try:
                    row = int(input("Enter the row (0-7): "))
                    col = int(input("Enter the column (0-7): "))
                    if (
                            (col == 0 or board[row][col - 1] != ' ') or
                            (col == 7 or board[row][col + 1] != ' ')
                    ) and board[row][col] == ' ':
                        valid_move = True
                        board[row][col] = current_player
                    else:
                        print("Invalid move. Try again.")
                except ValueError as e:
                    print(e)

        else:
            # AI player's move
            row, col = compmove(board)
            board[row][col] = '□'

        # Check if the current player has won
        if check_winner(board, current_player):
            print_board(board)
            print("Player", current_player, "wins!")
            break

        # Check for a tie
        if is_board_full(board):
            print_board(board)
            print("It's a tie!")
            break

        # Switch to the next player
        current_player = '□' if current_player == '■' else '■'

# Start the game
play_game()

