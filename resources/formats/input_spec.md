# XTB 输入格式规范

xtb 程序主要通过一个名为 `.xcontrolrc` (或用户自定义名称) 的控制文件来读取计算参数，并通过一个坐标文件 (通常是 `.xyz` 格式) 来读取分子结构。

## 1. 分子结构文件

xtb 支持多种常见的分子结构格式，最常用的是 XYZ 格式。

### XYZ 格式 (`.xyz`)
- **第一行**: 原子总数 (整数)。
- **第二行**: 注释行 (通常为空或包含能量等信息)。
- **后续行**: 每行一个原子，格式为 `元素符号 X坐标 Y坐标 Z坐标`。坐标单位通常为埃 (Å)。

**示例 (`molecule.xyz`):**
```xyz
3
Water molecule
O  0.000000  0.000000  0.117300
H  0.000000  0.757200 -0.469200
H  0.000000 -0.757200 -0.469200
```

### 其他支持的格式
xtb 也可以通过 Open Babel (如果已安装并集成) 间接支持其他格式，如:
- **COORD (TURBOMOLE)**: 通常命名为 `coord`。
- **Gaussian Input (`.gjf`, `.com`)**: 可以从中提取结构。
- **VASP (`POSCAR`, `CONTCAR`)**: 用于周期性体系。

**注意**: 结构文件通常通过命令行参数传递给 `xtb` 程序，例如 `xtb molecule.xyz --input .xcontrolrc`。

## 2. 控制文件 (`.xcontrolrc` 或自定义)

控制文件包含了 xtb 计算的所有参数和设置。它采用一种特定的块状结构。

### 基本语法:
- 以 `$` 开头的行表示一个参数块的开始或一个独立的参数。
- 参数块以 `$blockname` 开始，以 `$end` 结束 (对于某些简单块，`$end` 可能省略)。
- 参数名和参数值之间用 `=` 或空格分隔。
- `#` 开头的行为注释行。

**示例 (`.xcontrolrc`):**
```
# .xcontrolrc example for GFN2-xTB optimization

$gfn 2                # 使用 GFN2-xTB 方法
$chrg 0               # 分子总电荷为 0
$spin 0               # 未配对电子数为 0 (单重态)
$alpb h2o             # 使用 GBSA 水溶剂模型

$opt                  # 几何优化参数块
  level=normal        # 优化级别
  maxcycle=300        # 最大优化步数
$end                  # 结束 $opt 块

$scc                  # SCC (自洽电荷) 参数块
  temp=298.15         # 电子温度 (K)
  etol=1.d-8          # 能量收敛阈值
$end                  # 结束 $scc 块

$write                # 输出控制块
  json=true           # 输出 JSON 格式的 xtb结果
  wiberg=true         # 计算并输出 Wiberg 键级
$end                  # 结束 $write 块
```

### 常用参数块:
- `$gfn`: 指定 GFN 方法版本 (0, 1, 2)。
- `$chrg`: 分子电荷。
- `$spin`: 未配对电子数。
- `$alpb`: 隐式溶剂模型。
- `$scc`: 自洽电荷计算参数。
- `$opt`: 几何优化参数。
- `$hess`: Hessian (频率) 计算参数。
- `$scan`: 约束扫描参数。
- `$md`: 分子动力学参数。
- `$constrain`: 几何约束。
- `$write`: 输出控制。
- `$metadyn`: 元动力学参数。
- `$oniom`: ONIOM 计算参数。
- `$embedding`: QM/MM 嵌入计算参数。
- `$stm`: STM 模拟参数。
- `$cube`: 立方文件输出参数。

## 3. 其他输入文件 (可选)

根据计算类型，可能还需要其他输入文件：

- **`constraints.inp`**: 如果在 `.xcontrolrc` 中通过 `$constrain file=constraints.inp` 指定，则包含几何约束定义。
- **`scan.inp`**: 如果在 `.xcontrolrc` 中通过 `$scan file=scan.inp` 指定，则包含扫描坐标定义。
- **`restart` 文件**: 用于从之前的计算中重启，通常由 xtb 自动生成和读取。

## 4. 命令行参数

xtb 程序本身也接受许多命令行参数，这些参数可以覆盖或补充控制文件中的设置。
例如:
- `--input <file>`: 指定控制文件名。
- `--chrg <int>`: 设置电荷。
- `--uhf <int>`: 设置未配对电子数 (等同于 `$spin`)。
- `--opt`: 执行几何优化。
- `--hess`: 执行 Hessian 计算。
- `--gbsa <solvent>`: 使用 GBSA 溶剂模型。
- `--gfn <version>`: 指定 GFN 版本。

建议将主要参数放在控制文件中，以保持清晰和可重复性。

详细的参数和文件格式说明，请务必参考最新的 xtb 官方文档。