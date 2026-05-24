import random


def generate_random_maze(rows, cols):
    return [
        ['wall' if random.random() < 0.3 else 'empty' for _ in range(cols)]
        for _ in range(rows)
    ]


def random_open_pair(grid, rows, cols):
    cells = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 'empty']
    if len(cells) < 2:
        return None, None

    s = random.choice(cells)
    g = random.choice(cells)

    while g == s:
        g = random.choice(cells)

    return s, g


def format_time(t):
    return f"{t*1000:.2f} ms"