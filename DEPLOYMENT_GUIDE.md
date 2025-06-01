# XTB MCP服务器部署指南

## 项目概述

这是一个专业的XTB (Extended Tight-Binding) 量子化学计算输入文件生成MCP服务器。该服务器提供了完整的工具和资源，用于生成、验证和转换XTB计算输入文件。

## 功能特性

### 核心功能
- ✅ **输入文件生成**: 支持单点、优化、频率、扫描、分子动力学等计算类型
- ✅ **格式转换**: XYZ ↔ COORD ↔ Gaussian格式互转
- ✅ **输入验证**: 语法检查、参数一致性验证
- ✅ **模板系统**: 丰富的预定义计算模板
- ✅ **参数解释**: GFN0/1/2-xTB方法参数说明

### 高级功能
- ✅ **增强采样**: Metadynamics、路径搜索、正则模式跟踪
- ✅ **波函数分析**: 分子轨道、电子密度、成键分析
- ✅ **多层计算**: ONIOM方法支持
- ✅ **光谱计算**: IR、UV-Vis光谱性质计算
- ✅ **错误处理**: 完善的错误检测和用户友好的错误信息

## 系统要求

### 必需依赖
```bash
pip install mcp fastmcp
```

### 可选依赖（用于开发和测试）
```bash
pip install pytest unittest2
```

## 安装和部署

### 1. 克隆项目
```bash
git clone <repository-url>
cd xtb-mcp-server
```

### 2. 验证安装
```bash
# 运行所有测试
python run_tests.py

# 运行MCP功能测试
python test_mcp_functionality.py
```

### 3. 启动服务器

#### 方式1: STDIO模式（推荐用于MCP客户端）
```bash
python main.py
```

#### 方式2: HTTP模式（用于调试）
```python
# 修改main.py最后几行
if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=9000)
```

## MCP客户端配置

### Claude Desktop配置
在Claude Desktop的配置文件中添加：

```json
{
  "mcpServers": {
    "xtb-input-generator": {
      "command": "python",
      "args": ["path/to/xtb-mcp-server/main.py"],
      "cwd": "path/to/xtb-mcp-server"
    }
  }
}
```

### 其他MCP客户端
参考MCP协议文档配置STDIO传输方式。

## 使用示例

### 1. 生成单点计算输入
```python
# 通过MCP工具调用
generate_xtb_input(
    molecule_data={
        "format": "xyz",
        "content": "3\nWater\nO 0.0 0.0 0.0\nH 0.0 0.0 1.0\nH 0.0 1.0 0.0",
        "charge": 0,
        "multiplicity": 1
    },
    calculation_type="singlepoint",
    method="gfn2",
    settings={"solvent": "h2o", "temperature": 298.15}
)
```

### 2. 访问模板资源
```python
# 获取单点计算模板
template = access_resource("xtb://templates/singlepoint")

# 获取GFN2参数文档
docs = access_resource("xtb://parameters/gfn2")
```

### 3. 验证输入文件
```python
validate_xtb_input({
    "xcontrol_content": "$chrg 0\n$spin 0\n$gfn 2\n...",
    "expected_charge": 0,
    "expected_multiplicity": 1
})
```

## 资源结构

```
resources/
├── templates/           # 计算模板
│   ├── singlepoint.xtb_tpl
│   ├── optimization.xtb_tpl
│   ├── frequency.xtb_tpl
│   ├── scan.xtb_tpl
│   ├── md.xtb_tpl
│   ├── sampling/        # 增强采样模板
│   ├── wavefunction/    # 波函数分析模板
│   └── advanced/        # 高级计算模板
├── parameters/          # 参数文档
│   ├── gfn0.md
│   ├── gfn1.md
│   └── gfn2.md
├── formats/            # 格式规范
│   └── input_spec.md
└── help/               # 帮助文档
    └── faq.md
```

## 可用的MCP资源

### 模板资源
- `xtb://templates/singlepoint` - 单点计算模板
- `xtb://templates/optimization` - 几何优化模板
- `xtb://templates/frequency` - 频率计算模板
- `xtb://templates/scan` - 扫描计算模板
- `xtb://templates/md` - 分子动力学模板
- `xtb://sampling/metadynamics` - Metadynamics模板
- `xtb://sampling/pathfinder` - 反应路径搜索模板
- `xtb://wavefunction/orbitals` - 分子轨道分析模板
- `xtb://advanced/oniom` - ONIOM计算模板
- `xtb://advanced/spectroscopy_ir` - IR光谱计算模板

### 参数文档
- `xtb://parameters/gfn0` - GFN0-xTB参数说明
- `xtb://parameters/gfn1` - GFN1-xTB参数说明
- `xtb://parameters/gfn2` - GFN2-xTB参数说明

### 帮助资源
- `xtb://formats/input` - 输入格式规范
- `xtb://help/faq` - 常见问题解答

## 可用的MCP工具

### 基础工具
- `generate_xtb_input` - 生成XTB计算输入文件包
- `validate_xtb_input` - 验证XTB输入文件
- `convert_structure_format` - 分子结构格式转换
- `generate_xcontrol` - 生成xcontrol配置文件
- `explain_xtb_parameters` - 解释XTB参数

### 高级工具
- `generate_enhanced_sampling` - 生成增强采样输入
- `generate_wavefunction_analysis` - 生成波函数分析输入
- `generate_oniom_input` - 生成ONIOM计算输入
- `generate_spectroscopy_input` - 生成光谱计算输入
- `analyze_trajectory` - 分析MD轨迹（占位符功能）

## 测试状态

✅ **所有测试通过**: 50个单元测试全部通过
✅ **MCP功能验证**: 所有核心功能正常工作
✅ **错误处理**: 完善的错误检测和处理
✅ **资源访问**: 所有模板和文档资源可正常访问

## 故障排除

### 常见问题

1. **资源文件未找到**
   - 确保`resources/`目录存在且包含所有必需文件
   - 检查文件路径和权限

2. **编码问题**
   - 确保所有文件使用UTF-8编码
   - Windows系统可能需要设置环境变量`PYTHONIOENCODING=utf-8`

3. **MCP连接问题**
   - 检查客户端配置中的路径是否正确
   - 确保Python环境包含所需依赖

### 调试模式

启用调试输出：
```python
# 在main.py中添加
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 开发指南

### 添加新模板
1. 在`resources/templates/`中创建`.xtb_tpl`文件
2. 在`main.py`中添加对应的资源函数
3. 更新`generator.py`中的模板加载逻辑

### 添加新工具
1. 在`generator.py`中实现工具逻辑
2. 在`main.py`中添加MCP工具装饰器
3. 编写相应的测试用例

### 运行测试
```bash
# 运行特定测试模块
python run_tests.py test_structure_utils
python run_tests.py test_generator
python run_tests.py test_mcp_server

# 运行所有测试
python run_tests.py
```

## 许可证

[根据项目需要添加许可证信息]

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 编写测试
4. 提交Pull Request

## 联系信息

[根据项目需要添加联系信息]