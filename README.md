# XTB MCP Server / XTB MCP 服务器

[English](#english) | [中文](#中文)

---

## English

### Overview

The XTB MCP Server is a Model Context Protocol (MCP) server that provides comprehensive tools for generating Extended Tight-Binding (XTB) quantum chemistry calculation input files. This server integrates seamlessly with AI assistants like Claude, Cursor, and Windsurf to enable intelligent quantum chemistry workflow automation.

### Key Features

- **Complete XTB Input Generation**: Support for all major calculation types (singlepoint, optimization, frequency, scan, MD)
- **Multiple XTB Methods**: GFN0, GFN1, GFN2, and GFN-FF force field support
- **Structure Format Conversion**: XYZ ↔ COORD ↔ Gaussian format handling
- **Advanced Sampling Methods**: Metadynamics, pathfinder, normal mode following
- **Wavefunction Analysis**: Orbital analysis, population analysis, spectroscopy
- **ONIOM Calculations**: Multi-layer QM/MM calculations
- **Input Validation**: Comprehensive validation with detailed error reporting
- **Rich Documentation**: Extensive parameter documentation and examples

### Project Structure

```
xtb-mcp-server/
├── main.py                     # MCP server entry point
├── requirements.txt            # Python dependencies
├── DEPLOYMENT_GUIDE.md         # Deployment instructions
├── PROJECT_SUMMARY.md          # Project overview
├── run_tests.py               # Test runner
├── test_mcp_functionality.py  # MCP functionality tests
├── final_validation.py        # Final validation script
├── xtb_input_generator/       # Core generator module
│   ├── __init__.py
│   ├── generator.py           # Main XTB input generator
│   └── structure_utils.py     # Structure format utilities
├── resources/                 # Template and documentation resources
│   ├── templates/             # XTB input templates
│   │   ├── singlepoint.xtb_tpl
│   │   ├── optimization.xtb_tpl
│   │   ├── frequency.xtb_tpl
│   │   ├── scan.xtb_tpl
│   │   ├── md.xtb_tpl
│   │   ├── sampling/          # Enhanced sampling templates
│   │   ├── wavefunction/      # Wavefunction analysis templates
│   │   └── advanced/          # Advanced calculation templates
│   ├── parameters/            # Method parameter documentation
│   │   ├── gfn0.md
│   │   ├── gfn1.md
│   │   └── gfn2.md
│   ├── formats/               # Input format specifications
│   │   └── input_spec.md
│   └── help/                  # Help documentation
│       └── faq.md
└── tests/                     # Comprehensive test suite
    ├── test_generator.py      # Generator functionality tests
    ├── test_structure_utils.py # Structure utility tests
    └── test_mcp_server.py     # MCP server integration tests
```

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd xtb-mcp-server
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run tests to verify installation:**
   ```bash
   python run_tests.py
   ```

### MCP Configuration

#### Claude Desktop

Add to your Claude Desktop configuration file (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "xtb-mcp-server": {
      "command": "python",
      "args": ["path/to/xtb-mcp-server/main.py"],
      "env": {}
    }
  }
}
```

#### Cursor

Add to your Cursor MCP configuration:

```json
{
  "mcpServers": {
    "xtb-mcp-server": {
      "command": "python",
      "args": ["path/to/xtb-mcp-server/main.py"]
    }
  }
}
```

#### Windsurf

Configure in Windsurf settings:

```json
{
  "mcp": {
    "servers": {
      "xtb-mcp-server": {
        "command": "python",
        "args": ["path/to/xtb-mcp-server/main.py"]
      }
    }
  }
}
```

### Usage Examples

#### Example 1: Basic Geometry Optimization

**User:** "Generate XTB input files for water molecule geometry optimization using GFN2 method"

**AI Assistant Response:**
```
I'll generate XTB input files for water molecule geometry optimization using the GFN2 method.

[Uses generate_xtb_input_package tool]

Generated files:
- structure.xyz: Water molecule coordinates
- xcontrol: Optimization settings with GFN2 method
- run_xtb.sh: Execution script

The optimization will use tight convergence criteria and the GFN2 method for accurate results.
```

#### Example 2: Frequency Calculation with Solvent

**User:** "I need to run a frequency calculation for benzene in toluene solvent. Can you set up the input files?"

**AI Assistant Response:**
```
I'll set up frequency calculation input files for benzene in toluene solvent.

[Uses generate_xtb_input_package tool with frequency calculation type and toluene solvent]

Generated files include:
- Benzene structure in XYZ format
- xcontrol file with frequency calculation settings
- Toluene solvent model (GBSA)
- Temperature set to 298.15 K

