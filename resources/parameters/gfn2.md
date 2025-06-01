# GFN2-xTB 参数说明

GFN2-xTB 是 xtb 程序中默认且推荐的半经验紧束缚方法。它在 GFN1-xTB 的基础上进行了改进，提供了对各种化学体系更准确的描述，特别是在非共价相互作用、几何结构和振动频率方面。

## 主要特点:
- **准确性**: 相对于 GFN1-xTB，在几何、能量和频率计算方面有显著提升。
- **适用性**: 广泛适用于包含周期表中 H 到 Rn (Z=86) 元素的大多数有机和无机分子。
- **色散校正**: 包含 D4 色散校正，以准确描述非共价相互作用。
- **溶剂化模型**: 支持 GBSA (Generalized Born with Surface Area) 隐式溶剂化模型。

## 常用参数块:

### `$gfn`
用于指定 GFN 方法的版本。
```
$gfn 2  # 或者 $gfn gfn2
```
这是使用 GFN2-xTB 的基本指令。

### `$chrg`
定义体系的总电荷。
```
$chrg 0  # 中性体系
$chrg +1 # 阳离子
$chrg -1 # 阴离子
```

### `$spin`
定义体系的自旋多重度 (2S+1)。对于闭壳层体系，通常为单重态 (spin=0 for UHF, or not specified for RHF-like calculations if it's the default). xtb 内部通常处理为未配对电子数。
```
$spin 0  # 单重态 (0 个未配对电子)
$spin 1  # 双重态 (1 个未配对电子)
$spin 2  # 三重态 (2 个未配对电子)
```
**注意**: `xtb` 使用的是未配对电子数，而不是严格意义上的 (2S+1)。

### `$alpb`
选择隐式溶剂模型和溶剂。
```
$alpb h2o     # 使用 GBSA 水模型
$alpb toluene # 使用 GBSA 甲苯模型
$alpb none    # 气相计算 (默认)
```
可用的溶剂列表可以在 xtb 文档中找到。

### `$scc`
控制自洽电荷 (Self-Consistent Charge) 计算的参数。
```
$scc
  temp=300.0  # 电子温度 (K)
  maxiter=250 # 最大迭代次数
  etol=1.d-7  # 能量收敛阈值 (Hartree)
$end
```

### `$opt`
用于几何优化计算。
```
$opt
  level=normal  # 优化级别 (crude, sloppy, normal, tight, vtight, extreme)
  maxcycle=200  # 最大优化步数
  engine=lbfgs  # 优化算法 (lbfgs, rf, fire)
$end
```

### `$hess`
用于频率 (Hessian) 计算。
```
$hess
  temp=298.15   # 计算热化学数据的温度 (K)
  pressure=1.0  # 计算热化学数据的压力 (atm)
$end
```

## 使用建议:
- 对于大多数常规计算，GFN2-xTB 是首选方法。
- 确保正确设置电荷和自旋多重度。
- 对于涉及非共价相互作用的体系，GFN2-xTB 通常能给出合理结果。
- 在进行频率计算前，务必先进行几何优化。

更多详细信息和高级参数，请参考官方 xtb 文档。