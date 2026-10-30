"""test_sorts.py —— 排序步骤生成器的测试

运行：python tests/test_sorts.py
思路：回放生成器 yield 的事件，逐步执行 swap，最终结果必须与内置 sorted() 一致。
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from bubble_steps import bubble_sort_steps
from insertion_steps import insertion_steps

GENERATORS = [bubble_sort_steps, insertion_steps]


def replay(step_generator, case):
    """回放事件序列，返回 (排序结果, 比较次数, 交换次数)。"""
    a = list(case)
    compare = swap = 0
    saw_done = False
    for event in step_generator:
        kind = event[0]
        if kind == "compare":
            compare += 1
        elif kind == "swap":
            swap += 1
            a[event[1]], a[event[2]] = a[event[2]], a[event[1]]
        elif kind == "done":
            saw_done = True
    assert saw_done, "生成器没有 yield ('done',)"
    return a, compare, swap


CASES = [
    [],
    [1],
    [2, 1],
    [3, 3],
    [1, 2, 3],
    [5, 4, 3, 2, 1],
    [5, 3, 8, 1, 2],
    [4, -1, 0, 4, 2],
]


def test_correctness():
    for gen in GENERATORS:
        for case in CASES:
            result, _, _ = replay(gen(case), case)
            assert result == sorted(case), \
                f"{gen.__name__} 排序错误: {case} -> {result}"
    print("正确性测试通过（冒泡 + 插入，含空表、单元素、重复、逆序、负数等边界）")


def test_bubble_compare_count():
    # 冒泡排序的比较次数与数据无关：n 个元素固定为 n(n-1)/2
    for n in range(0, 8):
        case = list(range(n, 0, -1))
        _, compare, _ = replay(bubble_sort_steps(case), case)
        expected = n * (n - 1) // 2
        assert compare == expected, f"n={n} 比较次数应为 {expected}，实际 {compare}"
    print("冒泡比较次数测试通过：与理论值 n(n-1)/2 一致")


def test_no_modify_input():
    for gen in GENERATORS:
        case = [3, 1, 2]
        list(gen(case))
        assert case == [3, 1, 2], f"{gen.__name__} 不应修改传入的列表"
    print("输入保护测试通过（两种算法均不修改原列表）")


if __name__ == "__main__":
    test_correctness()
    test_bubble_compare_count()
    test_no_modify_input()
    print("全部测试通过")
