import tkinter as tk
from tkinter import ttk
root = tk.Tk()
#root.withdraw()
cb = ttk.Combobox(root, name='mycombo', values=('alpha', 'beta'))
cb.pack()
def here(event): print(event.widget)
cb.bind('<<ComboboxSelected>>', here)
cb.set('none')
root.update()
cb.event_generate('<Button-1>')
root.update()
cb.event_generate('<Key-Down>')
root.update()
cb.event_generate('<Key-Return>')
root.update()
cb.event_generate('<<ComboboxSelected>>')
root.update()