# XTB MCP 服务器 - 常见问题解答 (FAQ)

## 1. 一般问题

**Q: 这个 MCP 服务器有什么作用？**
A: 本服务器旨在帮助用户方便地生成用于 xtb (Semiempirical Extended Tight-Binding) 量子化学程序的输入文件，并提供相关参数和计算类型的解释。

**Q: xtb 是什么？**
A: xtb 是一个快速且功能强大的半经验量子化学程序包，适用于大分子体系的几何优化、频率计算、分子动力学等。它实现了 GFNn-xTB (n=0,1,2) 和 GFN-FF 等方法。

**Q: 我需要安装 xtb 才能使用这个服务器吗？**
A: 本服务器只负责生成输入文件。要在本地运行这些计算，您需要在您的系统上安装 xtb 程序。

## 2. 工具使用

**Q: `generate_xtb_input` 工具会生成哪些文件？**
A: 通常会生成一个包含分子结构文件 (如 `structure.xyz`) 和一个控制文件 (`.xcontrolrc`) 的包。根据计算类型和设置，还可能包含 `constraints.inp`, `scan.inp` 等，以及一个运行脚本 `run_xtb.sh`。

**Q: 如何指定分子电荷和自旋多重度？**
A: 在使用 `generate_xtb_input` 或 `generate_xcontrol` 等工具时，通过 `molecule_data` 中的 `charge` 和 `multiplicity` 参数指定。注意，xtb 内部通常使用“未配对电子数” (`multiplicity - 1`)。

**Q: 我可以在哪里找到支持的计算类型和方法？**
A: 请参考 `xtb://formats/input` 资源获取概览，或使用 `explain_xtb_parameters` 工具查询特定方法 (如 "gfn2") 或参数。

**Q: `convert_structure_format` 支持哪些格式转换？**
A: 目前主要支持 XYZ 和 COORD (Turbomole) 格式之间的互转，以及从 Gaussian 输入文件提取 XYZ 坐标。

## 3. 参数和设置

**Q: GFN0, GFN1, GFN2 有什么区别？**
A: 它们是不同版本的 GFN-xTB 方法。
    - **GFN0-xTB**: 速度最快，精度最低，不含色散校正。适用于非常初步的筛选或预优化。
    - **GFN1-xTB**: 速度和精度居中，包含 D3 色散校正。
    - **GFN2-xTB**: 目前推荐的默认方法，精度最高（在GFN系列中），包含 D4 色散校正，对非共价相互作用描述更佳。
    详细信息请查阅 `xtb://parameters/gfn0`, `xtb://parameters/gfn1`, `xtb://parameters/gfn2` 资源。

**Q: 如何设置溶剂？**
A: 在相关工具的 `settings` (或 `method_settings`) 参数中，通过 `"solvent": "solvent_name"` 指定，例如 `"solvent": "h2o"`。xtb 支持多种内置 GBSA 溶剂。指定 `"solvent": "none"` 表示气相计算。

**Q: `.xcontrolrc` 文件是什么？**
A: 这是 xtb 的主控制文件，包含了计算所需的所有参数和指令。本服务器的工具会自动生成此文件。

## 4. 增强采样与高级计算

**Q: 如何进行元动力学 (Metadynamics) 计算？**
A: 使用 `generate_enhanced_sampling` 工具，设置 `sampling_method_type="metadynamics"`，并在 `sampling_params` 中提供必要的参数，如集体变量定义 (`collective_variables_definition`) 和 MD 参数。可以参考 `xtb://sampling/metadynamics` 模板。

**Q: ONIOM 计算如何设置？**
A: 使用 `generate_oniom_input` 工具。您需要定义 QM 原子区域、低层方法以及可能的连接原子。模板 `xtb://advanced/oniom` 可供参考。

## 5. 错误与故障排除

**Q: 我生成的输入文件在 xtb 中运行失败怎么办？**
A: 
    1.  检查 xtb 的输出日志 (`xtb_output.log` 或类似文件) 中的具体错误信息。
    2.  使用 `validate_xtb_input` 工具检查 `.xcontrolrc` 的基本语法和电荷/自旋设置。
    3.  确保您的分子结构合理。
    4.  查阅 xtb 官方文档或相关参数说明资源。

**Q: 为什么我的溶剂设置似乎没有生效？**
A: 确保在 `.xcontrolrc` 文件中正确生成了 `$alpb solvent_name` 块。某些非常旧的 xtb 版本或特定方法 (如 GFN0) 可能对溶剂支持有限。

---
*此 FAQ 会随服务器功能完善而更新。*