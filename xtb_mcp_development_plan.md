# XTB 输入文件生成 MCP 服务器 - 开发计划与进度

## 1. 项目概述

开发一个 MCP (Model Context Protocol) 服务器，为大语言模型提供专业的 xtb 量子化学计算输入文件生成服务。该服务器能够根据用户需求智能生成完整的 xtb 计算输入文件包和配置，支持核心计算类型、增强采样、波函数分析及高级计算功能。

## 2. 开发阶段与任务分解

### 阶段一：项目初始化与核心框架 (预计 1 周)
*   **任务 1.1**: 初始化项目结构。
    *   创建 Python 项目环境。
    *   项目将使用 `mcp_python_sdk` 中的 `FastMCP` 类来构建服务器。开发者应使用 `uv add "mcp[cli]"` 或 `pip install "mcp[cli]"` (或类似的包含服务器组件的命令) 来安装必要的库。
*   **任务 1.2**: 搭建 MCP 服务器基本框架。
    *   实现 MCP `get_manifest` 端点。
    *   定义基础的资源 URI 结构。
*   **任务 1.3**: 实现基础资源管理。
    *   `xtb://templates/singlepoint`
    *   `xtb://templates/optimization`
    *   `xtb://templates/frequency`
    *   `xtb://parameters/gfn2` (作为示例)
    *   `xtb://formats/input`
    *   *说明*: 资源内容可以是预定义的文本文件或字符串。

### 阶段二：核心工具 - 输入生成与验证 (预计 2 周)
*   **任务 2.1**: 实现 `XTBInputGenerator` 核心类。
    *   设计 `__init__` 方法，加载模板和初始化验证器。
*   **任务 2.2**: 实现 `generate_xtb_input` 工具 (基础功能)。
    *   支持 `calculation_type`: `singlepoint`, `optimization`, `frequency`。
    *   支持 `method`: `gfn0`, `gfn1`, `gfn2`。
    *   分子结构数据处理 (`xyz` 格式初步支持)。
    *   基础 `settings` (如溶剂)。
    *   生成 `structure.xyz` 和 `.xcontrolrc`。
*   **任务 2.3**: 实现 `generate_xcontrol` 工具 (基础功能)。
    *   生成 `$chrg`, `$spin`。
    *   根据计算类型生成对应块 (如 `$opt`)。
*   **任务 2.4**: 实现 `validate_xtb_input` 工具 (基础功能)。
    *   验证分子电荷和自旋多重度。
    *   检查基础 `xcontrol` 语法。
*   **任务 2.5**: 实现 `convert_structure_format` 工具。
    *   初步支持 `xyz` 到 `coord` (反之亦然)。
*   **任务 2.6**: 实现 `explain_xtb_parameters` 工具。
    *   支持解释 `globpar` 类型的参数。

### 阶段三：核心功能完善与扩展 (预计 2 周)
*   **任务 3.1**: 完善 `generate_xtb_input`。
    *   支持 `calculation_type`: `scan`, `md`。
    *   扩展 `settings` 支持：约束、扫描参数。
    *   生成 `constraints.inp`, `scan.inp` (如果需要)。
    *   生成 `run_xtb.sh` 脚本。
*   **任务 3.2**: 完善分子结构处理。
    *   支持更多格式: `coord`, `vasp`, `gaussian`。
    *   自动检测分子电荷和自旋状态 (如果未提供)。
    *   基础的分子结构合理性验证。
*   **任务 3.3**: 完善参数验证规则。
    *   方法与设置兼容性检查。
*   **任务 3.4**: 实现其余核心资源。
    *   `xtb://templates/scan`, `xtb://templates/md`
    *   `xtb://parameters/gfn0`, `xtb://parameters/gfn1`

### 阶段四：增强采样功能 (预计 2 周)
*   **任务 4.1**: 实现增强采样相关资源。
    *   `xtb://sampling/metadynamics`, `xtb://sampling/pathfinder`, etc.
*   **任务 4.2**: 实现 `generate_enhanced_sampling` 工具。
    *   支持 `sampling_method`: `metadynamics`, `pathfinder`。
    *   处理 `collective_variables` 和 `sampling_parameters`。
*   **任务 4.3**: 实现 `setup_metadynamics` 工具。
*   **任务 4.4**: 实现 `generate_reaction_path` 工具 (部分，如 Pathfinder)。

