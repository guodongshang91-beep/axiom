# Strata · 层析

> 一个仓库，放逆向工程里不会过期的那部分。

[English version](README.en.md) · [MIT](LICENSE) · [22 秒介绍视频](assets/strata-intro.mp4) · [文字稿](assets/strata-intro-script.md)

工具换得很快，判断标准不该跟着换。扫描器报一堆"命中"，反编译器吐一段伪代码，产品拆解写得头头是道——哪一条能当结论用？

Strata 把标准放在最前面：**结论带证据和局限，命中过对照实验，推断标成推断**。`docs/evidence.md` 和 `docs/verification.md` 是所有模块共用的，脚本只负责产出能复核的原始材料，不负责下结论。

## 从两个项目合起来

- **REA**（`targets/native/`）：本机跑通的二进制逆向入口。Ghidra headless 在 Windows 上的三个真坑——预置 `.sla` 触发重编译、安装目录写不进去、超长环境变量让 `CreateProcess` 报 Win32 87——连同剥掉大变量的 MCP launcher 都留在这里。结论三件套（结论 / 证据 / 局限）也来自它。
- **逆向工程 Agent**（`targets/product/`）：面向产品和系统的拆解方法。四层拆解、五维验证、预判 → 确认 → 深入三步法，事实、推断、置信度分三栏写。

一个管"程序里是什么"，一个管"这套系统怎么搭的"。原先各写一份的证据规范抽到 `docs/`，工作流程抽到 `core/`，合起来是一个项目，不是两个目录并排。

## 顺手并进来的

整合时把此前两个公开仓库里能复用的工程件也收了：`ReverseKit` 的六模块脚本按目标类型重排（Web 侦察、APK 静态校验、ELF 分析、假阳性防线、证据固定、自检），`IronCore` 的"改动有没有生效要在链路上验证"作为 `toolkit/verify_armor.py` 留下。REA 官方六篇目标类型参考原样放在 `docs/reference/`。只收中性、可泛化的方法，不放具体目标、厂商清单和样本。

## 现在有什么

| 路径 | 管什么 |
| --- | --- |
| `core/` | 三步法工作流，目标 → 工具 → 证据形态的路由表 |
| `targets/native/` | PE / ELF / 原生二进制，Ghidra Windows 排障，MCP launcher |
| `targets/mobile/` | APK 拆包、资源引用与语法静态校验、模拟器验收要点 |
| `targets/web/` | 黑盒侦察、软 404 与 JSONP 判定、五道假阳性防线 |
| `targets/product/` | 产品与技术栈拆解、评级与防幻觉标注 |
| `toolkit/` | 证据固定、命中校验、生效验证、自检 |
| `docs/` | 证据规范、验证规范、模块模板、REA 上游参考 |

零重型依赖，Python 3.9+ 标准库为主。`python check.py` 一次跑完编译、CLI 冒烟和真实资产守卫，CI 用的是同一个脚本。

```bash
python check.py                       # 全量自检
python check.py --quick               # 改个字符串时够用
python toolkit/verify_hit.py -h       # 任一命中先过一遍对照判定
```

## 以后怎么加新项目

1. `cp -r targets/_template targets/<name>`，README 写清目标类型、证据长什么样、怎么复现。
2. 在 `core/routing.md` 加一行：目标 → 首选工具 → 证据形态。
3. 脚本放 `tools/`，`-h` 能自解释，写操作带 `--dry-run`。
4. 跑 `python check.py`，过了再提 PR。

别另起顶层目录，也别复制一份证据规范。新能力先接到现有四层里，接不进去再讨论第五层。完整规则见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 边界

仓库里只有方法、判定和可复现的脚本，没有真实目标、厂商清单、样本或凭据。只对自己有权分析的对象使用。

## 许可

MIT。上游资料沿用各自许可，见 [docs/reference/README.md](docs/reference/README.md)。
