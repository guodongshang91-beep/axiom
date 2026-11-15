# Axiom 介绍视频 · 文字稿

- 视频：`assets/axiom-intro.mp4` ｜ 封面：`assets/axiom-poster.png`
- 规格：1920×1080（16:9）、30 fps、24.00 秒、H.264、7.7 MB、无配乐
- 节奏：120 BPM，一拍 0.5 秒；五幕各 4.8 秒，切点落在小节线，每 4 拍一次强拍
- 制作：按 KIRO Motion Studio 的 2D 管线，**720 帧逐帧由代码渲染**（numpy 渐变/暗角/颗粒、PIL 文字与几何、seeded 粒子场），
  RGB24 直接送进 ffmpeg；不是静帧拼接，也不是实拍或模板特效
- 画面层次：流动光晕 + 网格 + 粒子 + 几何基准线（公理意象）→ 逐字入场的大字 Logo 与扫光 →
  HUD / 拍点脉冲 → 强拍色差、闪白、幕边界横条错位转场 → 暗角与颗粒
- 中文字形用本机 Microsoft YaHei，混合中英字符串自动回退到 CJK 字体，画面文字与 `README.md` / `README.en.md` 对应

## 分镜

| # | 时间 | 画面 | 中文文案 | English on screen |
| --- | --- | --- | --- | --- |
| 1 | 00:00–00:04.8 | AXIOM 逐字弹入、几何同心圆与基准线、扫光 | Axiom · 公理；工具会换，公理不换；first principles for reverse engineering | AXIOM / Tools rotate. Axioms don't. |
| 2 | 00:04.8–00:09.6 | 三条规则依次滑入 | 先写公理，再放工具：结论带证据和局限 / 命中过对照实验 / 推断标成推断 | Axioms first, tools second: a claim ships with its evidence and its limits / a hit survives a control experiment / an inference says it is an inference |
| 3 | 00:09.6–00:14.4 | 左右两卡片对向滑入、中间光轴 | 从两个项目合起来：REA（二进制逆向）、逆向工程 Agent（产品拆解）；顺手并入 ReverseKit 与 IronCore | Two projects, one repo: REA for binaries, Reverse Engineering Agent for systems; portable parts of two earlier repos came along too |
| 4 | 00:14.4–00:19.2 | 四层色块错峰升起 + 共用带 | 现在有什么：native / mobile / web / product；core、docs、toolkit、check.py；判定标准只有一份，工具可以换 | Four layers, shared rules |
| 5 | 00:19.2–00:24 | 三步流程展开、落版 | 以后怎么加新项目：复制模板 → 注册路由 → 自检再提；AXIOM · 公理；工具会换，公理不换 | Adding the next one: copy the template → register in routing → run check.py |

## 口播稿 · 中文

工具会换，公理不换。Axiom，把两个项目合成一个仓库：REA 管二进制，逆向工程 Agent 管产品拆解。共用一套不随工具改变的判定标准——结论带证据和局限，命中过对照实验，推断标成推断。现在按目标分四层：native、mobile、web、product，上面是工作流和路由，下面是工具与自检。以后加新项目，复制模板、注册路由、跑一遍 check.py。

## Voiceover · English

Tools rotate. Axioms don't. Axiom merges two projects into one repo: REA for binaries, and the Reverse Engineering Agent for systems. They share a standard that doesn't move with the tooling — a claim ships with its evidence and its limits, a hit survives a control experiment, and an inference stays labelled. Four layers today: native, mobile, web, product, with the workflow above and the toolkit below. Adding the next project? Copy the template, register it in routing, run check.py.

## 对应关系

中文口播取 `README.md` 的开头与「从两个项目合起来」「以后怎么加新项目」两节；英文口播取 `README.en.md` 的对应段落，不是逐句直译。每幕画面同时给中文主句与英文副句，覆盖名称、现有内容、扩展方式三项；片头与落版都出现「工具会换，公理不换 / Tools rotate. Axioms don't.」。
