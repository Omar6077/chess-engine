import chess
import random
import tkinter as tk

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

window.mainloop()