The calculation will provide vibrational frequencies and thermodynamic properties.
```

#### Example 3: Enhanced Sampling Setup

**User:** "Set up a metadynamics simulation for conformational sampling of a flexible molecule"

**AI Assistant Response:**
```
I'll configure a metadynamics simulation for conformational sampling.

[Uses generate_enhanced_sampling_input tool]

Generated metadynamics setup:
- Collective variables: dihedral angles
- Gaussian height: 0.1 kcal/mol
- Gaussian width: 0.2 radians
- Deposition frequency: every 100 steps
- Temperature: 300 K

This will efficiently explore the conformational space of your molecule.
```

#### Example 4: Structure Format Conversion

**User:** "Convert this Gaussian input to XYZ format for XTB calculations"

**AI Assistant Response:**
```
I'll convert your Gaussian input file to XYZ format for XTB calculations.

[Uses convert_structure_file_format tool]

Conversion successful:
- Extracted molecular geometry from Gaussian input
- Generated clean XYZ format
- Preserved atomic coordinates and elements
- Ready for XTB calculations

The converted structure is now compatible with all XTB calculation types.
```

### Available Tools

1. **generate_xtb_input_package**: Generate complete XTB input file packages
2. **convert_structure_file_format**: Convert between molecular structure formats
3. **validate_xtb_input_files**: Validate XTB input file syntax and parameters
4. **generate_xcontrol_file**: Generate XTB control files with specific settings
5. **explain_xtb_parameters**: Get detailed explanations of XTB parameters
6. **generate_enhanced_sampling_input**: Set up enhanced sampling calculations
7. **generate_wavefunction_analysis_input**: Configure wavefunction analysis
8. **generate_oniom_input**: Set up multi-layer ONIOM calculations
9. **generate_spectroscopy_input**: Configure spectroscopy calculations
10. **analyze_trajectory**: Analyze molecular dynamics trajectories

### Resources

The server provides access to extensive documentation and templates:
- **Templates**: Pre-configured input templates for all calculation types
- **Parameters**: Detailed documentation for GFN0, GFN1, and GFN2 methods
- **Formats**: Input format specifications and examples
- **Help**: FAQ and troubleshooting guides

---

## 中文

### 概述

XTB MCP 服务器是一个模型上下文协议（MCP）服务器，为生成扩展紧束缚（XTB）量子化学计算输入文件提供全面的工具。该服务器与 Claude、Cursor 和 Windsurf 等 AI 助手无缝集成，实现智能量子化学工作流自动化。

### 主要功能

- **完整的 XTB 输入生成**：支持所有主要计算类型（单点、优化、频率、扫描、分子动力学）
- **多种 XTB 方法**：支持 GFN0、GFN1、GFN2 和 GFN-FF 力场
- **结构格式转换**：XYZ ↔ COORD ↔ Gaussian 格式处理
- **高级采样方法**：元动力学、路径搜索、正常模式跟踪
- **波函数分析**：轨道分析、布居分析、光谱学
- **ONIOM 计算**：多层 QM/MM 计算
- **输入验证**：全面验证和详细错误报告
- **丰富文档**：广泛的参数文档和示例

### 项目结构

```
xtb-mcp-server/
├── main.py                     # MCP 服务器入口点
├── requirements.txt            # Python 依赖
├── DEPLOYMENT_GUIDE.md         # 部署指南
├── PROJECT_SUMMARY.md          # 项目概述
├── run_tests.py               # 测试运行器
├── test_mcp_functionality.py  # MCP 功能测试
├── final_validation.py        # 最终验证脚本
├── xtb_input_generator/       # 核心生成器模块
│   ├── __init__.py
│   ├── generator.py           # 主要 XTB 输入生成器
│   └── structure_utils.py     # 结构格式工具
├── resources/                 # 模板和文档资源
│   ├── templates/             # XTB 输入模板
│   │   ├── singlepoint.xtb_tpl
│   │   ├── optimization.xtb_tpl
│   │   ├── frequency.xtb_tpl
│   │   ├── scan.xtb_tpl
│   │   ├── md.xtb_tpl
│   │   ├── sampling/          # 增强采样模板
│   │   ├── wavefunction/      # 波函数分析模板
│   │   └── advanced/          # 高级计算模板
│   ├── parameters/            # 方法参数文档
│   │   ├── gfn0.md
│   │   ├── gfn1.md
│   │   └── gfn2.md
│   ├── formats/               # 输入格式规范
│   │   └── input_spec.md
│   └── help/                  # 帮助文档
│       └── faq.md
└── tests/                     # 全面测试套件
    ├── test_generator.py      # 生成器功能测试
    ├── test_structure_utils.py # 结构工具测试
    └── test_mcp_server.py     # MCP 服务器集成测试
