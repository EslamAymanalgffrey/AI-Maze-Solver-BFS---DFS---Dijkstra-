"""
واجهة المستخدم
"""

import tkinter as tk
from tkinter import messagebox
import time

from algorithms import bfs, dfs, dijkstra, reconstruct_path
from utils import generate_random_maze, random_open_pair, format_time

ROWS = 20
COLS = 25
CELL = 28

COLORS = {
    'empty': '#1E2D45',
    'wall': '#2D3436',
    'start': '#00B894',
    'goal': '#E94560',
    'visited': '#2C4A7C',
    'path': '#FDCB6E',
    'grid_line': '#0D1B2A',
}


class MazeSolverGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Maze Solver")

        self.grid = [['empty'] * COLS for _ in range(ROWS)]
        self.start = None
        self.goal = None

        self.mode = tk.StringVar(value='wall')

        self._build_ui()
        self._init_canvas()

    def _build_ui(self):
        frame = tk.Frame(self.root)
        frame.pack()

        self.canvas = tk.Canvas(
            frame,
            width=COLS * CELL,
            height=ROWS * CELL,
            bg=COLORS['grid_line']
        )
        self.canvas.pack(side='left')

        panel = tk.Frame(frame)
        panel.pack(side='left', padx=10)

        # أزرار الرسم
        for text, mode in [
            ('Start', 'start'),
            ('Goal', 'goal'),
            ('Wall', 'wall'),
            ('Erase', 'erase')
        ]:
            tk.Radiobutton(panel, text=text, variable=self.mode, value=mode).pack(anchor='w')

        tk.Button(panel, text="Random", command=self._random).pack(fill='x')
        tk.Button(panel, text="Reset", command=self._reset).pack(fill='x')

        tk.Button(panel, text="BFS", command=lambda: self._run(bfs)).pack(fill='x')
        tk.Button(panel, text="DFS", command=lambda: self._run(dfs)).pack(fill='x')
        tk.Button(panel, text="Dijkstra", command=lambda: self._run(dijkstra)).pack(fill='x')

        self.canvas.bind("<Button-1>", self._click)
        self.canvas.bind("<B1-Motion>", self._drag)

    def _init_canvas(self):
        self.rects = {}
        for r in range(ROWS):
            for c in range(COLS):
                x1, y1 = c * CELL, r * CELL
                rect = self.canvas.create_rectangle(
                    x1, y1, x1 + CELL, y1 + CELL,
                    fill=COLORS['empty'],
                    outline='black'
                )
                self.rects[(r, c)] = rect

    def _paint(self, r, c, t):
        self.canvas.itemconfig(self.rects[(r, c)], fill=COLORS[t])

    def _click(self, event):
        r = event.y // CELL
        c = event.x // CELL
        self._apply(r, c)

    def _drag(self, event):
        r = event.y // CELL
        c = event.x // CELL
        if self.mode.get() in ['wall', 'erase']:
            self._apply(r, c)

    def _apply(self, r, c):
        if not (0 <= r < ROWS and 0 <= c < COLS):
            return

        mode = self.mode.get()

        if mode == 'start':
            self.start = (r, c)
            self._paint(r, c, 'start')

        elif mode == 'goal':
            self.goal = (r, c)
            self._paint(r, c, 'goal')

        elif mode == 'wall':
            self.grid[r][c] = 'wall'
            self._paint(r, c, 'wall')

        elif mode == 'erase':
            self.grid[r][c] = 'empty'
            self._paint(r, c, 'empty')

    def _random(self):
        self.grid = generate_random_maze(ROWS, COLS)
        self.start, self.goal = random_open_pair(self.grid, ROWS, COLS)
        self._draw()

    def _reset(self):
        self.grid = [['empty'] * COLS for _ in range(ROWS)]
        self.start = None
        self.goal = None
        self._draw()

    def _draw(self):
        for r in range(ROWS):
            for c in range(COLS):
                self._paint(r, c, self.grid[r][c])

        if self.start:
            self._paint(*self.start, 'start')
        if self.goal:
            self._paint(*self.goal, 'goal')

    def _run(self, algo):
        if not self.start or not self.goal:
            messagebox.showwarning("Error", "حدد start و goal")
            return

        t0 = time.perf_counter()
        order, parent = algo(self.grid, self.start, self.goal, ROWS, COLS)
        path = reconstruct_path(parent, self.start, self.goal)
        print("Time:", format_time(time.perf_counter() - t0))

        self._animate(order, path, 0)

    def _animate(self, order, path, i):
        if i < len(order):
            r, c = order[i]
            if (r, c) != self.start and (r, c) != self.goal:
                self._paint(r, c, 'visited')

            self.root.after(10, lambda: self._animate(order, path, i + 1))
        else:
            for r, c in path:
                if (r, c) != self.start and (r, c) != self.goal:
                    self._paint(r, c, 'path')