### 阶段五：波函数分析与高级计算 (预计 2 周)
*   **任务 5.1**: 实现波函数分析相关资源。
    *   `xtb://wavefunction/orbitals`, `xtb://wavefunction/density`, etc.
*   **任务 5.2**: 实现 `generate_wavefunction_analysis` 工具。
    *   支持多种 `analysis_types`。
    *   处理 `output_formats` (如 cube 文件)。
*   **任务 5.3**: 实现高级计算相关资源。
    *   `xtb://advanced/oniom`, `xtb://advanced/embedding`, etc.
*   **任务 5.4**: 实现 `generate_oniom_input` 工具。
*   **任务 5.5**: 实现 `generate_spectroscopy_input` 工具 (部分，如 IR)。

### 阶段六：高级功能完善、测试与文档 (预计 2-3 周)
*   **任务 6.1**: 完善所有扩展工具。
    *   `generate_enhanced_sampling` (Umbrella, Steered MD, Normal Mode)。
    *   `generate_reaction_path` (NEB, String)。
    *   `generate_spectroscopy_input` (UV-Vis, NMR, STM)。
    *   `analyze_trajectory` 工具。
*   **任务 6.2**: 实现用户交互设计。
    *   智能参数建议。
    *   帮助和文档资源 (`xtb://help/faq`, `xtb://help/examples`)。
*   **任务 6.3**: 全面测试。
    *   单元测试 (目标覆盖率 >90%)。
    *   集成测试，覆盖各种计算类型和参数组合。
    *   边界条件和错误情况测试。
*   **任务 6.4**: 编写 API 文档和使用示例。
*   **任务 6.5**: 性能优化和错误处理增强。
    *   详细的错误诊断信息和建议。
    *   计算资源需求评估警告。
*   **任务 6.6**: 安全性检查 (输入内容验证，防止路径遍历等)。

## 3. 预估总时间

总计约 11-12 周。这是一个初步估计，具体时间会根据开发过程中的实际情况调整。

## 4. 建议的代码结构 (功能模块划分)

```
xtb-mcp-server/
├── main.py                     # MCP 服务器入口 (FastAPI/FastMCP app)
├── mcp_manifest.json           # MCP 服务器清单文件 (或动态生成)
├── xtb_input_generator/
│   ├── __init__.py
│   ├── generator.py            # 包含 XTBInputGenerator 类
│   ├── validators.py           # 输入验证逻辑模块
│   ├── structure_utils.py      # 分子结构处理工具函数
│   └── templates.py            # 模板加载和管理
├── resources/                  # 存放资源文件
│   ├── templates/              # 计算模板
│   │   ├── singlepoint.xtb_tpl
│   │   ├── optimization.xtb_tpl
│   │   └── ...
│   ├── parameters/             # 参数说明文档 (markdown)
│   │   ├── gfn0.md
│   │   └── ...
│   ├── formats/                # 格式规范文档
│   │   └── input_spec.md
│   ├── sampling/               # 增强采样模板/配置
│   │   └── metadynamics.xtb_tpl
│   ├── wavefunction/           # 波函数分析配置
│   │   └── orbitals_output.xtb_tpl
│   └── advanced/               # 高级计算模板
│       └── oniom_setup.xtb_tpl
├── tests/
│   ├── test_generator.py
│   ├── test_validators.py
│   └── ...
├── docs/
│   ├── api.md
│   └── examples/
│       └── example_singlepoint.json
└── README.md
```

