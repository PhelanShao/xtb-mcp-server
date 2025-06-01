# GFN1-xTB 参数说明

GFN1-xTB (简写为 GFN-xTB) 是 xtb 程序中早于 GFN2-xTB 的一个半经验紧束缚方法版本。它相对于 GFN0-xTB 在精度上有所改进，特别是在几何结构和能量方面，并且包含了 D3 色散校正。

## 主要特点:
- **平衡性**: 在计算速度和精度之间提供了一个较好的平衡，优于 GFN0-xTB，但通常不如 GFN2-xTB 精确。
- **元素覆盖**: 支持周期表中 H 到 Rn (Z=86) 的元素。
- **色散校正**: 包含 D3(BJ) 色散校正，用于描述非共价相互作用，但其效果通常不如 GFN2-xTB 中的 D4 校正。
- **溶剂化模型**: 支持 GBSA (Generalized Born with Surface Area) 隐式溶剂化模型。
- **用途**:
    - 当 GFN2-xTB 计算成本过高，但 GFN0-xTB 精度不足时的折中选择。
    - 某些特定体系或与旧研究对比时可能需要。
    - 分子动力学模拟。

## 常用参数块:

### `$gfn`
用于指定 GFN 方法的版本。
```
$gfn 1  # 或者 $gfn gfn1
```

### `$chrg`
定义体系的总电荷。
```
$chrg 0
```

### `$spin` (或 `$uhf`)
定义体系的未配对电子数。
```
$spin 0
```

### `$alpb`
选择隐式溶剂模型和溶剂。
```
$alpb h2o     # 使用 GBSA 水模型
$alpb toluene # 使用 GBSA 甲苯模型
```
GFN1-xTB 支持的溶剂与 GFN2-xTB 类似。

### `$scc`
控制自洽电荷计算的参数。
```
$scc
  temp=300.0  # 电子温度 (K)
  maxiter=200 # 最大迭代次数
  etol=1.d-7  # 能量收敛阈值
$end
```

### `$opt`
用于几何优化计算。
```
$opt
  level=normal  # 优化级别 (crude, sloppy, normal, tight, vtight, extreme)
  maxcycle=200  # 最大优化步数
$end
```

### `$hess`
用于频率 (Hessian) 计算。结果的可靠性介于 GFN0 和 GFN2 之间。
```
$hess
  temp=298.15   # 计算热化学数据的温度 (K)
$end
```

## 使用建议:
- **作为 GFN2 的替代**: 如果 GFN2-xTB 计算过于耗时，可以考虑使用 GFN1-xTB。
- **非共价相互作用**: D3 色散校正使其能够处理非共价相互作用，但精度可能不如 GFN2-xTB 的 D4 校正。
- **与 GFN2 比较**: 在关键计算中，如果使用了 GFN1-xTB，建议与 GFN2-xTB 的结果进行比较以评估其可靠性。
- **分子动力学**: GFN1-xTB 曾是 xtb 中进行分子动力学模拟的常用方法，直到 GFN2-xTB 出现并提供了更好的性能。

虽然 GFN2-xTB 是目前推荐的默认方法，但 GFN1-xTB 在某些特定情况下仍有其应用价值。
更多详细信息和高级参数，请参考官方 xtb 文档。