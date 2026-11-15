# Changelog

## 0.1.0

第一个版本。把四个来源合成一个仓库：

- **REA** 的本机二进制链路（Ghidra Windows 排障、MCP launcher、结论三件套）→ `targets/native/`
- **逆向工程 Agent** 的产品拆解方法论（四层拆解、五维验证、三步法）→ `targets/product/`
- **ReverseKit** 的六模块脚本按目标类型重排 → `targets/mobile/`、`targets/web/`、`toolkit/`
- **IronCore** 的链路上验证习惯 → `toolkit/verify_armor.py`

统一了证据规范（`docs/evidence.md`）、验证规范（`docs/verification.md`）、工作流（`core/workflow.md`）与路由表（`core/routing.md`）。留出 `targets/_template/` 作为新项目的接入位。

`check.py` 与 CI 共用同一套自检：编译、CLI 冒烟、真实资产与凭据守卫。
