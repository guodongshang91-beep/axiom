# 目标 → 工具 → 证据形态

新模块接入时在这张表里加一行。没登记的能力不会被发现，也不会被维护。

| 目标类型 | 典型对象 | 首选工具 / 入口 | 证据形态 |
| --- | --- | --- | --- |
| native | PE / DLL / ELF / 固件 | `targets/native/tools/elfkit.py`；REA + Ghidra provider（见模块 README） | 伪代码、指令、偏移、`evidence_id` |
| mobile | APK / AAR / 应用运行时 | `targets/mobile/tools/aar_extract.py`、`res_check.py`；模拟器 UI 层级 | 类与方法名、资源引用、`uiautomator` 回显、logcat |
| web | 站点 / 接口 / 前端 bundle | `targets/web/tools/probe.py`、`unauth_scan.py`；随机路径基线 | 原始请求响应（头 + 体）、状态码、md5 对照 |
| product | 产品 / 平台 / 技术栈 | 四层拆解法、五维验证（见模块 README） | 公开可观测行为、接口面、版本与依赖线索 |

## 怎么选

1. 先看**对象本身**属于哪一类，不要看手边哪个工具顺手。
2. 跨类的对象（比如 Electron 桌面应用）按要回答的问题选：问"这个二进制里有什么"走 native，问"页面和主进程怎么通信"走 `docs/reference/javascript-applications.md` + web 的运行期观测。
3. 一类对象有多个工具时，先跑产出**原始材料**的那个，再跑会下判断的那个。
4. 表里没有的类型，先走 `targets/_template/` 的接入流程，不要临时塞进最近的一层。

## 证据形态为什么写在表里

不同层的证据不能直接互相印证：一段伪代码不能证明接口未授权，一个 200 状态码不能证明函数被调用。写清形态，是为了让跨层结论自动带上局限。
