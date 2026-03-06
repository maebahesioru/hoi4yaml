import re
from collections import Counter, defaultdict
from .gamedata import _load_cache, _save_cache, find_hoi4_path

ICON_HINTS_FALLBACK = {
    "industry": "GFX_focus_generic_industry_1",
    "factory":  "GFX_focus_generic_industry_2",
    "manpower": "GFX_focus_generic_manpower",
    "army":     "GFX_focus_generic_manpower",
    "rearm":    "GFX_focus_generic_military_mission",
    "military": "GFX_focus_generic_military_mission",
    "tank":     "GFX_focus_generic_army_tank",
    "armor":    "GFX_focus_generic_army_tank",
    "artillery":"GFX_focus_generic_army_artillery",
    "motorized":"GFX_focus_generic_army_motorized",
    "air":      "GFX_focus_generic_air_fighter",
    "fighter":  "GFX_focus_generic_air_fighter",
    "bomber":   "GFX_focus_generic_air_bomber",
    "navy":     "GFX_focus_generic_navy_cruiser",
    "naval":    "GFX_focus_generic_navy_cruiser",
    "submarine":"GFX_focus_generic_navy_submarine",
    "carrier":  "GFX_focus_generic_navy_carrier",
    "battleship":"GFX_focus_generic_navy_battleship",
    "political":"GFX_focus_generic_political_support",
    "fascism":  "GFX_focus_generic_political_fascism",
    "communism":"GFX_focus_generic_political_communism",
    "democracy":"GFX_focus_generic_political_democracy",
    "alliance": "GFX_focus_generic_alliance",
    "annex":    "GFX_focus_generic_annexation",
    "trade":    "GFX_focus_generic_trade",
    "research": "GFX_focus_generic_research",
    "radar":    "GFX_focus_generic_radar",
    "nuclear":  "GFX_focus_generic_nuclear",
    "rocket":   "GFX_focus_generic_rocket",
    "oil":      "GFX_focus_generic_oil",
    "steel":    "GFX_focus_generic_steel",
    "rubber":   "GFX_focus_generic_rubber",
    "fort":     "GFX_focus_generic_fortification",
    "defense":  "GFX_focus_generic_home_defense",
    "propaganda":"GFX_focus_generic_war_propaganda",
    "pp":       "GFX_focus_generic_pp_unity_bonus",
    "unity":    "GFX_focus_generic_pp_unity_bonus",
    "diplo":    "GFX_focus_generic_diplomatic_support",
    "support":  "GFX_focus_generic_diplomatic_support",
    "secret":   "GFX_focus_generic_secret_weapon",
}

_SKIP_WORDS = {"generic", "gfx", "focus", "idea", "spirit", "1", "2", "3"}
_icon_hints = None
_focus_icons = {}
_focus_loc_words = {}
_mod_localisation = {}


def learn_icon_hints(hoi4_path):
    word_icon = defaultdict(Counter)
    focus_icons = {}
    for f in (hoi4_path / "common/national_focus").glob("*.txt"):
        text = f.read_text(encoding="utf-8-sig", errors="ignore")
        for m in re.finditer(
            r'focus\s*=\s*\{[^{}]*?id\s*=\s*(\S+)[^{}]*?icon\s*=\s*(GFX_focus_generic_\S+)',
            text, re.DOTALL
        ):
            fid, icon = m.group(1), m.group(2)
            focus_icons[fid.lower()] = icon
            words = [w for w in fid.lower().split("_")[1:] if w and w not in _SKIP_WORDS]
            for word in words:
                word_icon[word][icon] += 1
            for i in range(len(words) - 1):
                word_icon[f"{words[i]}_{words[i+1]}"][icon] += 1

    focus_loc_words = {}
    loc_dir = hoi4_path / "localisation" / "english"
    if not loc_dir.exists():
        loc_dir = hoi4_path / "localisation"
    for f in loc_dir.rglob("*.yml"):
        try:
            text = f.read_text(encoding="utf-8-sig", errors="ignore")
        except Exception:
            continue
        for m in re.finditer(r'^\s*(\w+):0\s+"([^"]+)"', text, re.MULTILINE):
            key = m.group(1).lower()
            if key in focus_icons:
                words = frozenset(
                    w.lower() for w in re.findall(r'\b[a-zA-Z]{4,}\b', m.group(2))
                    if w.lower() not in _SKIP_WORDS
                )
                if words:
                    focus_loc_words[key] = words
                    for word in words:
                        word_icon[word][focus_icons[key]] += 1

    word_hints = {w: c.most_common(1)[0][0] for w, c in word_icon.items()}
    return word_hints, focus_icons, focus_loc_words


