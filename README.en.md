# Axiom

> Tools rotate. Axioms don't.

[中文版](README.md) · [MIT](LICENSE) · [intro video](assets/axiom-intro.mp4) · [script](assets/axiom-intro-script.md)

What gets lost in reverse engineering isn't tooling, it's the bar for believing a result. A scanner prints hits, a decompiler prints pseudocode, a teardown reads beautifully — none of that tells you which line is a finding.

Axiom writes the axioms down before it ships any tool. **A claim carries its evidence and its limits; a hit survives a control experiment; an inference says it's an inference.** These aren't best practices, they're the premises every module shares, in `docs/evidence.md` and `docs/verification.md`. Scripts produce raw material you can re-check, not verdicts. Swap a tool whenever you like; changing an axiom means changing the whole repo.

## Two projects, one repo

- **REA** (`targets/native/`) — the binary side. What it actually takes to run Ghidra headless on Windows: prebuilt `.sla` files forcing a recompile, install dirs that refuse writes, and an oversized inherited environment blowing up `CreateProcess` with Win32 87. The MCP launcher that strips those variables lives here, and so does the claim / evidence / limits rule.
- **Reverse Engineering Agent** (`targets/product/`) — the system side. Four-layer teardown, five-axis validation, and a three-step workflow (scan → pick a direction → go deep) that keeps facts, inferences and confidence in separate columns.

One answers "what's inside this program", the other "how was this thing put together". Their duplicate evidence rules are now `docs/`, their workflow is `core/`. Merged, not parked side by side.

## What else came in

Two earlier public repos were mined for parts worth keeping. `ReverseKit`'s six modules were regrouped by target — web probing, APK static checks, ELF analysis, false-positive defenses, evidence capture, self-check. `IronCore`'s habit of proving a change on the wire became `toolkit/verify_armor.py`. REA's six upstream target guides are kept verbatim in `docs/reference/`. Only portable, target-agnostic methods made the cut: no live targets, vendor lists or samples.

## Layout

| Path | What lives there |
| --- | --- |
| `core/` | three-step workflow, and the target → first tool → evidence shape table |
| `targets/native/` | PE / ELF / native binaries, Ghidra-on-Windows notes, MCP launcher |
| `targets/mobile/` | APK unpacking, resource and syntax checks, emulator acceptance |
| `targets/web/` | black-box probing, soft-404 and JSONP judgement, five false-positive guards |
| `targets/product/` | product and stack teardown, ratings, anti-hallucination labels |
| `toolkit/` | evidence capture, hit verification, effect verification, self-check |
| `docs/` | evidence and verification rules, module template, REA upstream guides |

Mostly standard library, Python 3.9+. `python check.py` runs compile, CLI smoke tests and an asset/secret guard; CI runs the same file.

```bash
python check.py                       # full self-check
python check.py --quick               # enough after a string edit
python toolkit/verify_hit.py -h       # put any hit through a control first
```

## Adding the next project

1. `cp -r targets/_template targets/<name>` — write down the target type, what counts as evidence, how to reproduce it.
2. Add one row to `core/routing.md`: target → first tool → evidence shape.
3. Put scripts under `tools/`, make `-h` self-explanatory, give writes a `--dry-run`.
4. Run `python check.py`, then open a PR.

Don't start a new top-level tree and don't fork the axioms. Fit new work into one of the four layers; if it doesn't fit, that's the discussion for a fifth. Full rules in [CONTRIBUTING.md](CONTRIBUTING.md).

## Scope

Methods, decision rules and reproducible scripts only. No real targets, vendor lists, samples or credentials. Use it on things you're allowed to analyze.

## License

MIT. Upstream material keeps its own licenses; see [docs/reference/README.md](docs/reference/README.md).