```

### 安装

1. **克隆仓库：**
   ```bash
   git clone <repository-url>
   cd xtb-mcp-server
   ```

2. **安装依赖：**
   ```bash
   pip install -r requirements.txt
   ```

3. **运行测试验证安装：**
   ```bash
   python run_tests.py
   ```

### MCP 配置

#### Claude Desktop

在 Claude Desktop 配置文件（`claude_desktop_config.json`）中添加：

```json
{
  "mcpServers": {
    "xtb-mcp-server": {
      "command": "python",
      "args": ["path/to/xtb-mcp-server/main.py"],
      "env": {}
    }
  }
}
```

#### Cursor

在 Cursor MCP 配置中添加：

```json
{
  "mcpServers": {
    "xtb-mcp-server": {
      "command": "python",
      "args": ["path/to/xtb-mcp-server/main.py"]
    }
  }
}
```

#### Windsurf

在 Windsurf 设置中配置：

```json
{
  "mcp": {
    "servers": {
      "xtb-mcp-server": {
        "command": "python",
        "args": ["path/to/xtb-mcp-server/main.py"]
      }
    }
  }
}
```

### 使用示例

#### 示例 1：基本几何优化

**用户：** "为水分子生成使用 GFN2 方法的几何优化 XTB 输入文件"

**AI 助手回应：**
```
我将为水分子生成使用 GFN2 方法的几何优化 XTB 输入文件。

[使用 generate_xtb_input_package 工具]

生成的文件：
- structure.xyz：水分子坐标
- xcontrol：使用 GFN2 方法的优化设置
- run_xtb.sh：执行脚本

优化将使用紧收敛标准和 GFN2 方法以获得准确结果。
```

#### 示例 2：溶剂中的频率计算

**用户：** "我需要在甲苯溶剂中对苯进行频率计算。你能设置输入文件吗？"

**AI 助手回应：**
```
我将为苯在甲苯溶剂中的频率计算设置输入文件。

[使用带有频率计算类型和甲苯溶剂的 generate_xtb_input_package 工具]

生成的文件包括：
- XYZ 格式的苯结构
- 带有频率计算设置的 xcontrol 文件
- 甲苯溶剂模型（GBSA）
- 温度设置为 298.15 K

计算将提供振动频率和热力学性质。
```

#### 示例 3：增强采样设置

**用户：** "为柔性分子的构象采样设置元动力学模拟"

**AI 助手回应：**
```
我将为构象采样配置元动力学模拟。

[使用 generate_enhanced_sampling_input 工具]

生成的元动力学设置：
- 集体变量：二面角
- 高斯高度：0.1 kcal/mol
- 高斯宽度：0.2 弧度
- 沉积频率：每 100 步
- 温度：300 K

这将有效探索分子的构象空间。
```

#### 示例 4：结构格式转换

**用户：** "将这个 Gaussian 输入转换为 XTB 计算的 XYZ 格式"

**AI 助手回应：**
```
我将把您的 Gaussian 输入文件转换为 XTB 计算的 XYZ 格式。

[使用 convert_structure_file_format 工具]

转换成功：
- 从 Gaussian 输入中提取分子几何
- 生成清洁的 XYZ 格式
- 保留原子坐标和元素
- 准备用于 XTB 计算

转换后的结构现在与所有 XTB 计算类型兼容。
```

### 可用工具

1. **generate_xtb_input_package**：生成完整的 XTB 输入文件包
2. **convert_structure_file_format**：在分子结构格式之间转换
3. **validate_xtb_input_files**：验证 XTB 输入文件语法和参数
4. **generate_xcontrol_file**：生成具有特定设置的 XTB 控制文件
5. **explain_xtb_parameters**：获取 XTB 参数的详细解释
6. **generate_enhanced_sampling_input**：设置增强采样计算
7. **generate_wavefunction_analysis_input**：配置波函数分析
8. **generate_oniom_input**：设置多层 ONIOM 计算
9. **generate_spectroscopy_input**：配置光谱学计算
10. **analyze_trajectory**：分析分子动力学轨迹

### 资源

服务器提供对广泛文档和模板的访问：
- **模板**：所有计算类型的预配置输入模板
- **参数**：GFN0、GFN1 和 GFN2 方法的详细文档
- **格式**：输入格式规范和示例
- **帮助**：FAQ 和故障排除指南

### 许可证

本项目采用 MIT 许可证。

### 贡献

欢迎贡献！请提交 Pull Request 或创建 Issue 来报告错误或建议功能。

### 支持

如有问题或需要支持，请查看 `resources/help/faq.md` 或创建 Issue。