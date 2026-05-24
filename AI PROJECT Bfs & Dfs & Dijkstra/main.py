"""
main.py
=======
نقطة تشغيل البرنامج
"""

import tkinter as tk
from gui import MazeSolverGUI


def main():
    root = tk.Tk()
    app = MazeSolverGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()