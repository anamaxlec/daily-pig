# NOTICE / Attribution

`daily-pig` is an **agent-agnostic CLI skill port** of the HoshinoBot / NoneBot
“今日小猪 / 今天是什么小猪” plugin ecosystem. It is **not** an official product
of the original authors, and it is **not** affiliated with PigHub beyond using
its public catalog/API as an optional image source.

Works anywhere you can run `python3` + shell: Claude Code, Codex, OpenCode, Pi,
Cursor, Hermes, plain terminal, etc.

## Upstream projects

| Project | Role | Link |
|---------|------|------|
| **nonebot-plugin-rollpig** | Original idea & local pig roster tradition | https://github.com/Bearlele/nonebot-plugin-rollpig |
| **huannai_plugin_rollpig** | HoshinoBot port we adapted from (commands, `pig.json`, local art, PigHub refresh) | https://github.com/SonderXiaoming/huannai_plugin_rollpig |
| **PigHub** | Large online pig image gallery (`pighub.top`) | https://pighub.top |

Original plugin license: MIT (Copyright (c) 2025 Bear_lele), preserved in `LICENSE`.

## What we changed (relative to huannai_plugin_rollpig)

This is a **rewrite as a standalone skill/CLI**, not a drop-in HoshinoBot module:

1. **Removed** NoneBot / HoshinoBot service wiring (`Service`, `CQEvent`, `MessageSegment`, `pic2b64`, bot-process cron).
2. **Added** a standalone CLI: `skills/daily-pig/scripts/daily_pig.py` (`today` / `random` / `find` / `refresh` / `list` / `show`).
3. **Default `today` source is PigHub** (sticky once per user per day). Classic local 62-pig roster remains via `today --local` (with `description` + `analysis`).
4. **Image URL fix**: catalog exposes `/data/{filename}`; public files are under `https://pighub.top/images/{filename}`.
5. **State location**: `~/.daily-pig/` (override with `DAILY_PIG_HOME`), outside the skill tree.
6. **Agent delivery**: human text + `MEDIA:/abs/path` + `<!--DAILY_PIG_JSON-->` trailer — any agent that can run shell can parse it.
7. **Packaging**: portable `SKILL.md` + multi-agent install paths; original README branding/logo replaced with an original SVG hero (not the upstream `PigLogo`).

Local roster JSON and classic PNG art in `skills/daily-pig/resource/` are carried over from the upstream plugin resource set (with gratitude). Online gallery content remains on PigHub; README hub samples under `docs/assets/hub/` are illustrative snapshots only.

## Please go star the originals

If you enjoy this skill, please also star / support the upstream repos and PigHub creators. We only moved the pigs into a CLI skill — they built the pigsty.
