from .clausewitz import to_clausewitz
from .utils import write
from .shorthands import expand_shorthands, expand_events
from .gamedata import resolve_game_refs


from .icons import guess_icon, guess_picture


def _auto_picture(ideas_dict):
    """Auto-set picture for ideas missing picture."""
    for k, v in ideas_dict.items():
        if isinstance(v, dict) and "picture" not in v:
            guessed = guess_picture(k) or guess_icon(k)
            v["picture"] = guessed if guessed else f"GFX_idea_{k}"
    return ideas_dict


def _auto_icon(decisions_dict):
    """Auto-set icon = generic_political_discourse for decisions missing icon."""
    for k, v in decisions_dict.items():
        if isinstance(v, dict) and "icon" not in v:
            v["icon"] = "generic_political_discourse"
    return decisions_dict


def gen_section(mod_dir, entries, subdir, ext="txt", **kw):
    if subdir == "events":
        entries = expand_events(entries)
    for entry in entries:
        filename = entry.get("_file", "generated")
        parts = []
        namespace = entry.get("_namespace", filename)
        has_event = any(k in entry for k in ("country_event", "news_event", "state_event"))
        if has_event:
            parts.append(f"add_namespace = {namespace}\n")
        if "_category" in entry:
            cat = entry["_category"]
            raw = _auto_picture({k: v for k, v in entry.items() if not k.startswith("_")})
            data = expand_shorthands(resolve_game_refs({"ideas": {cat: raw}}))
        elif "_wrap" in entry:
            wrap = entry["_wrap"]
            raw = {k: v for k, v in entry.items() if not k.startswith("_")}
            data = expand_shorthands(resolve_game_refs({wrap: raw}))
        else:
            raw = {k: v for k, v in entry.items() if not k.startswith("_")}
            # auto-set picture for ideas, icon for decisions
            if subdir.startswith("common/ideas"):
                for cat_val in raw.values():
                    if isinstance(cat_val, dict):
                        _auto_picture(cat_val)
            if subdir.startswith("common/decisions") and not subdir.endswith("categories"):
                for cat_val in raw.values():
                    if isinstance(cat_val, dict):
                        _auto_icon(cat_val)
            data = expand_shorthands(resolve_game_refs(raw))
        if data:
            parts.append(to_clausewitz(data))
        write(mod_dir / subdir / f"{filename}.{ext}", "\n".join(parts) + "\n", **kw)


ALL_LANGS = ["english", "french", "german", "spanish", "russian", "polish", "braz_por", "japanese", "korean"]


def _get_all_langs():
    from .gamedata import find_hoi4_path
    hoi4 = find_hoi4_path()
    if hoi4:
        p = hoi4 / "localisation" / "languages.yml"
        if p.exists():
            import re
            return re.findall(r'^l_(\w+):', p.read_text(encoding="utf-8-sig"), re.MULTILINE)
    return ALL_LANGS


def gen_localisation(mod_dir, loc, **kw):
    if loc and isinstance(next(iter(loc.values())), dict):
        english = loc.get("english") or next(iter(loc.values()), {})
        # auto-fill all languages not explicitly specified
        langs = {lang: loc.get(lang, {}) for lang in _get_all_langs()}
        for lang, entries in langs.items():
            merged = {**english, **entries} if lang != "english" else entries
            if not merged:
                continue
            lines = [f"l_{lang}:"] + [f' {k}:0 "{v}"' for k, v in merged.items()]
            write(mod_dir / "localisation" / f"mod_l_{lang}.yml", "\n".join(lines) + "\n", **kw)
    else:
        lines = ["l_english:"] + [f' {k}:0 "{v}"' for k, v in loc.items()]
        write(mod_dir / "localisation" / "mod_l_english.yml", "\n".join(lines) + "\n", **kw)
