# Ghidra headless 在 Windows 上的三个坑

这几条是在本机实测出来的，现象很容易误判成 JDK 或权限问题。记下来是为了不用再花一小时。

## 坑 1：预置 `.sla` 导致 "Ghidra exited before bridge startup"

Ghidra 的语言定义分两半：`.slaspec` / `.sinc` 是源码，`.sla` 是编译产物。启动时 `SleighLanguage.initialize()` 会判断 `.sla` 是否过期或版本不符，需要重编译——而重编译要写安装目录。

zip 里预置的 `.sla` 常被判成过期，于是启动失败：

```
java.io.FileNotFoundException: ...\data\languages\x86-64.sla (拒绝访问。)
ERROR Can't read language spec ... -> Ghidra exited before bridge startup
```

改时间戳、设只读、加 ACL 全都无效，拦截不在文件系统权限层。

**解法**：解压时跳过所有 `.sla`，让 Ghidra 首次用到某架构时自己编译并写出新文件（写新文件是允许的）：

```python
import zipfile
with zipfile.ZipFile('ghidra.zip') as z:
    for info in z.infolist():
        if info.filename.lower().endswith('.sla'):
            continue
        z.extract(info, 'install-dir')
```

首次编译产物持久有效，第二次运行只读。同一二进制两次独立运行拿到相同 `evidence_id`，可复现。

## 坑 2：沙箱会"封存"工具调用创建的文件

某次工具调用创建的文件，过几分钟再写入或删除会被拒，同目录新建文件却可以。所以"就地修安装目录"这条路走不通；安装目录要放在真实用户可写的位置，并且一次性编译要在同一次调用链里完成。

## 坑 3：超长环境变量 → Win32 87

现象：MCP 通道正常（`open_binary` 能返回哈希），但任何真正拉起 Ghidra 的调用都失败：

```
GhidraLaunchError: Ghidra headless launch failed
cause: Windows value exceeds the native string limit (Win32 87)
```

stderr 里只有 `Picked up JDK_JAVA_OPTIONS / JAVA_TOOL_OPTIONS`，很容易误判成 JDK 配置，**不是**。

真因：宿主进程会给子进程注入一个约 39 万字符的产品配置变量，MCP server 继承后整个环境块接近 788 KB；REA 把它交给 `CreateProcess`，而 Windows 用 16 位长度字段度量环境块，上限 32767 字符 → `ERROR_INVALID_PARAMETER(87)`。

判据：干净环境下直接跑 CLI 的 `inspect` 成功，就说明 Ghidra 本身没问题，问题在进程环境。读进程环境块，看总字节数和最长条目即可定位。

**修法**：所有入口过 `tools/rea-mcp-launcher.mjs`，spawn 前删掉超过 20000 字符的环境变量，stdio 保持 inherit（MCP 走 JSON-RPC，不能缓冲）。改完注册要重启客户端，旧 MCP 进程不会自动换配置。

## 复现清单

- 干净 CLI 与 MCP 两条链路对照跑一遍，确认差异只在环境。
- 记录环境块总大小、最长变量名与长度（不记内容）。
- 首次编译后重跑同一分析，比对 `evidence_id` 是否一致。
