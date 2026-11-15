# toolkit · 跨层工具

这里放不属于任何单一目标类型、四层都要用的东西。新增工具前先问一句：它是不是只对某一类目标有用？是的话放回对应 `targets/*/tools/`。

| 文件 | 作用 |
| --- | --- |
| `evidkit.py` | 证据固定：把原始请求响应、哈希、时间戳收成可复核的一包 |
| `verify_hit.py` | 命中判定：随机路径基线 + 五道假阳性防线，输出 candidate / rejected |
| `verify_armor.py` | 生效验证：证明改动真的到达了链路上，而不只是文件写对了 |
| `../check.py` | 仓库自检：编译、CLI 冒烟、真实资产与凭据守卫 |

## 为什么要单独一层

四层各自都能产出"命中"，但判定逻辑是同一套。放在各自目录里就会各写一遍，措辞慢慢分叉。这里只保留一份实现，模块引用它。

```bash
python toolkit/verify_hit.py --self-test
python toolkit/verify_hit.py --baseline base.json --candidate hit.json \
    --pattern 'org\.h2\.server\.web'
python check.py
```

## 约定

- 工具不输出"高危""疑似"这类判定词，只输出候选和理由。
- 只读工具不写文件；需要落盘时提供 `--dry-run`。
- 输入用 JSON 或命令行参数，不依赖包内 import 路径。
