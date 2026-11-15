# Strata 介绍视频 · 文字稿

- 视频：`assets/strata-intro.mp4` ｜ 封面：`assets/strata-poster.png`
- 规格：1920×1080（16:9）、30 fps、22.6 秒、H.264、无配乐
- 节奏：按 120 BPM 的 0.5 秒网格排镜头，每幕 5 秒，转场 0.6 秒
- 制作：分镜由 HTML/CSS 代码渲染、无头 Chromium 定帧，ffmpeg 用 xfade 合成；画面文字与 `README.md` / `README.en.md` 对应

## 分镜

| # | 时间 | 画面 | 中文文案 | English on screen |
| --- | --- | --- | --- | --- |
| 1 | 00:00–00:05 | 名称与分层条纹 | Strata · 层析；一个仓库 · 一套证据规范 · 四类目标 | Strata / One repo. One evidence standard. Four target layers. |
| 2 | 00:05–00:09 | 三条判定规则 | 先定标准，再谈工具：结论带证据和局限 / 命中过对照实验 / 推断标成推断 | Standard first, tools second: a claim ships with its evidence and its limits / a hit survives a control experiment / an inference says it is an inference |
| 3 | 00:09–00:14 | 左右两栏 | 从两个项目合起来：REA（二进制逆向）、逆向工程 Agent（产品拆解）；顺手并入 ReverseKit 工具链与 IronCore 的生效验证 | Two projects, one repo: REA for binaries, Reverse Engineering Agent for systems; portable parts of two earlier repos came along too |
| 4 | 00:14–00:18 | 四层色块 + 共用带 | 现在有什么：native / mobile / web / product；core、docs、toolkit、check.py | Four layers, shared rules |
| 5 | 00:18–00:22.6 | 三步流程 + 落版 | 以后怎么加新项目：复制模板 → 注册路由 → 自检再提；Strata · 层析 | Adding the next one: copy the template → register in routing → run check.py |

## 口播稿 · 中文

做逆向，工具换得快，判断标准不该跟着换。Strata，层析，把两个项目合成一个仓库：REA 管二进制，逆向工程 Agent 管产品拆解。共用一套证据规范——结论带证据和局限，命中过对照实验，推断标成推断。现在按目标分四层：native、mobile、web、product，上面是工作流和路由，下面是工具与自检。以后加新项目，复制模板、注册路由、跑一遍 check.py。

## Voiceover · English

Tools rotate. The bar for believing a result shouldn't. Strata merges two projects into one repo: REA for binaries, and the Reverse Engineering Agent for systems. They share one evidence standard — a claim ships with its evidence and its limits, a hit survives a control experiment, and an inference stays labelled. Four layers today: native, mobile, web, product, with the workflow above and the toolkit below. Adding the next project? Copy the template, register it in routing, run check.py.

## 对应关系

中文口播取 `README.md` 的"从两个项目合起来""以后怎么加新项目"两节；英文口播取 `README.en.md` 的对应段落，不是逐句直译。画面里每幕同时给中文主句与英文副句，覆盖名称、现有内容、扩展方式三项。
