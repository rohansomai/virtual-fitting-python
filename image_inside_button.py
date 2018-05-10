import tkinter
root = tkinter.Tk()
def sel():
    pass
b = tkinter.Button(root, text = "button2", command = sel)
b.pack()
canvas = tkinter.Canvas(b, height = 25, width = 25)
canvas.grid(row = 0, column = 0)
photo = tkinter.PhotoImage(file = '2.png')
canvas.create_image(0, 0, image=photo)
root.mainloop()