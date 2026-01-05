import tkinter as tk
from ui import TaskManagerUI

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerUI(root)
    root.mainloop()
