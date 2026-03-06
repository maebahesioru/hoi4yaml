from .clausewitz import to_clausewitz
from .utils import write
from .shorthands import expand_shorthands, expand_events
from .gamedata import resolve_game_refs


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
            raw = {k: v for k, v in entry.items() if not k.startswith("_")}
            data = expand_shorthands(resolve_game_refs({"ideas": {cat: raw}}))
        elif "_wrap" in entry:
            wrap = entry["_wrap"]
            raw = {k: v for k, v in entry.items() if not k.startswith("_")}
            data = expand_shorthands(resolve_game_refs({wrap: raw}))
        else:
            data = expand_shorthands(resolve_game_refs({k: v for k, v in entry.items() if not k.startswith("_")}))
        if data:
            parts.append(to_clausewitz(data))
        write(mod_dir / subdir / f"{filename}.{ext}", "\n".join(parts) + "\n", **kw)


ALL_LANGS = ["english", "french", "german", "spanish", "russian", "polish", "braz_por", "japanese", "korean"]


def gen_localisation(mod_dir, loc, **kw):
    if loc and isinstance(next(iter(loc.values())), dict):
        english = loc.get("english", {})
        # auto-fill all languages not explicitly specified
        langs = {lang: loc.get(lang, {}) for lang in ALL_LANGS}
        for lang, entries in langs.items():
            merged = {**english, **entries} if lang != "english" else entries
            if not merged:
                continue
            lines = [f"l_{lang}:"] + [f' {k}:0 "{v}"' for k, v in merged.items()]
            write(mod_dir / "localisation" / f"mod_l_{lang}.yml", "\n".join(lines) + "\n", **kw)
    else:
        lines = ["l_english:"] + [f' {k}:0 "{v}"' for k, v in loc.items()]
        write(mod_dir / "localisation" / "mod_l_english.yml", "\n".join(lines) + "\n", **kw)