def get_icon_hints():
    global _icon_hints, _focus_icons, _focus_loc_words
    if _icon_hints is None:
        cache = _load_cache()
        if cache and "icon_hints" in cache:
            _icon_hints = cache["icon_hints"]
            _focus_icons = cache.get("focus_icons", {})
            _focus_loc_words = {k: frozenset(v) for k, v in cache.get("focus_loc_words", {}).items()}
        else:
            hoi4 = find_hoi4_path()
            if hoi4:
                _icon_hints, _focus_icons, _focus_loc_words = learn_icon_hints(hoi4)
                c = _load_cache() or {}
                c.update({"icon_hints": _icon_hints, "focus_icons": _focus_icons,
                          "focus_loc_words": {k: list(v) for k, v in _focus_loc_words.items()}})
                _save_cache(c)
            else:
                _icon_hints, _focus_icons, _focus_loc_words = ICON_HINTS_FALLBACK, {}, {}
    return _icon_hints


_idea_hints = None


def learn_idea_hints(hoi4_path):
    """Learn word→picture mapping from game idea files + localisation."""
    word_pic = defaultdict(Counter)
    idea_pics = {}  # idea_id → picture
    for f in (hoi4_path / "common/ideas").glob("*.txt"):
        text = f.read_text(encoding="utf-8-sig", errors="ignore")
        for m in re.finditer(
            r'(\w+)\s*=\s*\{[^{}]*?picture\s*=\s*(generic_\S+)',
            text, re.DOTALL
        ):
            idea_id, pic = m.group(1).lower(), m.group(2)
            idea_pics[idea_id] = pic
            words = [w for w in idea_id.split("_") if w and w not in _SKIP_WORDS and len(w) > 3]
            for word in words:
                word_pic[word][pic] += 1
            for i in range(len(words) - 1):
                word_pic[f"{words[i]}_{words[i+1]}"][pic] += 1

    # also learn from localisation text
    idea_loc_words = {}
    loc_dir = hoi4_path / "localisation" / "english"
    if not loc_dir.exists():
        loc_dir = hoi4_path / "localisation"
    for f in loc_dir.rglob("*.yml"):
        try:
            text = f.read_text(encoding="utf-8-sig", errors="ignore")
        except Exception:
            continue
        for m in re.finditer(r'^\s*(\w+):0\s+"([^"]+)"', text, re.MULTILINE):
            key = m.group(1).lower()
            if key in idea_pics:
                words = frozenset(
                    w.lower() for w in re.findall(r'\b[a-zA-Z]{4,}\b', m.group(2))
                    if w.lower() not in _SKIP_WORDS
                )
                if words:
                    idea_loc_words[key] = words
                    for word in words:
                        word_pic[word][idea_pics[key]] += 1

    return {w: c.most_common(1)[0][0] for w, c in word_pic.items()}, idea_pics, idea_loc_words


_idea_loc_words = {}
_idea_pics = {}


def get_idea_hints():
    global _idea_hints, _idea_pics, _idea_loc_words
    if _idea_hints is None:
        cache = _load_cache()
        if cache and "idea_hints" in cache:
            _idea_hints = cache["idea_hints"]
            _idea_pics = cache.get("idea_pics", {})
            _idea_loc_words = {k: frozenset(v) for k, v in cache.get("idea_loc_words", {}).items()}
        else:
            hoi4 = find_hoi4_path()
            if hoi4:
                _idea_hints, _idea_pics, _idea_loc_words = learn_idea_hints(hoi4)
                c = _load_cache() or {}
                c.update({"idea_hints": _idea_hints, "idea_pics": _idea_pics,
                          "idea_loc_words": {k: list(v) for k, v in _idea_loc_words.items()}})
                _save_cache(c)
            else:
                _idea_hints, _idea_pics, _idea_loc_words = {}, {}, {}
    return _idea_hints


def guess_picture(idea_id):
    """Guess idea picture from localisation text + ID keywords."""
    hints = get_idea_hints()
    # semantic match via localisation text
    loc_text = _mod_localisation.get(idea_id, "")
    if loc_text and _idea_loc_words:
        query = frozenset(
            w.lower() for w in re.findall(r'\b[a-zA-Z]{4,}\b', loc_text)
            if w.lower() not in _SKIP_WORDS
        )
        if query:
            best_score, best_pic = 0.0, None
            for iid, iwords in _idea_loc_words.items():
                score = len(query & iwords) / len(query | iwords)
                if score > best_score:
                    best_score, best_pic = score, _idea_pics[iid]
            if best_score >= 0.15:
                return best_pic
    # keyword match via ID
    words = [w for w in idea_id.lower().split("_") if w not in _SKIP_WORDS and len(w) > 3]
    for i in range(len(words) - 1, 0, -1):
        if f"{words[i-1]}_{words[i]}" in hints:
            return hints[f"{words[i-1]}_{words[i]}"]
    for word in reversed(words):
        if word in hints:
            return hints[word]
    return None
    return _icon_hints


