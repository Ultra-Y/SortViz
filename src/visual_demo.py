"""visual_demo.py —— 冒泡排序动画（turtle 美化版）

运行：python src/visual_demo.py
依赖：仅标准库 turtle；需同目录下有 bubble_steps.py
"""

import random
import time
import turtle
from bubble_steps import bubble_sort_steps

# ---------- 可调参数 ----------
N = 20                 # 柱子数量
DELAY = 0.06           # 每步间隔秒数，越小越快
BG      = "#1e1e2e"    # 背景
BAR     = "#89b4fa"    # 普通柱子
COMPARE = "#f9e2af"    # 正在比较
SWAP    = "#f38ba8"    # 正在交换
SORTED  = "#a6e3a1"    # 排序完成

# ---------- 画布 ----------
screen = turtle.Screen()
screen.setup(900, 600)
screen.bgcolor(BG)
screen.title("SortViz · 冒泡排序")
screen.tracer(0)               # 关闭自动刷新，动画更流畅

pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)
pen.penup()

# ---------- 布局 ----------
MARGIN = 60
LEFT = -450 + MARGIN           # 最左柱子的 x
BASE = -220                    # 柱子底边的 y
MAX_H = 380                    # 最高柱子的高度
GAP = (900 - 2 * MARGIN) / N   # 每根柱子占的宽度（含间距）
BAR_W = GAP * 0.8              # 柱子实际宽度

def draw(a, highlight=(), color=BAR, compare=0, swap=0):
    """把数组 a 画成一帧：highlight 中的下标用 color 高亮。"""
    pen.clear()
    lo, hi = min(a), max(a)
    span = max(hi - lo, 1)     # 归一化，避免全相等时除零
    for i, v in enumerate(a):
        x = LEFT + i * GAP
        h = (v - lo) / span * (MAX_H - 40) + 40   # 最小高度 40
        pen.goto(x, BASE)
        pen.fillcolor(color if i in highlight else BAR)
        pen.begin_fill()
        for dx, dy in ((BAR_W, 0), (0, h), (-BAR_W, 0), (0, -h)):
            pen.goto(pen.xcor() + dx, pen.ycor() + dy)
        pen.end_fill()
    pen.goto(0, 245)           # 顶部统计文字
    pen.color("white")
    pen.write(f"比较 {compare} 次     交换 {swap} 次",
              align="center", font=("微软雅黑", 16, "normal"))
    screen.update()

# ---------- 主流程：生成数据 → 逐步回放事件 ----------
data = [random.randint(1, 100) for _ in range(N)]
a = list(data)
compare = swap = 0
draw(a)
time.sleep(0.8)                # 开场停一下，让人看清初始状态

for event in bubble_sort_steps(data):
    kind = event[0]
    if kind == "compare":
        compare += 1
        draw(a, (event[1], event[2]), COMPARE, compare, swap)
    elif kind == "swap":
        swap += 1
        i, j = event[1], event[2]
        a[i], a[j] = a[j], a[i]
        draw(a, (i, j), SWAP, compare, swap)
    else:                      # "done"：整体染绿
        draw(a, tuple(range(N)), SORTED, compare, swap)
    time.sleep(DELAY)

screen.mainloop()              # 保持窗口打开
