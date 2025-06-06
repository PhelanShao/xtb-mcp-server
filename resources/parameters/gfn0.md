# GFN0-xTB 参数说明

GFN0-xTB 是一种较早版本的半经验紧束缚方法，主要用于快速的初步计算或作为更精确方法（如 GFN2-xTB）的预优化步骤。它通常计算速度非常快，但精度相对较低，尤其是在描述非共价相互作用和某些特定化学体系时。

## 主要特点:
- **速度**: 计算成本极低，适用于非常大的分子体系或高通量筛选。
- **元素覆盖**: 支持周期表中 H 到 Rn (Z=86) 的元素。
- **精度**: 相对于 GFN1-xTB 和 GFN2-xTB，精度较低。不包含色散校正，因此对非共价相互作用的描述较差。
- **用途**:
    - 初步的几何预优化。
    - 快速筛选大量化合物。
    - 作为更高级计算的起点。
    - 教学或快速演示。

## 常用参数块:

### `$gfn`
用于指定 GFN 方法的版本。
```
$gfn 0  # 或者 $gfn gfn0
```

### `$chrg`
定义体系的总电荷。
```
$chrg 0  # 中性体系
```

### `$spin` (或 `$uhf`)
定义体系的未配对电子数。
```
$spin 0  # 单重态 (0 个未配对电子)
```

### `$alpb`
GFN0-xTB **不直接支持** GBSA 等隐式溶剂模型。溶剂化效应通常不包含在该方法中。如果需要溶剂效应，应考虑 GFN1 或 GFN2。
如果错误地使用了 `$alpb`，xtb 可能会忽略它或给出警告/错误。

### `$scc`
控制自洽电荷计算的参数。
```
$scc
  temp=300.0  # 电子温度 (K)
  maxiter=100 # 最大迭代次数 (GFN0 通常收敛更快)
  etol=1.d-6  # 能量收敛阈值
$end
```

### `$opt`
用于几何优化计算。
```
$opt
  level=crude   # GFN0 通常用于粗略优化，更高级别可能意义不大
  maxcycle=100  # 最大优化步数
$end
```

### `$hess`
GFN0-xTB 可以计算 Hessian 矩阵以获得振动频率，但其精度有限，不推荐用于精确的热化学数据分析。
```
$hess
  # temp 和 pressure 参数与 GFN2 类似，但结果可靠性较低
$end
```

## 使用建议:
- **谨慎使用**: GFN0-xTB 的精度有限，不应作为最终结果的唯一依据，除非计算资源极其受限或仅需粗略估计。
- **预优化**: 是一个很好的预优化工具，可以为 GFN2-xTB 或 DFT 计算提供一个合理的初始结构。
- **避免用于非共价相互作用**: 由于缺乏色散校正，不适用于研究范德华斯复合物、氢键主导的体系等。
- **检查输出**: 仔细检查 GFN0-xTB 的输出，特别是几何结构和能量，确保其物理化学合理性。

更多详细信息，请参考 xtb 官方文档，特别是关于不同 GFN 方法版本比较的部分。