"""bubble_steps.py —— 冒泡排序步骤生成器

把排序过程拆成一步步的"事件"，由调用方（测试或动画）逐步消费：
    ("compare", i, j)  正在比较 a[i] 和 a[j]
    ("swap",    i, j)  交换了 a[i] 和 a[j]
    ("done",)          排序完成，a 已升序
"""


def bubble_sort_steps(arr):
    """返回一个生成器，逐步 yield 冒泡排序的每个事件。

    注意：不修改传入的 arr，内部使用副本。
    """
    a = list(arr)          # 复制一份，保护原始数据
    n = len(a)
    # 每轮把最大值"冒泡"到区间末尾，区间从右往左收缩
    for end in range(n - 1, 0, -1):      # end = n-1, n-2, ..., 1
        for i in range(end):
            j = i + 1
            yield ("compare", i, j)      # 先记录"比较"事件
            if a[i] > a[j]:
                a[i], a[j] = a[j], a[i]  # 需要交换时先交换
                yield ("swap", i, j)     # 再记录"交换"事件
    yield ("done",)
