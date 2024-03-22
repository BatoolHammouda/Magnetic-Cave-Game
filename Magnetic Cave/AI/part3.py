import time

# Initialize the board
board = [[' ' for _ in range(8)] for _ in range(8)]


# Function to print the board
def print_board(board):
    for row in board:
        print(' | '.join(row))
        print('-' * 31)


# Function to check if the board is full
def is_board_full(board):
    return all(board[row][col] != ' ' for row in range for col in range(8))


def check_winner(board, player):
    directions = [(1, 0), (0, 1), (1, 1), (-1, 1)]  # Down, Right, Diagonal, Reverse Diagonal

    for r in range(8):
        for c in range(8):
            if board[r][c] != " ":
                s = board[r][c]
                for direction in directions:
                    dx, dy = direction
                    count = 1
                    for i in range(1, 5):
                        row2 = r + i * dx
                        col2 = c + i * dy
                        if (
                                row2 < 0 or row2 >= 8 or
                                col2 < 0 or col2 >= 8 or
                                board[row2][col2] != s
                        ):
                            break
                        count += 1
                    if count == 5:
                        return True

    return False


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

    for r in range(len(board)):
        for c in range(len(board[r])):
            if (
                    (c == 0 or board[r][c - 1] != ' ') or
                    (c == 7 or board[r][c + 1] != ' ')
            ) and board[r][c] == ' ':
                board[r][c] = '■'
                score = minimax(False, 3, board)
                board[r][c] = ' '

                if score > best_score:
                    best_score = score
                    best_move = (r, c)

                if time.time() - start_time >= 3:
                    return best_move

    return best_move


# Function to play the game
def start():
    current_player = '□'  # Player ■ starts the game

    while True:
        print_board(board)
        print("It's", current_player, "turn.")

        if current_player == '□':
            # Get the player's move
            valid_move = False
            while not valid_move:
                try:
                    r = int(input("Enter the row (0-7): "))
                    c = int(input("Enter the column (0-7): "))
                    if (
                            (c == 0 or board[r][c - 1] != ' ') or
                            (c == 7 or board[r][c + 1] != ' ')
                    ) and board[r][c] == ' ':
                        valid_move = True
                        board[r][c] = current_player
                    else:
                        print("Invalid move. Try again.")
                except ValueError as e:
                    print(e)

        else:
            # AI player's move
            r, c = compmove(board)
            board[r][c] = '■'

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

        current_player = '■' if current_player == '□' else '□'


# Start the game
start()