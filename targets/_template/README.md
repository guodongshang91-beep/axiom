# 模板：新目标类型

> 这是扩展位。复制整个目录（`cp -r targets/_template targets/<name>`），不要修改模板本体。

## 目标类型

这一层处理什么对象、不处理什么。一句话说清边界。

## 首选工具

拿到对象后第一个跑什么，为什么是它。只列一个首选，其余放"备选"。

## 证据形态

结论靠什么材料支撑，引用 `docs/evidence.md`。典型形态：原始回显 / 伪代码与偏移 / 资源引用 / 公开行为线索。

## 复现方式

```bash
python targets/<name>/tools/example.py -h
```

写清命令、参数、预期输出，以及别人照着跑需要的环境版本。

## 已知局限

工具不支持什么、什么情况下结论不成立、哪些结论只能标成 inference。

---

接入规则见 `docs/module-template.md`；接入后记得在 `core/routing.md` 加一行。
