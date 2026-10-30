"""visual_demo.py —— 排序过程可视化（冒泡 / 插入）

功能：
    1. 开始前输入待排序数字（直接回车则随机生成，长度可指定）
    2. 选择排序算法（冒泡 / 插入）
    3. 可设置加速倍数；演示中按 S 键在原速与加速之间切换，进度保留
    4. 界面实时显示比较/交换次数与用时；中途关窗也会在终端输出统计

运行：python src/visual_demo.py
依赖：仅标准库 turtle；同目录需有 bubble_steps.py 和 insertion_steps.py
"""

import random
import time
import turtle
from bubble_steps import bubble_sort_steps
from insertion_steps import insertion_steps

# ---------- 可调参数 ----------
RANDOM_N = 20          # 随机生成时的默认柱子数量（可由用户输入覆盖）
DELAY = 0.06           # 原始速度下每步间隔秒数，越小越快
HEIGHT_POWER = 1.5     # 高度映射指数：大于 1 会拉大柱子的高度差
BG      = "#1e1e2e"    # 背景
BAR     = "#89b4fa"    # 普通柱子
COMPARE = "#f9e2af"    # 正在比较
SWAP    = "#f38ba8"    # 正在交换
SORTED  = "#a6e3a1"    # 排序完成

# 算法编号 -> (算法名, 对应的步骤生成器函数)
ALGORITHMS = {
    "1": ("冒泡排序", bubble_sort_steps),
    "2": ("插入排序", insertion_steps),
}


def get_data():
    """读取用户输入的数组；直接回车则随机生成（长度同样由用户决定）。"""
    s = input("请输入待排序数字（空格分隔），直接回车则随机生成：").strip()
    if s:
        try:
            data = [int(x) for x in s.split()]
            if data:
                return data
        except ValueError:
            print("输入格式不正确，改为随机生成。")
    # 随机生成：询问数组长度
    n = RANDOM_N
    s = input(f"随机生成的数组长度（直接回车默认 {RANDOM_N}）：").strip()
    if s:
        try:
            if int(s) > 0:
                n = int(s)
            else:
                print("长度需为正整数，已使用默认值。")
        except ValueError:
            print("长度格式不正确，已使用默认值。")
    return [random.randint(1, 100) for _ in range(n)]


def get_algorithm():
    """让用户选择排序算法，返回 (算法名, 步骤生成器函数)。"""
    print("请选择排序算法：1 = 冒泡排序，2 = 插入排序")
    choice = input("输入编号（直接回车默认 1）：").strip() or "1"
    return ALGORITHMS.get(choice, ALGORITHMS["1"])


def get_fast_factor():
    """读取加速模式的倍数，默认 4 倍。原始速度始终保留，可按键切换。"""
    s = input("加速模式的倍数（直接回车默认 4 倍）：").strip()
    if not s:
        return 4.0
    try:
        f = float(s)
        if f > 0:
            return f
    except ValueError:
        pass
    print("倍数格式不正确，使用默认 4 倍。")
    return 4.0


# ---------- 主流程：先拿到输入，再开窗口 ----------
data = get_data()
algo_name, step_generator = get_algorithm()
n = len(data)

speed = {"fast": get_fast_factor(), "current": 1.0}   # current 是当前实际倍数

# ---------- 画布 ----------
screen = turtle.Screen()
screen.setup(900, 600)
screen.bgcolor(BG)
screen.title(f"SortViz · {algo_name}")
screen.tracer(0)               # 关闭自动刷新，动画更流畅

pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)
pen.penup()

# ---------- 布局（按实际元素个数 n 计算）----------
MARGIN = 60
LEFT = -450 + MARGIN           # 最左柱子的 x
BASE = -220                    # 柱子底边的 y
MAX_H = 420                    # 最高柱子的高度
GAP = (900 - 2 * MARGIN) / n   # 每根柱子占的宽度（含间距）
BAR_W = GAP * 0.8              # 柱子实际宽度


