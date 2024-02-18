import customtkinter as ctk

class MatrixButton(ctk.CTkButton):
    def __init__(self, master, row, col, command=None, **kwargs):
        super().__init__(master, command=lambda: command(self), **kwargs)
        self.row = row
        self.col = col
        self.route = []
        self.painted = False

def create_matrix_buttons(frame, matrix_size, commands):
    button_matrix = [[None] * matrix_size for _ in range(matrix_size)]

    for row in range(matrix_size):
        for col in range(matrix_size):
            button = MatrixButton(frame, row, col, command=commands, text="", width=25, height=25, fg_color="white",border_width=0.5,border_color="black")
            button.grid(row=row, column=col)
            button_matrix[row][col] = button

    return button_matrix