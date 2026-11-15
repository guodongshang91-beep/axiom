# native · 原生二进制

来自 **REA**（Reverse Engineer Anything）的本机链路，加并入的 ELF 分析工具。REA 上游是 MIT，作者 morluto；它不是自研反编译引擎，而是把 Ghidra / IDA / JADX 这些现成工具包成 MCP 网关，让 Agent 用自然语言驱动。

## 目标类型

PE / DLL / ELF / 原生二进制、固件镜像。不处理托管运行时、不处理 Web 接口。

## 首选工具

- 概览与函数伪代码：REA + `ghidra` provider（headless，只读）。
- 结构体检：`tools/elfkit.py`。
- MCP 通道：`tools/rea-mcp-launcher.mjs`，见下方 Windows 注意事项。

MCP 已在工具列表里就直接调，不要每次先跑 doctor / setup。工具不可用时再退回 CLI。

## 证据形态

伪代码、指令、偏移、`evidence_id`。每条结论按 `docs/evidence.md` 写三件套；静态结果一律标 `inference`，不能写成"观测到执行"。

Windows 上 provider 只覆盖只读的 inventory / memory / function-analysis 操作，限定原生 x86 / x86-64 / ARMNT / ARM64 的 PE 与 DLL。GUI 状态、批注、其他架构不在范围内。冷启动一次导入加分析约 40–60 秒，别当成卡死。

## Windows 排障

三个真坑的完整成因与解法在 [`ghidra-windows.md`](ghidra-windows.md)：预置 `.sla` 触发重编译、安装目录写不进去、超长环境变量让 `CreateProcess` 报 Win32 87。

`tools/rea-mcp-launcher.mjs` 是第三条的修法：spawn 前删掉超过 20000 字符的环境变量。入口路径走环境变量 `REA_ENTRY`，不再写死绝对路径：

```bash
REA_ENTRY=/path/to/rea-agents/scripts/rea.mjs \
  node targets/native/tools/rea-mcp-launcher.mjs mcp
```

## 已知局限

- 免执行的静态分析，不证明运行时行为。
- 反编译结果随 provider 版本变化，`evidence_id` 要连同版本一起记。
- 授权校验一类的判定只做结构定位与证据记录，仓库里不放针对具体程序的补丁。
