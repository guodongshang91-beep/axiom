# 上游参考

`docs/reference/` 放的是 REA（Reverse Engineer Anything）官方按目标类型编写的六篇指南，原样保留，便于对照上游更新。

| 文件 | 主题 |
| --- | --- |
| `native-and-artifacts.md` | 原生二进制、安装包、固件 |
| `javascript-applications.md` | JS / ASAR 应用、IPC 边界、版本比对 |
| `android-applications.md` | APK 的类、方法与资源 |
| `runtime-observation.md` | 浏览器 / Electron 运行期观测、HAR |
| `evidence-workflows.md` | 证据分页、比对、验证 |
| `connection-and-recovery.md` | MCP 连接与故障恢复 |

REA 上游为 MIT 许可，作者 morluto。这些文件是参考资料，不是本仓库的规范；本仓库的规范在 `docs/evidence.md` 与 `docs/verification.md`，两者冲突时以本仓库规范为准。

其余并入的脚本来自此前的公开仓库 `ReverseKit` 与 `IronCore`（同为 MIT），已按目标类型重排、去掉机器相关路径和具体目标。原始出处见各模块 README。
