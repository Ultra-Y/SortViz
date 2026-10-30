# SortViz —— 排序过程可视化

用 Python 标准库 turtle 动画演示常见排序算法的执行过程，帮助初学者直观理解每一步的比较与交换。

## 项目背景与目标

教材中的排序算法通常只有静态插图，初学者难以直观感受"比较"和"交换"发生的时机。SortViz 把排序过程拆成一步步事件并动画展示，同时统计比较/交换次数，便于与理论复杂度对照。

## 功能

- [x] 冒泡排序步骤生成器（核心逻辑与界面分离，可独立测试）
- [x] 冒泡排序动画演示（高亮比较/交换、实时统计次数、配色与调速）
- [x] 插入排序
- [ ] 选择排序
- [ ] 多算法对比展示

## 环境与运行

- Python 3.10+，仅使用标准库，无第三方依赖
- 需要本机图形界面（turtle 会弹出窗口）

```bash
python src/visual_demo.py      # 动画演示冒泡排序
python tests/test_sorts.py     # 运行测试
```

## 目录结构

```text
SortViz/
├── src/                 # 源代码：排序步骤生成器 + turtle 动画
├── tests/               # 测试脚本（对照 sorted()、边界用例、次数校验）
├── examples/            # 示例输入与预期输出
├── docs/                # 截图与演示材料
└── README.md
```

## 核心设计：步骤生成器

每种排序实现为一个生成器函数，逐条 yield `("compare", i, j)`、`("swap", i, j)`、`("done",)` 事件。测试层回放事件验证正确性，动画层把事件翻译成画面——核心逻辑与界面完全分离。

## 课程知识与分析
插入排序已解决：
原理：
def insertion_steps(arr):
    sort = []
    for item in arr:
        pos = len(sort)
        for i in range(len(sort)):
            if sort[i] > item:
                pos = i
                break
        sort.insert(pos, item)
    return sort
演示程序：
def insertion_sort_steps(arr):
    a = list(arr)                     # 复制输入，保护原列表
    n = len(a)
    for j in range(n):
        while j > 0:
            yield ("compare", j - 1, j)     # 传下标，不传值
            if a[j - 1] > a[j]:
                a[j - 1], a[j] = a[j], a[j - 1]
                yield ("swap", j - 1, j)    # 传下标，不传值
                j = j - 1
            else:
                break
    yield ("done",)
（待补充：冒泡/插入/选择排序的比较次数分析，n(n-1)/2 与实测对照，选型理由）

## 测试与结果

（待补充：对照内置 sorted() 的验证方法、边界用例表、实际运行结果）

## 局限与改进

（待补充）

## AI 使用声明

- 使用工具：Qoder 智能体
- 参与环节：冒泡排序步骤生成器与 turtle 动画的示例代码由 AI 提供；后续算法的实现与修改由本人完成
- 本人完成的设计、修改与判断：（待补充）
- 验证方法及结果：回放事件与内置 sorted() 对照、边界用例测试、比较次数与理论值 n(n-1)/2 校验
- 代表性协作案例：（待补充，提交前脱敏）

## 许可证

MIT License，见 LICENSE 文件。

##功能增加
10.30 
-增加了插入排序，在终端打开可以从冒泡和插入选择其一作为排序依据
-增加了计时器，方便看用时
-增加了输入功能，可以手动输入数据，演示时可不依靠内部数据
-增加了加速功能，方便在输入大数组时节省时间
-优化了柱子的高度，现在柱子之间的高度差更大，对比效果更强
