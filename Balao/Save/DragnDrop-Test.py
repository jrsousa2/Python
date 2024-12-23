# USADO APENAS PARA TESTAR SE DRAG AND DROP TAVA FUNCIONANDO

import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES

def on_drop(event):
    print(f"Dropped file: {event.data}")

root = TkinterDnD.Tk()

root.title("Drag and Drop Test")
root.geometry("400x300")

label = tk.Label(root, text="Drag and drop a file here", width=40, height=10, relief="solid")
label.pack(padx=10, pady=10)

label.drop_target_register(DND_FILES)
label.dnd_bind('<<Drop>>', on_drop)

root.mainloop()
