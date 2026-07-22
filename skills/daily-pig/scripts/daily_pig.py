#!/usr/bin/env python3
"""Daily Pig (今日小猪) — agent-agnostic CLI port of huannai_plugin_rollpig.

Commands:
  today   [--user ID] [--local] [--no-download]
                        Draw today's pig from PigHub (sticky once/day)
                        --local uses the classic 62-pig local roster instead
  random                Random pig from PigHub cache
  find KEYWORD [--limit N]  Search PigHub by title keyword
  refresh               Refresh PigHub catalog from pighub.top
  list                  List local pig roster
  show ID               Show a local pig by id
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).resolve().parent.parent
RES_DIR = SKILL_DIR / "resource"
PIGINFO_PATH = RES_DIR / "pig.json"
PIG_HUB_PATH = RES_DIR / "pig_hub.json"
IMAGE_DIR = RES_DIR / "image"
PIGHUB_API = "https://pighub.top/api/all-images"
# Public image CDN path (catalog thumbnails use /data/… but files are served under /images/)
PIGHUB_DATA = "https://pighub.top/images/"


def state_dir() -> Path:
    """Runtime cache dir (sticky today draws + hub downloads).

    Priority:
      1) DAILY_PIG_HOME
      2) ~/.daily-pig  (agent-agnostic default)
      3) legacy $HERMES_HOME/daily-pig if it already exists (smooth migration)
    """
    if os.environ.get("DAILY_PIG_HOME"):
        d = Path(os.environ["DAILY_PIG_HOME"]).expanduser()
    else:
        default = Path.home() / ".daily-pig"
        legacy = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes")).expanduser() / "daily-pig"
        d = legacy if (not default.exists() and legacy.exists()) else default
    d.mkdir(parents=True, exist_ok=True)
    return d


def today_cache_path() -> Path:
    return state_dir() / "today.json"


def hub_cache_dir() -> Path:
    d = state_dir() / "hub-images"
    d.mkdir(parents=True, exist_ok=True)
    return d


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def find_image_file(pig_id: str) -> Path | None:
    for ext in ("png", "jpg", "jpeg", "webp", "gif"):
        p = IMAGE_DIR / f"{pig_id}.{ext}"
        if p.exists():
            return p
    return None


def emit(obj: dict[str, Any], human: str | None = None) -> int:
    """Print human text (for agent/user) then a machine JSON trailer."""
    if human:
        print(human.rstrip())
        print()
    print("<!--DAILY_PIG_JSON-->")
    print(json.dumps(obj, ensure_ascii=False, indent=2))
    return 0 if obj.get("ok", False) else 1


def load_pigs() -> list[dict[str, Any]]:
    pigs = load_json(PIGINFO_PATH, [])
    if not isinstance(pigs, list) or not pigs:
        raise SystemExit("猪圈空荡荡：resource/pig.json 缺失或为空")
    return pigs


def cmd_list(_: argparse.Namespace) -> int:
    pigs = load_pigs()
    lines = [f"本地小猪名册（{len(pigs)} 头）："]
    for p in pigs:
        lines.append(f"- {p.get('id')}: {p.get('name')} — {p.get('description')}")
    return emit(
        {"ok": True, "mode": "list", "count": len(pigs), "pigs": pigs},
        "\n".join(lines),
    )


def cmd_show(args: argparse.Namespace) -> int:
    pigs = load_pigs()
    pig = next((p for p in pigs if p.get("id") == args.id or p.get("name") == args.id), None)
    if not pig:
        return emit({"ok": False, "error": f"找不到小猪: {args.id}"}, f"找不到小猪：{args.id}")
    img = find_image_file(pig["id"])
    human = format_local_pig(pig, img, header="这是：")
    return emit(
        {
            "ok": True,
            "mode": "show",
            "pig": pig,
            "image_path": str(img) if img else None,
            "media_hint": f"MEDIA:{img}" if img else None,
        },
        human,
    )


def format_local_pig(pig: dict[str, Any], img: Path | None, header: str = "今日你是：") -> str:
    lines = [
        f"{header}{pig.get('name', '?')}",
        pig.get("description", ""),
        f"分析：{pig.get('analysis', '')}",
    ]
    if img:
        lines.append("")
        lines.append(f"MEDIA:{img}")
    else:
        lines.append("")
        lines.append("（未找到本地图片）")
    return "\n".join(lines)


def format_hub_pig(
    pig: dict[str, Any],
    *,
    img: Path | None,
    url: str,
    header: str = "今日你是：",
) -> str:
    title = pig.get("title") or pig.get("filename") or "?"
    lines = [
        f"{header}{title}",
        "来源：PigHub",
        f"URL：{url}",
    ]
    if img:
        lines += ["", f"MEDIA:{img}"]
    else:
        lines += ["", f"![{title}]({url})"]
    return "\n".join(lines)


def is_hub_pig_record(pig: Any) -> bool:
    """True if cached record looks like a PigHub image entry (not local roster)."""
    if not isinstance(pig, dict):
        return False
    if pig.get("title") or pig.get("thumbnail") or pig.get("filename"):
        return True
    # local roster has name+analysis and no hub fields
    return False


def ensure_hub_images(auto_refresh: bool = True) -> list[dict[str, Any]]:
    images = hub_images()
    if images:
        return images
    if not auto_refresh:
        return []
    try:
        req = urllib.request.Request(PIGHUB_API, headers={"User-Agent": "hermes-daily-pig/1.0"})
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        if isinstance(data, dict) and data.get("images"):
            save_json(PIG_HUB_PATH, data)
            return list(data["images"])
    except Exception:
        pass
    return hub_images()


def cmd_today(args: argparse.Namespace) -> int:
    today_str = date.today().isoformat()
    user_id = str(
        args.user
        or os.environ.get("DAILY_PIG_USER")
        or os.environ.get("HERMES_USER_ID")  # optional legacy
        or "local"
    )
    use_local = bool(getattr(args, "local", False))
    source = "local" if use_local else "hub"

    cache = load_json(today_cache_path(), {"date": "", "source": "", "records": {}})
    if cache.get("date") != today_str or cache.get("source") != source:
        # New day or source mode switch (hub vs local) → reset sticky cache
        cache = {"date": today_str, "source": source, "records": {}}

    records = cache.setdefault("records", {})
    is_reroll = user_id in records

    if use_local:
        pigs = load_pigs()
        if is_reroll and not is_hub_pig_record(records[user_id]):
            pig = records[user_id]
        else:
            pig = random.choice(pigs)
            records[user_id] = pig
            save_json(today_cache_path(), cache)
            is_reroll = False
        img = find_image_file(pig["id"])
        prefix = "（今天已经抽过啦，还是这只）\n" if is_reroll else ""
        human = prefix + format_local_pig(pig, img)
        return emit(
            {
                "ok": True,
                "mode": "today",
                "source": "local",
                "date": today_str,
                "user": user_id,
                "is_repeat": is_reroll,
                "pig": pig,
                "image_path": str(img) if img else None,
                "media_hint": f"MEDIA:{img}" if img else None,
            },
            human,
        )

    # Default: PigHub today
    images = ensure_hub_images(auto_refresh=True)
    if not images:
        return emit(
            {"ok": False, "error": "PigHub 缓存为空且自动刷新失败"},
            "猪圈连不上 PigHub…请检查网络后执行 refresh，或临时用 today --local。",
        )

    if is_reroll and is_hub_pig_record(records[user_id]):
        pig = records[user_id]
    else:
        pig = random.choice(images)
        records[user_id] = pig
        save_json(today_cache_path(), cache)
        is_reroll = False

    url = hub_image_url(pig)
    local = None if getattr(args, "no_download", False) else download_hub_image(pig)
    prefix = "（今天已经抽过啦，还是这只）\n" if is_reroll else ""
    human = prefix + format_hub_pig(pig, img=local, url=url)
    return emit(
        {
            "ok": True,
            "mode": "today",
            "source": "hub",
            "date": today_str,
            "user": user_id,
            "is_repeat": is_reroll,
            "pig": pig,
            "image_url": url,
            "image_path": str(local) if local else None,
            "media_hint": f"MEDIA:{local}" if local else None,
        },
        human,
    )


def hub_images() -> list[dict[str, Any]]:
    data = load_json(PIG_HUB_PATH, {})
    images = data.get("images") if isinstance(data, dict) else None
    if not images:
        return []
    return images


def hub_image_url(pig: dict[str, Any]) -> str:
    thumb = pig.get("thumbnail") or pig.get("filename") or ""
    name = str(thumb).split("/")[-1]
    return PIGHUB_DATA + urllib.parse.quote(name)


def download_hub_image(pig: dict[str, Any], timeout: float = 20.0) -> Path | None:
    url = hub_image_url(pig)
    name = urllib.parse.unquote(url.rsplit("/", 1)[-1])
    # keep filesystem-safe
    safe = "".join(c if c.isalnum() or c in "._-()（）" else "_" for c in name)[:180]
    dest = hub_cache_dir() / safe
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "hermes-daily-pig/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
        if not data:
            return None
        dest.write_bytes(data)
        return dest
    except Exception:
        return None


def cmd_random(args: argparse.Namespace) -> int:
    images = hub_images()
    if not images:
        return emit(
            {"ok": False, "error": "PigHub 缓存为空，请先 refresh"},
            "猪圈空荡荡…先执行 refresh 拉一下 PigHub。",
        )
    pig = random.choice(images)
    url = hub_image_url(pig)
    local = None if args.no_download else download_hub_image(pig)
    title = pig.get("title") or pig.get("filename") or "随机小猪"
    lines = [f"随机小猪：{title}", f"来源：PigHub", f"URL：{url}"]
    if local:
        lines += ["", f"MEDIA:{local}"]
    else:
        lines += ["", f"![{title}]({url})"]
    return emit(
        {
            "ok": True,
            "mode": "random",
            "pig": pig,
            "image_url": url,
            "image_path": str(local) if local else None,
            "media_hint": f"MEDIA:{local}" if local else None,
        },
        "\n".join(lines),
    )


def cmd_find(args: argparse.Namespace) -> int:
    images = hub_images()
    if not images:
        return emit(
            {"ok": False, "error": "PigHub 缓存为空，请先 refresh"},
            "猪圈空荡荡…先执行 refresh 拉一下 PigHub。",
        )
    kw = (args.keyword or "").strip().lower()
    if not kw:
        return emit({"ok": False, "error": "缺少关键词"}, "用法：find <关键词>")
    found = [p for p in images if kw in str(p.get("title", "")).lower()]
    if not found:
        return emit(
            {"ok": False, "mode": "find", "keyword": kw, "count": 0, "results": []},
            "你要找的猪仔离家出走了~",
        )
    limit = max(1, min(int(args.limit or 8), 8))
    picks = found[:limit]
    lines = [f"找到 {len(found)} 头相关小猪，展示前 {len(picks)} 头："]
    results = []
    for pig in picks:
        url = hub_image_url(pig)
        title = pig.get("title") or "?"
        local = None if args.no_download else download_hub_image(pig)
        entry = {
            "title": title,
            "image_url": url,
            "image_path": str(local) if local else None,
            "media_hint": f"MEDIA:{local}" if local else None,
            "pig": pig,
        }
        results.append(entry)
        lines.append(f"- {title}")
        if local:
            lines.append(f"MEDIA:{local}")
        else:
            lines.append(f"![{title}]({url})")
    return emit(
        {
            "ok": True,
            "mode": "find",
            "keyword": kw,
            "count": len(found),
            "shown": len(picks),
            "results": results,
        },
        "\n".join(lines),
    )


def cmd_refresh(_: argparse.Namespace) -> int:
    try:
        req = urllib.request.Request(PIGHUB_API, headers={"User-Agent": "hermes-daily-pig/1.0"})
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return emit({"ok": False, "error": str(e)}, f"刷新失败：{e}")

    images = data.get("images") if isinstance(data, dict) else None
    if not images:
        return emit({"ok": False, "error": "no images"}, "刷新失败，PigHub 中找不到猪猪。")

    save_json(PIG_HUB_PATH, data)
    total = data.get("total", len(images))
    return emit(
        {"ok": True, "mode": "refresh", "total": total, "count": len(images)},
        f"成功从 PigHub 刷新 {len(images)} 头猪猪（total={total}）",
    )


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="今日小猪 / Daily Pig (agent-agnostic CLI)")
    sub = p.add_subparsers(dest="cmd", required=True)

    t = sub.add_parser("today", help="抽取今日小猪（默认 PigHub，每人每天固定）")
    t.add_argument("--user", default=None, help="用户 ID（默认 local / DAILY_PIG_USER）")
    t.add_argument(
        "--local",
        action="store_true",
        help="改用本地 62 种小猪池（带 description/analysis）",
    )
    t.add_argument("--no-download", action="store_true", help="Hub 模式不下载，只返回 URL")
    t.set_defaults(func=cmd_today)

    r = sub.add_parser("random", help="随机 PigHub 小猪图")
    r.add_argument("--no-download", action="store_true", help="不下载，只返回 URL")
    r.set_defaults(func=cmd_random)

    f = sub.add_parser("find", help="按关键词找猪")
    f.add_argument("keyword")
    f.add_argument("--limit", type=int, default=8)
    f.add_argument("--no-download", action="store_true")
    f.set_defaults(func=cmd_find)

    ref = sub.add_parser("refresh", help="刷新 PigHub 目录")
    ref.set_defaults(func=cmd_refresh)

    ls = sub.add_parser("list", help="列出本地小猪")
    ls.set_defaults(func=cmd_list)

    s = sub.add_parser("show", help="展示指定本地小猪")
    s.add_argument("id")
    s.set_defaults(func=cmd_show)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
