import chess
import random
import tkinter as tk
import time
nodesearched = 0

def minimax(board, depth):
    global nodesearched
    nodesearched += 1
    if depth == 0:
        return evaluate(board)
    turn = board.turn
    if turn == chess.WHITE:
        bestscore = float("-inf")
        for move in board.legal_moves:
            board.push(move)
            score = minimax(board, depth - 1)
            board.pop()
            if score > bestscore:
                bestscore = score
        return bestscore

    elif turn == chess.BLACK:
        bestscore = float("inf")
        for move in board.legal_moves:
            board.push(move)
            score = minimax(board, depth - 1)
            board.pop()
            if score < bestscore:
                bestscore = score
        return bestscore


def blackmove(board):
    global nodesearched
    nodesearched = 0
    starttime = time.perf_counter()
    bestscore = float("inf")
    bestmove = None
    for move in board.legal_moves:
        board.push(move)
        tempscore = minimax(board, 2)
        board.pop()

        if tempscore < bestscore:
            bestscore = tempscore
            bestmove = move
    searchtime = time.perf_counter() - starttime

    print(f"Engine move: {bestmove}")
    print(f"Evaluation: {bestscore}")
    print(f"Positions searched: {nodesearched}")
    print(f"Search time: {round(searchtime, 3)}s")
    return bestmove

def evaluate(board):
    score = 0
    piecevalues = {chess.PAWN: 100, chess.KNIGHT: 300, chess.BISHOP: 300, chess.ROOK: 500, chess.QUEEN: 900}
    for piecetype, value in piecevalues.items():
        whitecount = len(board.pieces(piecetype, chess.WHITE))
        blackcount = len(board.pieces(piecetype, chess.BLACK))
        score += piecevalues[piecetype] * whitecount - piecevalues[piecetype] * blackcount
    centresquares = [chess.D4, chess.E4, chess.D5, chess.E5]
    for square in centresquares:
        piece = board.piece_at(square)
        if piece is not None:
            if piece.color ==  chess.WHITE:
                score += 20
            else:
                score -= 20
    return score

def getsquare(event):
    global selectedsquare
    column = event.x // squaresize
    row = event.y // squaresize
    guisquare = chess.square(column, 7 - row)
    squarename = chess.square_name(guisquare)
    piece = board.piece_at(guisquare)
    if selectedsquare is None:
        if piece is not None and piece.color == chess.WHITE:
            selectedsquare = guisquare
            print(f"Selected: ", chess.square_name(selectedsquare))
    else:
        cmove = chess.Move(selectedsquare, guisquare)
        print(cmove)
        if cmove in board.legal_moves:
            board.push(cmove)
            drawboard()
            selectedsquare = None
            bmove = blackmove(board)
            if bmove is not None:
                board.push(bmove)
                drawboard()
                print(evaluate(board))
        else:
            print("Illegal move!")
            selectedsquare = None

def drawboard():
    canvas.delete("all")
    for i in range (0, 8):
        for j in range(0, 8):
            square = chess.square(i, 7-j)
            x1 = squaresize * i
            y1 = squaresize * j
            x2 = x1 + squaresize
            y2 = y1 + squaresize
            if (i + j) % 2 == 1:
                canvas.create_rectangle(x1, y1, x2, y2, fill = "brown")
            else:
                canvas.create_rectangle(x1, y1, x2, y2, fill = "white")
            piece = board.piece_at(square)
            if piece is not None:
                x = i * squaresize + squaresize / 2
                y = j * squaresize + squaresize / 2
                canvas.create_text(x, y, text = piece.unicode_symbol(), font = ("Arial", 50))


squaresize = 640 // 8
selectedsquare = None

window = tk.Tk()
window.title("Explainable Chess Engine")

canvas = tk.Canvas(window, width = 640, height = 640)
canvas.pack()

board = chess.Board()
drawboard()
canvas.bind("<Button-1>", getsquare)

print(board)
print(evaluate(board))

window.mainloop()
