import customtkinter as ctk
import tkinter as tk
from MatrixButton import create_matrix_buttons

canvas_size = 600
matrix_size = 24
Currently = "start"
posStart = {'value': 0, 'row': 0,'col': 0}
posEnd = {'value': 0, 'row': 0,'col': 0}
myQ = []
endRoute = None

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def startClick():
    global Currently
    Currently = "start"
    start.configure(state=ctk.DISABLED)
    end.configure(state=ctk.NORMAL)
    buildWall.configure(state=ctk.NORMAL)
    
def endClick():
    global Currently
    Currently = "end"
    end.configure(state=ctk.DISABLED)
    start.configure(state=ctk.NORMAL)
    buildWall.configure(state=ctk.NORMAL)

def algoClick():
    global Currently
    Currently = "algo"
    start.configure(state=ctk.DISABLED)
    end.configure(state=ctk.DISABLED)
    buildWall.configure(state=ctk.DISABLED)
    algo.configure(state=ctk.DISABLED)
    Play(button_matrix[posStart['row']][posStart["col"]])
    
def WallClick():
    global Currently
    Currently = "wall"
    buildWall.configure(state=ctk.DISABLED)
    start.configure(state=ctk.NORMAL)
    end.configure(state=ctk.NORMAL)

def BFS(myQ):
    if len(myQ) == 0:
        return None

    current, route = myQ.pop(0)

    while current.painted:
        if len(myQ) == 0:
            return None
        current, route = myQ.pop(0)

    print("in", current.row, current.col)
    current.painted = True
    route.append([current.row, current.col])
    current.route = route.copy()
    
    if (current != button_matrix[posStart['row']][posStart["col"]]) and (current != button_matrix[posEnd['row']][posEnd["col"]]):
        current.configure(fg_color="#FF9999")

    if current.row == posEnd["row"] and current.col == posEnd["col"]:
        return route

    row = current.row
    col = current.col

    if row + 1 < matrix_size and button_matrix[row + 1][col].painted != True:
        myQ.append([button_matrix[row + 1][col], route.copy()])  
    if row - 1 >= 0 and button_matrix[row - 1][col].painted != True:
        myQ.append([button_matrix[row - 1][col], route.copy()]) 
    if col + 1 < matrix_size and button_matrix[row][col + 1].painted != True:
        myQ.append([button_matrix[row][col + 1], route.copy()]) 
    if col - 1 >= 0 and button_matrix[row][col - 1].painted != True:
        myQ.append([button_matrix[row][col - 1], route.copy()])  

    return BFS(myQ)
    
def routeFound(route):
    if not route:
        label.text = "no route found"
    else:
        for node in route:
            if (
                node != [posStart['row'], posStart['col']]
                and node != [posEnd['row'], posEnd['col']]
            ):
                button_matrix[node[0]][node[1]].configure(fg_color="#54E936")

        
def Play(button):
    global Currently
    if Currently == "start" and posStart['value'] == 0:
        button.configure(fg_color="#990000", state=tk.DISABLED)
        posStart['value'] = 1
        posStart['row'] = button.row
        posStart['col'] = button.col
    elif Currently == "start" and posStart['value'] != 0:
        button_matrix[posStart['row']][posStart['col']].configure(fg_color="white", state=tk.NORMAL)
        button.configure(fg_color="#FC5757", state=tk.DISABLED)
        posStart['row'] = button.row
        posStart['col'] = button.col
    elif Currently == "end" and posEnd['value'] == 0:
        button.configure(fg_color="#27DDF2", state=tk.DISABLED)
        posEnd['value'] = 1
        posEnd['row'] = button.row
        posEnd['col'] = button.col
    elif Currently == "end" and posEnd['value'] != 0:
        button_matrix[posEnd['row']][posEnd['col']].configure(fg_color="white", state=tk.NORMAL)
        button.configure(fg_color="#FC5757", state=tk.DISABLED)
        posEnd['row'] = button.row
        posEnd['col'] = button.col
    elif Currently == "wall":
        if button.painted == False:
            button.configure(fg_color="#D76E06")
            button.painted = True
        else:
            button.configure(fg_color="white")
            button.painted = False
    elif Currently == "algo":
        if posEnd['value'] == 0 or posStart['value'] == 0:
            start.configure(state=ctk.NORMAL)
            end.configure(state=ctk.NORMAL)
            buildWall.configure(state=ctk.NORMAL)
            algo.configure(state=ctk.NORMAL)
            Currently = "start"
        else:
            for i in range(matrix_size):
                for j in range(matrix_size):
                    button_matrix[i][j].configure(state=ctk.DISABLED)
            
            button.route.append([button.row,button.col])
            myQ.append([button,button.route])
            result =  BFS(myQ)
            print("the result is:",result)
            canvas.after(1000, lambda: routeFound(result))
            

         
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

window = ctk.CTk()
window.geometry("900x800")
window.title('Shortest Path Finder ~(BFS)~')

label = ctk.CTkLabel(window, text='Shortest Path Finder', text_color="white", width=200, pady=50, font=("Ariel", 48))
label.pack()

canvas = ctk.CTkFrame(master=window, width=canvas_size, height=canvas_size, border_width=5, fg_color="lightgray")
canvas.pack(side=ctk.LEFT, padx=30)

button_matrix = create_matrix_buttons(canvas, matrix_size,Play)

buttonFrame = ctk.CTkFrame(master=window)
buttonFrame.pack(side=ctk.LEFT, padx=30,pady=100)

start = ctk.CTkButton(buttonFrame, text="Start Position", command=startClick, width=150, height=50, state=ctk.DISABLED,fg_color="#FF0000",text_color="black")
start.pack(pady=10)

end = ctk.CTkButton(buttonFrame, text="End Position", command=endClick, width=150, height=50,fg_color="#27DDF2",text_color="black")
end.pack(pady=10)

buildWall = ctk.CTkButton(buttonFrame, text="Build Wall", command=WallClick, width=150, height=50,fg_color="#844403",text_color="black")
buildWall.pack(pady=10)

algo = ctk.CTkButton(buttonFrame, text="Start Algoritm", command=algoClick, width=150, height=50,text_color="black")
algo.pack(pady=10)

window.mainloop()
