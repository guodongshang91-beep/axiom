# mobile · APK 与 Android 运行时

并入 `ReverseKit` 的 android 模块，加本机 APK 验证与免 root 注入实践里抽出的通用部分。脚本只做静态校验与产物体检，不含针对具体应用的目标数据。

## 目标类型

APK / AAR / 资源与清单 / 应用运行时。不处理原生 so 的指令级分析（走 `targets/native/`）。

## 首选工具

| 脚本 | 作用 |
| --- | --- |
| `tools/aar_extract.py` | 拆 AAR，取出 classes / res / manifest |
| `tools/res_check.py` | XML、资源 id 与 manifest 引用一致性 |
| `tools/syntax_check.py` | Java 源码语法解析（需 `pip install javalang`） |

三个都能 `-h` 自解释，被 `check.py` 逐个冒烟。

## 证据形态

类与方法名、资源引用、`uiautomator` UI 层级回显、logcat、安装包里文件的哈希与大小。

## 两条实践规则

**读图失败就切文本验收。** 截图识别不可用时，用 `uiautomator dump` 的节点树 + logcat + `adb forward` + 包内文件体检继续验证，不要因为一张图停摆。坐标从 `bounds` 取，别按截图比例目测。

**静态校验不能替代编译。** `syntax_check.py` 只能查语法、括号和结构，查不出类型错误、方法不存在、API 等级不够。要下"能跑"的结论，必须真机或 Gradle 编译；这一点在证据的"局限"里要写明。

## 已知局限

- 语法检查依赖第三方解析器，版本差异会影响结果，记录版本。
- 运行时观测需要模拟器 / 设备，仓库里只有方法，没有设备配置和 AVD 镜像。
- 涉及坐标系的做法先统一坐标系（物理分辨率、检测帧缩放系数）再谈数值。
