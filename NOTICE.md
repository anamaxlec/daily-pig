# NOTICE / Attribution

`hermes-daily-pig` is a **Hermes Agent skill port** of the HoshinoBot / NoneBot
“今日小猪 / 今天是什么小猪” plugin ecosystem. It is **not** an official product
of the original authors, and it is **not** affiliated with PigHub beyond using
its public catalog/API as an optional image source.

## Upstream projects

| Project | Role | Link |
|---------|------|------|
| **nonebot-plugin-rollpig** | Original idea & local pig roster tradition | https://github.com/Bearlele/nonebot-plugin-rollpig |
| **huannai_plugin_rollpig** | HoshinoBot port we forked from (commands, `pig.json`, local art, PigHub refresh) | https://github.com/SonderXiaoming/huannai_plugin_rollpig |
| **PigHub** | Large online pig image gallery (`pighub.top`) | https://pighub.top |

Original plugin license: MIT (Copyright (c) 2025 Bear_lele), preserved in `LICENSE`.

## What we changed (relative to huannai_plugin_rollpig)

This is a **rewrite for Hermes**, not a drop-in HoshinoBot module:

1. **Removed** NoneBot / HoshinoBot service wiring (`Service`, `CQEvent`, `MessageSegment`, `pic2b64`, scheduled jobs inside the bot process).
2. **Added** a standalone CLI: `skills/daily-pig/scripts/daily_pig.py` with subcommands `today` / `random` / `find` / `refresh` / `list` / `show`.
3. **Default `today` source is PigHub** (sticky once per user per day). Classic local 62-pig roster remains available via `today --local` (with `description` + `analysis`).
4. **Image URL fix**: catalog entries expose `/data/{filename}` paths, but public files are served under `https://pighub.top/images/{filename}` — the CLI uses `/images/` for download/display.
5. **State location**: daily sticky cache and hub downloads live under `$HERMES_HOME/daily-pig/` (not inside the skill tree), so skill updates do not wipe user draws.
6. **Agent delivery**: stdout includes human text + `MEDIA:/abs/path` lines for Telegram/gateway image send, plus a `<!--DAILY_PIG_JSON-->` trailer for machine parsing.
7. **Packaging**: Hermes `SKILL.md` + install-as-skill layout; README/docs assets for gallery showcase.

Local roster JSON and classic PNG art in `skills/daily-pig/resource/` are carried over from the upstream plugin resource set (with gratitude). Online gallery content remains on PigHub; README hub samples under `docs/assets/hub/` are illustrative snapshots only.

## Please go star the originals

If you enjoy this skill, please also star / support the upstream repos and PigHub creators. We only moved the pigs into Hermes — they built the pigsty.
