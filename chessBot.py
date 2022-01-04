import math
import timeit
import chess
import random

piece_value = {
    "p": -1,
    "n": -3,
    "b": -3,
    "r": -5,
    "q": -9,
    "k": -100,
    "P": 1,
    "N": 3,
    "B": 3,
    "R": 5,
    "Q": 9,
    "K": 100
}

def evaluate_state(board):
    score = 0
    # print("EVALUATING:")
    # print(board)
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            #figure out piece type
            score += piece_value[str(piece)]
    # print("SCORE: " + str(score))
    return score

def random_chess_game(number_of_moves):
    for x in range(number_of_moves + 1):
        legal_moves = str(board.legal_moves)[38:-2].replace(',', '').split()
        board.push_san(legal_moves[random.randint(0, len(legal_moves))])
        print(board)
        print("\n")

def minimax(board, depth, maximizingPlayer):
    if board.outcome():
        return board.outcome()
    if depth == 0:
        return evaluate_state(board), "should be replaced"

    if maximizingPlayer:
        maxEval = -math.inf
        legal_moves = str(board.legal_moves)[38:-2].replace(',', '').split()
        for move in legal_moves:
            # print(move)
            board.push_san(move)
            next_move = minimax(board, depth - 1, False) #should return a tuple (float, str)
            print(next_move)
            eval = next_move[0] #eval now holds the float
            board.pop()
            # print(maxEval)
            # print(eval)
            if maxEval < eval:
                maxEval = eval
                best_move = move
                # print("BEST MOVE:" + best_move)
                # print("MOVE: " + move)
        return max(maxEval, eval), best_move
    else:
        minEval = math.inf
        legal_moves = str(board.legal_moves)[38:-2].replace(',', '').split()
        for move in legal_moves:
            board.push_san(move)
            next_move = minimax(board, depth - 1, True)
            eval = next_move[0]
            board.pop()
            # print(minEval)
            # print(eval)
            if minEval > eval:
                minEval = eval
                best_move = move
                # print("BEST MOVE:" + best_move)
                # print("MOVE: " + move)
        return min(minEval, eval), best_move

#when calling this, pass in alpha = +inf and beta = -inf
def minimax_alpha_beta(board, depth, alpha, beta, maximizingPlayer):
    if board.is_game_over():
        if board.outcome().winner:
            return math.inf, "white wins"
        elif not board.outcome().winner:
            return -math.inf, "black wins"
        else:
            return 0, "draw"
    if depth == 0:
        return evaluate_state(board), "replace"

    if maximizingPlayer:
        maxEval = -math.inf
        legal_moves = str(board.legal_moves)[38:-2].replace(',', '').split()
        for move in legal_moves:
            board.push_san(move)
            next_move = minimax_alpha_beta(board, depth - 1, alpha, beta, False) #should return a tuple (float, str)
            eval = next_move[0] #eval now holds the float
            board.pop()

            if maxEval < eval:
                maxEval = eval
                best_move = move

            alpha = max(alpha, eval)
            if beta <= alpha:
                break

        return max(maxEval, eval), best_move
    else:
        minEval = math.inf
        legal_moves = str(board.legal_moves)[38:-2].replace(',', '').split()
        for move in legal_moves:
            board.push_san(move)
            next_move = minimax_alpha_beta(board, depth - 1, alpha, beta, True)
            eval = next_move[0]
            board.pop()
            if minEval > eval:
                minEval = eval
                best_move = move

            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min(minEval, eval), best_move

def play_game(board):
    who_plays = True
    print(board)
    move_turn = "a"
    while(move_turn != "q"):
        move_turn = input()
        try:
            board.push_san(move_turn)
        except ValueError:
            print("Please input a valid move")
            continue

        #displays board
        if who_plays:
            print("White moved " + move_turn)
        else:
            print("Black moved " + move_turn)
        print(board)

        #switches turn logic and asks for next move
        who_plays = not who_plays

def play_ai(board, player_color):
    if player_color:
        print(board)
        while(not board.outcome()):
            #player moves
            move_turn = input()
            try:
                board.push_san(move_turn)
            except ValueError:
                print("Please input a valid move")
                continue
            #computer moves
            move = minimax_alpha_beta(board, 4, -math.inf, math.inf, False)
            board.push_san(move[1])
            print(board)
            print("\n")
        print(board.outcome())
    else:
        print(board)
        while(not board.outcome()):
            #computer moves
            move = minimax_alpha_beta(board, 4, -math.inf, math.inf, True)
            board.push_san(move[1])
            # player moves
            move_turn = input()
            try:
                board.push_san(move_turn)
            except ValueError:
                print("Please input a valid move")
                continue
            print("\n")
        print(board.outcome())


board = chess.Board()
play_ai(board, True)
#play_game(board)
# board.push_san("e4")
# board.push_san("e5")
# board.push_san("Nf3")
# board.push_san("Nc6")
# board.push_san("d4")
# board.push_san("exd4")

# board.push_san("b4")
# board.push_san("c5")

# board.push_san("b4")
# board.push_san("b5")
# board.push_san("a3")
# board.push_san("d6")
# board.push_san("h4")
# board.push_san("g5")

# board.push_san("e4")
# board.push_san("Nh6")
# board.push_san("e5")
# board.push_san("Rg8")
# board.push_san("e6")

# current_board_score = evaluate_state(board)
# print("The board state is " + str(current_board_score))

# print(board)
# print("\n")

# test mini_max
# start = timeit.default_timer()
# print("The best move results in a score of " + str(minimax(board, 4, True)))
# stop = timeit.default_timer()
#
#test mini_max w/ alpha beta pruning
# start = timeit.default_timer()
# print("The best move has a score of " + str(minimax_alpha_beta(board, 2, -math.inf, math.inf, False)))
# stop = timeit.default_timer()
# print("Program executed in " + str(stop - start))
#
# print(board)
# print(str(board.legal_moves)[38:-2].replace(',', '').split())
# print("\n")