### `XTBInputGenerator` 类 (在 `xtb_input_generator/generator.py` 中)
```python
class XTBInputGenerator:
    def __init__(self, resource_path="resources"):
        self.resource_path = resource_path
        self.templates = self._load_all_templates()
        self.parameter_docs = self._load_parameter_docs()
        # self.validators = self._init_validators() # 可能移到 validators.py

    def _load_all_templates(self):
        # 加载所有类型的模板
        pass

    def _load_parameter_docs(self):
        # 加载参数说明文档
        pass

    # --- MCP Tool Implementations ---
    def generate_xtb_input_package(self, molecule_data, calculation_type, method, settings):
        # 实现 generate_xtb_input 工具的核心逻辑
        # 返回文件内容字典: {"structure.xyz": "...", ".xcontrolrc": "..."}
        pass

    def validate_xtb_input_files(self, input_files):
        # 实现 validate_xtb_input 工具
        pass

    def convert_structure_file_format(self, input_format, output_format, structure_data):
        # 实现 convert_structure_format 工具
        pass

    def generate_xcontrol_file(self, charge, spin, calculation_settings):
        # 实现 generate_xcontrol 工具
        pass

    def explain_xtb_parameters_info(self, parameter_type, specific_parameter=None):
        # 实现 explain_xtb_parameters 工具
        pass

    def generate_enhanced_sampling_input_package(self, sampling_method, collective_variables, sampling_parameters, restart_options=None):
        # 实现 generate_enhanced_sampling 工具
        pass

    def generate_wavefunction_analysis_input_package(self, analysis_types, output_formats, visualization_settings=None):
        # 实现 generate_wavefunction_analysis 工具
        pass

    def generate_oniom_input_package(self, layers, link_atoms, oniom_settings=None):
        # 实现 generate_oniom_input 工具
        pass

    def generate_reaction_path_input_package(self, path_method, reactant_structure, product_structure, path_parameters, convergence_criteria=None):
        # 实现 generate_reaction_path 工具
        pass

    def generate_spectroscopy_input_package(self, spectroscopy_types, ir_settings=None, uv_vis_settings=None, stm_settings=None):
        # 实现 generate_spectroscopy_input 工具
        pass

    def setup_metadynamics_run_files(self, collective_variables, gaussian_parameters, simulation_settings):
        # 实现 setup_metadynamics 工具
        pass

    def analyze_md_trajectory_results(self, trajectory_file, analysis_types, output_options=None):
        # 实现 analyze_trajectory 工具
        pass

    # --- MCP Resource Access ---
    def get_resource(self, uri_path):
        # 根据URI路径 (e.g., "templates/singlepoint") 返回资源内容
        # Example: xtb://templates/singlepoint -> uri_path = "templates/singlepoint"
        # 需要解析URI，并从 self.templates 或 self.parameter_docs 或直接从文件系统加载
        pass

    # --- Helper methods ---
    def _create_xcontrol_content(self, charge, spin, calc_settings_dict):
        # 内部方法，用于构建 .xcontrolrc 文件内容
        pass

    def _validate_molecule_structure(self, molecule_data):
        # 内部方法，验证分子结构
        pass
```

## 5. 关键技术点和注意事项

*   **MCP SDK/Framework**: 项目将使用官方 `mcp_python_sdk` 中提供的 `FastMCP` 类 ([`mcp.server.fastmcp.FastMCP`](https://github.com/modelcontextprotocol/python-sdk/blob/main/README.md#2025-04-23_snippet_4)) 来构建 MCP 服务器。
*   **XTB 参数知识**: 准确理解和实现 xtb 的各种参数和输入文件格式至关重要。必要时通过 `context7` 查询 xtb 文档。
*   **分子结构库**: 可能需要一个 Python 库来处理分子坐标的读写和转换 (如 `ase`, `rdkit` 的轻量级部分，或自定义实现)。
*   **模板引擎**: 考虑使用简单的模板引擎 (如 `jinja2`，如果 `xcontrol` 文件复杂) 或字符串格式化来生成配置文件。
*   **错误处理**: 提供清晰、具体的错误信息和修复建议。
*   **安全性**: 对所有用户输入进行严格验证，特别是文件路径和内容。
*   **可扩展性**: 设计时考虑未来 xtb 版本更新或新功能的加入。
*   **无中文代码**: 所有 Python 代码不包含中文字符，注释可以使用中文。

## 6. 后续步骤

*   **环境搭建**: 根据阶段一开始任务。
*   **Context7 查询**:
    *   在开发过程中，按需查询 xtb 的具体参数细节和高级用法。
    *   参考 `mcp_python_sdk` ([`/modelcontextprotocol/python-sdk`](https://context7.com/modelcontextprotocol/python-sdk)) 和 `fastmcp` ([`/jlowin/fastmcp`](https://context7.com/jlowin/fastmcp)) 的文档以获取 `FastMCP` 的最佳实践和高级用法。

这个计划为后续的开发工作提供了一个清晰的路线图。