def guess_icon(focus_id):
    hints = get_icon_hints()
    loc_text = _mod_localisation.get(focus_id, "")
    if loc_text and _focus_loc_words:
        query = frozenset(
            w.lower() for w in re.findall(r'\b[a-zA-Z]{4,}\b', loc_text)
            if w.lower() not in _SKIP_WORDS
        )
        if query:
            best_score, best_icon = 0.0, None
            for fid, fwords in _focus_loc_words.items():
                score = len(query & fwords) / len(query | fwords)
                if score > best_score:
                    best_score, best_icon = score, _focus_icons[fid]
            if best_score >= 0.2:
                return best_icon
    words = [w for w in focus_id.lower().split("_")[1:] if w not in _SKIP_WORDS]
    for i in range(len(words) - 1, 0, -1):
        if f"{words[i-1]}_{words[i]}" in hints:
            return hints[f"{words[i-1]}_{words[i]}"]
    for word in reversed(words):
        if word in hints:
            return hints[word]
    return "GFX_focus_generic_political_support"


def auto_layout_focuses(focuses):
    prereq_map = {}
    for f in focuses:
        fid = f.get("id")
        if not fid:
            continue
        p = f.get("prereq")
        p_or = f.get("prereq_or")
        all_prereqs = (p if isinstance(p, list) else ([p] if p else [])) + \
                      (p_or if isinstance(p_or, list) else ([p_or] if p_or else []))
        prereq_map[fid] = all_prereqs

    children = defaultdict(list)
    roots = []
    for fid in prereq_map:
        parents = [p for p in prereq_map[fid] if p in prereq_map]
        if parents:
            children[parents[0]].append(fid)
        else:
            roots.append(fid)

    y_cache = {}
    def get_y(fid, seen=frozenset()):
        if fid in y_cache:
            return y_cache[fid]
        parents = [p for p in prereq_map.get(fid, []) if p in prereq_map and p not in seen]
        y = max((get_y(p, seen | {fid}) + 1 for p in parents), default=0)
        y_cache[fid] = y
        return y
    for fid in prereq_map:
        get_y(fid)

    x_map = {}
    for f in focuses:
        fid = f.get("id")
        if fid and ("x" in f or "rel_pos" in f):
            x_map[fid] = f.get("x", 0)

    counter = [0]
    fixed_ids = {f.get("id") for f in focuses if "x" in f or "rel_pos" in f}
    def assign_x(fid):
        kids = [k for k in children.get(fid, []) if k not in x_map]
        if fid in x_map:
            counter[0] = max(counter[0], x_map[fid] + 2)
            for kid in kids: assign_x(kid)
            return
        if not kids:
            x_map[fid] = counter[0]; counter[0] += 2
        else:
            for kid in kids: assign_x(kid)
            xs = [x_map[k] for k in children.get(fid, []) if k in x_map]
            if xs:
                center = (min(xs) + max(xs)) // 2
                x_map[fid] = center + (center % 2)
            else:
                x_map[fid] = counter[0]; counter[0] += 2

    for root in sorted(roots, key=lambda fid: x_map.get(fid, float('inf'))):
        assign_x(root)

    multi_prereq = {fid for fid in prereq_map
                    if len([p for p in prereq_map[fid] if p in prereq_map]) > 1}
    affected = set(multi_prereq)
    changed = True
    while changed:
        changed = False
        for fid in prereq_map:
            if fid not in affected:
                primary = next((p for p in prereq_map[fid] if p in prereq_map), None)
                if primary in affected:
                    affected.add(fid); changed = True
    for fid in sorted(affected, key=lambda f: y_cache.get(f, 0)):
        if fid in fixed_ids:
            continue
        parents = [p for p in prereq_map[fid] if p in x_map]
        if parents:
            ideal = sum(x_map[p] for p in parents) // len(parents)
            x_map[fid] = ideal + (ideal % 2)

    for f in focuses:
        fid = f.get("id")
        if fid and fid in x_map and "x" not in f and "rel_pos" not in f:
            f["x"] = x_map[fid]
            f["y"] = y_cache.get(fid, 0)
    return focuses