def toggle_speed():
    """在原速(1倍)与加速倍数之间切换。只改速度，不影响排序进度。"""
    speed["current"] = 1.0 if speed["current"] != 1.0 else speed["fast"]


screen.listen()                # 让窗口接收键盘事件
screen.onkey(toggle_speed, "s")
screen.onkey(toggle_speed, "S")


def draw(a, highlight=(), color=BAR, compare=0, swap=0, elapsed=0.0):
    """把数组 a 画成一帧：highlight 中的下标用 color 高亮。"""
    pen.clear()
    lo, hi = min(a), max(a)
    span = max(hi - lo, 1)     # 归一化，避免全相等时除零
    for i, v in enumerate(a):
        x = LEFT + i * GAP
        # 用指数映射夸大高度差：让矮柱子更矮、高柱子更突出
        ratio = (v - lo) / span
        h = ratio ** HEIGHT_POWER * (MAX_H - 10) + 10   # 最小高度 10
        pen.goto(x, BASE)
        pen.fillcolor(color if i in highlight else BAR)
        pen.begin_fill()
        for dx, dy in ((BAR_W, 0), (0, h), (-BAR_W, 0), (0, -h)):
            pen.goto(pen.xcor() + dx, pen.ycor() + dy)
        pen.end_fill()
    # 顶部：实时统计（次数、用时、当前速度）
    pen.goto(0, 245)
    pen.color("white")
    pen.write(f"比较 {compare} 次   交换 {swap} 次   "
              f"演示计时 {elapsed:.1f} 秒   速度 x{speed['current']:g}",
              align="center", font=("微软雅黑", 16, "normal"))
    # 底部：操作提示
    pen.goto(0, -275)
    pen.color("#a6adc8")
    pen.write("按 S 切换速度（先点击窗口获得焦点）｜关闭窗口结束演示",
              align="center", font=("微软雅黑", 11, "normal"))
    screen.update()


# ---------- 逐步回放事件，驱动动画 ----------
a = list(data)
compare = swap = 0
completed = False              # 是否完整演示到结束
draw(a)
time.sleep(0.8)                # 开场停一下，看清初始状态

start = time.perf_counter()    # 真实计时起点
last_tick = start              # 上一次结算演示计时的时刻
sim_time = 0.0                 # 演示计时：真实间隔 × 当前倍数的累计
try:
    batch = 0                  # 自上次画帧以来累积的事件数
    for event in step_generator(data):
        kind = event[0]
        # 先处理事件本身：更新数据与计数（这部分不受速度影响）
        if kind == "compare":
            compare += 1
            hi, color = (event[1], event[2]), COMPARE
        elif kind == "swap":
            swap += 1
            i, j = event[1], event[2]
            a[i], a[j] = a[j], a[i]
            hi, color = (i, j), SWAP
        else:                  # "done"：整体染绿
            completed = True
            hi, color = tuple(range(n)), SORTED
        # 原速时每个事件画一帧；加速时合并多个事件画一帧，
        # 减少画图次数，总用时才会真正按比例缩短
        batch += 1
        if kind == "done" or batch >= max(1, round(speed["current"])):
            batch = 0
            now = time.perf_counter()
            # 演示计时按当前倍数推进：原速走 1 秒/秒，N 倍速走 N 秒/秒
            sim_time += (now - last_tick) * speed["current"]
            last_tick = now
            draw(a, hi, color, compare, swap, sim_time)
            time.sleep(DELAY / speed["current"])
    screen.mainloop()          # 演示完成后保持窗口打开
except turtle.Terminator:
    pass                       # 用户中途关闭窗口：不报错，走 finally 输出统计
finally:
    real_elapsed = time.perf_counter() - start
    status = "演示完成" if completed else "中途退出"
    print(f"{algo_name}（{status}）：比较 {compare} 次，交换 {swap} 次，"
          f"演示计时 {sim_time:.2f} 秒，真实用时 {real_elapsed:.2f} 秒")
