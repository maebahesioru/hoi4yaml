import re
import difflib
from pathlib import Path
from .utils import warn
from . import gamedata as _gd


def load_gfx_from_game(hoi4_path):
    gfx = set()
    for gfx_file in hoi4_path.glob("interface/*.gfx"):
        gfx.update(re.findall(r'name\s*=\s*"?(GFX_\w+)"?',
                               gfx_file.read_text(encoding="utf-8-sig", errors="ignore")))
    return gfx


def extract_mod_gfx(config):
    gfx = set()
    for entry in config.get("interface", []):
        for sprite in entry.get("sprites", []):
            if "name" in sprite:
                gfx.add(sprite["name"])
        st = entry.get("spriteTypes", {})
        for s in (st.get("spriteType") or []):
            if isinstance(s, dict) and "name" in s:
                gfx.add(s["name"])
    return gfx


def extract_mod_states(config):
    state_map = {}
    for entry in config.get("history_states", []):
        state = entry.get("state", {})
        sid = state.get("id")
        name = state.get("name", "")
        if sid and name.startswith("STATE_"):
            loc = config.get("localisation", {})
            if isinstance(next(iter(loc.values()), None), dict):
                loc = loc.get("english", {})
            human = loc.get(name, "").lower()
            if human:
                state_map[human] = int(sid)
    return state_map


def load_extra_mod_paths(mod_paths):
    extra_gfx = set()
    extra_states = {}
    extra_loc_keys = set()
    extra_traits = set()
    extra_ideologies = set()
    for path_str in (mod_paths or []):
        p = Path(path_str).expanduser()
        if not p.exists():
            warn(f"mod_path not found: {p}"); continue
        for f in p.glob("interface/*.gfx"):
            extra_gfx.update(re.findall(r'name\s*=\s*"?(GFX_\w+)"?',
                f.read_text(encoding="utf-8-sig", errors="ignore")))
        for f in (p / "history/states").glob("*.txt") if (p / "history/states").exists() else []:
            text = f.read_text(encoding="utf-8-sig", errors="ignore")
            id_m  = re.search(r'\bid\s*=\s*(\d+)', text)
            key_m = re.search(r'\bname\s*=\s*"(STATE_\d+)"', text)
            if id_m and key_m:
                extra_states[key_m.group(1)] = int(id_m.group(1))
        for f in p.glob("localisation/**/*.yml"):
            for m in re.finditer(r'^\s*(\S+):\d+\s+"', f.read_text(encoding="utf-8-sig", errors="ignore"), re.MULTILINE):
                extra_loc_keys.add(m.group(1))
        for trait_dir in ("common/country_leader", "common/unit_leader"):
            for f in (p / trait_dir).glob("*.txt") if (p / trait_dir).exists() else []:
                text = f.read_text(encoding="utf-8-sig", errors="ignore")
                for block in re.findall(r'leader_traits\s*=\s*\{(.+?)^\}', text, re.DOTALL | re.MULTILINE):
                    for m in re.finditer(r'^\t(\w+)\s*=\s*\{', block, re.MULTILINE):
                        extra_traits.add(m.group(1))
        for f in (p / "common/ideologies").glob("*.txt") if (p / "common/ideologies").exists() else []:
            text = f.read_text(encoding="utf-8-sig", errors="ignore")
            for m in re.finditer(r'^\s*(\w+)\s*=\s*\{', text, re.MULTILINE):
                extra_ideologies.add(m.group(1))
    return extra_gfx, extra_states, extra_loc_keys, extra_traits, extra_ideologies


def validate(config):
    known_gfx = set()
    hoi4_path = _gd.find_hoi4_path()
    if hoi4_path:
        known_gfx = load_gfx_from_game(hoi4_path)
    known_gfx |= extract_mod_gfx(config)
    extra_gfx, _, extra_loc_keys, extra_traits, extra_ideologies = load_extra_mod_paths(
        config.get("mod", {}).get("mod_paths", []))
    known_gfx |= extra_gfx

    _gd.get_game_maps()
    if extra_traits and _gd._trait_set is not None:
        _gd._trait_set.update(extra_traits)
        if _gd._country_leader_trait_set is not None:
            _gd._country_leader_trait_set.update(extra_traits)
        if _gd._unit_leader_trait_set is not None:
            _gd._unit_leader_trait_set.update(extra_traits)
    if extra_ideologies and _gd._ideology_set is not None:
        _gd._ideology_set.update(extra_ideologies)

    loc = config.get("localisation", {})
    loc_keys = set()
    if loc and isinstance(next(iter(loc.values())), dict):
        for entries in loc.values():
            loc_keys.update(entries.keys())
    else:
        loc_keys.update(loc.keys())
    loc_keys |= extra_loc_keys

    focus_ids = []
    for entry in config.get("national_focus", []):
        for focus in (entry.get("focus_tree") or {}).get("focus", []):
            focus_ids.append(focus.get("id"))
            icon = focus.get("icon")
            if icon and known_gfx and icon not in known_gfx:
                warn(f"Unknown GFX key: {icon}")
    for d in {x for x in focus_ids if focus_ids.count(x) > 1}:
        warn(f"Duplicate focus id: {d}")

    referenced_event_ids = set()
    def _collect_all_event_refs(d):
        if isinstance(d, list):
            for i in d: _collect_all_event_refs(i)
        elif isinstance(d, dict):
            for k, v in d.items():
                if k in ("country_event", "news_event", "state_event", "random_events"):
                    if isinstance(v, (str, int)):
                        referenced_event_ids.add(str(v))
                    elif isinstance(v, dict) and "id" in v:
                        referenced_event_ids.add(str(v["id"]))
                    else:
                        _collect_all_event_refs(v)
                else:
                    _collect_all_event_refs(v)
    _collect_all_event_refs(config)

    event_ids = []
    for entry in config.get("events", []):
        for etype in ("country_event", "news_event", "state_event"):
            for ev in (entry.get(etype) or []):
                event_ids.append(ev.get("id"))
                eid = str(ev.get("id", ""))
                if (not ev.get("is_triggered_only") and not ev.get("mean_time_to_happen")
                        and eid not in referenced_event_ids):
                    warn(f"Event '{eid}' has neither 'is_triggered_only' nor 'mean_time_to_happen' — it will never fire")
                for key in ("title", "desc"):
                    val = ev.get(key)
                    if val and val not in loc_keys:
                        warn(f"Missing localisation: {val}")
                for opt in (ev.get("option") or []):
                    name = opt.get("name")
                    if not name:
                        warn(f"Event '{ev.get('id')}' has an option without 'name' — localisation key required")
                    elif name not in loc_keys:
                        warn(f"Missing localisation: {name}")
    for d in {x for x in event_ids if event_ids.count(x) > 1}:
        warn(f"Duplicate event id: {d}")

    if _gd._ideology_set or _gd._trait_set or _gd._tech_category_set:
        COUNTRY_LEADER_KEYS = {"country_leader"}
        UNIT_LEADER_KEYS = {"field_marshal", "corps_commander", "navy_leader"}
        IDEOLOGY_KEYS = {"ideology", "ruling_party"}
        EFFECT_CTX_KEYS = {"completion_reward", "option", "immediate", "after", "hidden_effect"}

        def _check_recursive(data, ctx=None):
            if isinstance(data, list):
                for i in data: _check_recursive(i, ctx)
            elif isinstance(data, dict):
                _line = getattr(data, "_line", None)
                for k, v in data.items():
                    new_ctx = ctx
                    if k in COUNTRY_LEADER_KEYS: new_ctx = "country_leader"
                    elif k in UNIT_LEADER_KEYS: new_ctx = "unit_leader"
                    elif k in EFFECT_CTX_KEYS: new_ctx = k
                    elif k in ("regiment", "support"): new_ctx = "regiment"
                    elif k in ("add_equipment_to_stockpile", "equipment"): new_ctx = "equipment"

                    if k in IDEOLOGY_KEYS and isinstance(v, str) and _gd._ideology_set and v not in _gd._ideology_set:
                        close = difflib.get_close_matches(v, _gd._ideology_set, n=3, cutoff=0.5)
                        warn(f"Unknown ideology: '{v}'" + (f" — did you mean: {close}?" if close else ""), line=_line)
                    elif k == "traits" and isinstance(v, list):
                        valid = (_gd._country_leader_trait_set if ctx == "country_leader"
                                 else _gd._unit_leader_trait_set if ctx == "unit_leader"
                                 else _gd._trait_set)
                        ctx_label = f" ({ctx})" if ctx else ""
                        for t in v:
                            if isinstance(t, str) and valid and t not in valid:
                                close = difflib.get_close_matches(t, valid, n=3, cutoff=0.5)
                                warn(f"Unknown trait{ctx_label}: '{t}'" + (f" — did you mean: {close}?" if close else ""), line=_line)
                    elif k == "categories" and isinstance(v, list) and _gd._tech_category_set:
                        for c in v:
                            if isinstance(c, str) and c not in _gd._tech_category_set:
                                close = difflib.get_close_matches(c, _gd._tech_category_set, n=3, cutoff=0.5)
                                warn(f"Unknown tech category: '{c}'" + (f" — did you mean: {close}?" if close else ""), line=_line)
                    elif k in ("add_building_construction", "set_building_level") and _gd._building_max:
                        btype = v.get("type") if isinstance(v, dict) else None
                        level = v.get("level") if isinstance(v, dict) else (v if isinstance(v, int) else None)
                        if btype and level and btype in _gd._building_max and level > _gd._building_max[btype]:
                            warn(f"Building '{btype}' level {level} exceeds max {_gd._building_max[btype]}", line=_line)
                    elif k in _gd._building_max and isinstance(v, int) and v > _gd._building_max[k]:
                        warn(f"Building '{k}' level {v} exceeds max {_gd._building_max[k]}", line=_line)
                    elif k == "resources" and isinstance(v, dict) and _gd._resource_set:
                        for rk in v:
                            if rk not in _gd._resource_set:
                                close = difflib.get_close_matches(rk, _gd._resource_set, n=3, cutoff=0.4)
                                warn(f"Unknown resource: '{rk}'" + (f" — did you mean: {close}?" if close else f" — valid: {sorted(_gd._resource_set)}"), line=_line)
                    elif k == "add_resource" and isinstance(v, dict) and _gd._resource_set:
                        rtype = v.get("type")
                        if rtype and rtype not in _gd._resource_set:
                            close = difflib.get_close_matches(rtype, _gd._resource_set, n=3, cutoff=0.4)
                            warn(f"Unknown resource: '{rtype}'" + (f" — did you mean: {close}?" if close else f" — valid: {sorted(_gd._resource_set)}"), line=_line)
                    elif k == "type" and isinstance(v, str) and ctx == "regiment" and _gd._sub_unit_set and v not in _gd._sub_unit_set:
                        close = difflib.get_close_matches(v, _gd._sub_unit_set, n=3, cutoff=0.5)
                        warn(f"Unknown unit type: '{v}'" + (f" — did you mean: {close}?" if close else ""), line=_line)
                    elif k == "type" and isinstance(v, str) and ctx in ("equipment", "add_equipment_to_stockpile") and _gd._equipment_type_set and v not in _gd._equipment_type_set:
                        close = difflib.get_close_matches(v, _gd._equipment_type_set, n=3, cutoff=0.5)
                        warn(f"Unknown equipment type: '{v}'" + (f" — did you mean: {close}?" if close else ""), line=_line)
                    elif k == "ai_will_do" and isinstance(v, dict) and v.get("factor") == 0:
                        warn(f"ai_will_do factor: 0 — AI will never pick this (use factor: 1 with modifiers instead)", line=_line)
                    elif k == "modifier" and isinstance(v, dict) and ctx in EFFECT_CTX_KEYS:
                        warn(f"'modifier' block in effect context ('{ctx}') does nothing — use 'add_modifier' or 'add_ideas' instead", line=_line)
                        _check_recursive(v, new_ctx)
                    elif k in ("target", "add_core_of", "remove_core_of", "owner", "controller",
                               "tag", "original_tag", "default_country", "white_peace") and \
                            isinstance(v, str) and re.match(r'^[A-Z]{2,3}$', v) and \
                            _gd._country_map is not None and _gd._country_map and \
                            v not in _gd._country_map.values():
                        close = difflib.get_close_matches(v, _gd._country_map.values(), n=3, cutoff=0.6)
                        warn(f"Unknown country TAG: '{v}'" + (f" — did you mean: {close}?" if close else ""), line=_line)
                    elif k == "add_core_of" and isinstance(v, (int, float)):
                        warn(f"'add_core_of' takes a country TAG (e.g. GER), not a number — did you mean 'add_core = {v}'?", line=_line)
                    elif k == "add_core" and isinstance(v, str) and re.match(r'^[A-Z]{2,3}$', v):
                        warn(f"'add_core' takes a state ID (number), not a TAG — did you mean 'add_core_of = {v}'?", line=_line)
                    elif k == "set_technology" and isinstance(v, dict) and "type" in v:
                        warn(f"'set_technology' does not use a 'type' key — use '{{ tech_name: 1 }}' directly, e.g. set_technology: {{ {v.get('type')}: 1 }}", line=_line)
                    elif k == "add_tech_bonus" and isinstance(v, dict) and "category" not in v:
                        warn(f"'add_tech_bonus' missing 'category' — it will not work without specifying a tech category", line=_line)
                    elif k == "set_politics" and isinstance(v, dict):
                        for req in ("ruling_party", "elections_allowed", "election_frequency"):
                            if req not in v:
                                warn(f"'set_politics' missing '{req}' — all three fields are required", line=_line)
                        _check_recursive(v, new_ctx)
                    elif k == "add_popularity" and isinstance(v, dict):
                        for req in ("ideology", "popularity"):
                            if req not in v:
                                warn(f"'add_popularity' missing '{req}' — use add_popularity: {{ ideology: X, popularity: 0.1 }}", line=_line)
                        _check_recursive(v, new_ctx)
                    elif k == "create_wargoal" and isinstance(v, dict):
                        if "type" not in v:
                            warn(f"'create_wargoal' missing 'type'", line=_line)
                        elif _gd._wargoal_type_set and v["type"] not in _gd._wargoal_type_set:
                            close = difflib.get_close_matches(v["type"], _gd._wargoal_type_set, n=3, cutoff=0.4)
                            warn(f"Unknown wargoal type: '{v['type']}'" + (f" — did you mean: {close}?" if close else f" — valid: {sorted(_gd._wargoal_type_set)}"))
                        if "target" not in v:
                            warn(f"'create_wargoal' missing 'target' (country TAG)", line=_line)
                        _check_recursive(v, new_ctx)
                    elif k == "equipment_bonus" and isinstance(v, dict):
                        for eq_key, eq_val in v.items():
                            if isinstance(eq_val, dict) and "instant" not in eq_val:
                                warn(f"'equipment_bonus.{eq_key}' missing 'instant: yes' — bonus only applies to newly produced equipment", line=_line)
                        _check_recursive(v, new_ctx)
                    elif k == "modifier" and isinstance(v, dict) and ctx not in EFFECT_CTX_KEYS and _gd._modifier_name_set:
                        for mk in v:
                            if mk not in _gd._modifier_name_set:
                                close = difflib.get_close_matches(mk, _gd._modifier_name_set, n=3, cutoff=0.5)
                                warn(f"Unknown modifier: '{mk}'" + (f" — did you mean: {close}?" if close else ""), line=_line)
                        _check_recursive(v, new_ctx)
                    elif k == "random_list" and isinstance(v, dict):
                        for weight in v:
                            try: float(str(weight))
                            except ValueError:
                                warn(f"random_list key '{weight}' is not a number (weights must be numeric)", line=_line)
                        _check_recursive(v, new_ctx)
                    elif k in ("completion_reward", "option", "immediate", "after", "hidden_effect") and isinstance(v, (dict, list)):
                        TRIGGER_ONLY = {"has_war", "is_major", "tag", "has_government", "has_idea",
                                        "has_tech", "has_stability", "has_war_support", "num_of_factories",
                                        "is_ai", "has_full_control_of_state", "has_capitulated"}
                        EFFECT_ONLY = {"add_political_power", "add_stability", "add_war_support",
                                       "add_manpower", "add_equipment_to_stockpile", "set_politics",
                                       "add_ideas", "remove_ideas", "start_war", "white_peace"}
                        def _find_triggers(d, ctx_key):
                            if isinstance(d, list):
                                for i in d: _find_triggers(i, ctx_key)
                            elif isinstance(d, dict):
                                for dk, dv in d.items():
                                    if dk in TRIGGER_ONLY:
                                        warn(f"'{dk}' is a trigger, not an effect — found in '{ctx_key}' block", line=_line)
                                    elif dk not in ("limit", "trigger"):
                                        _find_triggers(dv, ctx_key)
                        def _find_effects_in_triggers(d, ctx_key):
                            if isinstance(d, list):
                                for i in d: _find_effects_in_triggers(i, ctx_key)
                            elif isinstance(d, dict):
                                for dk, dv in d.items():
                                    if dk in EFFECT_ONLY:
                                        warn(f"'{dk}' is an effect, not a trigger — found in '{ctx_key}' block", line=_line)
                                    else:
                                        _find_effects_in_triggers(dv, ctx_key)
                        _find_triggers(v, k)
                        def _scan_for_trigger_blocks(d):
                            if isinstance(d, list):
                                for i in d: _scan_for_trigger_blocks(i)
                            elif isinstance(d, dict):
                                for sub_k in ("trigger", "limit"):
                                    if sub_k in d:
                                        _find_effects_in_triggers(d[sub_k], sub_k)
                                for dv in d.values():
                                    if isinstance(dv, (dict, list)):
                                        _scan_for_trigger_blocks(dv)
                        _scan_for_trigger_blocks(v)
                        _check_recursive(v, new_ctx)
                    elif k == "news_event" and ctx in EFFECT_CTX_KEYS:
                        warn(f"'news_event' fires for ALL countries — use 'country_event' if targeting specific countries only", line=_line)
                        _check_recursive(v, new_ctx)
                    elif k == "add_to_variable" and isinstance(data, dict) and "clamp_variable" not in data:
                        warn(f"'add_to_variable' without 'clamp_variable' — variable may go negative or overflow", line=_line)
                        _check_recursive(v, new_ctx)
                    else:
                        _check_recursive(v, new_ctx)
        _check_recursive(config)

    non_removable = set()
    for entry in config.get("ideas", []):
        if "_category" in entry:
            for idea_name, idea_def in entry.items():
                if not idea_name.startswith("_") and isinstance(idea_def, dict):
                    if idea_def.get("removal_cost") == -1:
                        non_removable.add(idea_name)
        else:
            for cat_ideas in entry.values():
                if isinstance(cat_ideas, dict):
                    for idea_name, idea_def in cat_ideas.items():
                        if isinstance(idea_def, dict) and idea_def.get("removal_cost") == -1:
                            non_removable.add(idea_name)
    if non_removable:
        def _find_remove_ideas(data):
            if isinstance(data, list):
                for i in data: _find_remove_ideas(i)
            elif isinstance(data, dict):
                if "remove_ideas" in data:
                    targets = data["remove_ideas"]
                    if isinstance(targets, str): targets = [targets]
                    for t in (targets if isinstance(targets, list) else []):
                        if t in non_removable:
                            warn(f"'remove_ideas: {t}' — this idea has removal_cost: -1 (cannot be removed)")
                for v in data.values():
                    _find_remove_ideas(v)
        _find_remove_ideas(config)

    if "character" in config:
        warn(f"Top-level key 'character' found — did you mean 'characters'?")

    for entry in config.get("technologies", []):
        for tech_name, tech_def in entry.items():
            if tech_name.startswith("_") or not isinstance(tech_def, dict):
                continue
            if "path" not in tech_def and "folder" not in tech_def and "on_research_complete" not in tech_def:
                warn(f"Technology '{tech_name}' has no 'path' or 'folder' — it will not appear in the tech tree")

    for entry in config.get("history_countries", []):
        cap = entry.get("capital") or (entry.get("history") or {}).get("capital")
        if cap and isinstance(cap, int) and cap < 1000:
            warn(f"'capital = {cap}' looks like a state ID — 'capital' takes a province ID (usually > 1000)")

    oob_files = {entry.get("_file") for entry in config.get("history_units", [])}
    def _find_load_oob(d):
        if isinstance(d, list):
            for i in d: _find_load_oob(i)
        elif isinstance(d, dict):
            if "load_oob" in d:
                ref = d["load_oob"]
                if isinstance(ref, str) and ref not in oob_files:
                    warn(f"'load_oob = {ref}' — no matching history_units entry with _file: {ref}")
            for v in d.values():
                _find_load_oob(v)
    _find_load_oob(config)

    # Localisation checks for additional sections
    def _check_loc(key, section_label):
        if key and key not in loc_keys:
            warn(f"Missing localisation: {key} ({section_label})")

    # national_focus: focus name and desc
    for entry in config.get("national_focus", []):
        for focus in (entry.get("focus_tree") or {}).get("focus", []):
            fid = focus.get("id")
            if fid:
                _check_loc(fid, "focus name")
                _check_loc(focus.get("desc", f"{fid}_desc"), "focus desc")

    # ideas: idea name
    for entry in config.get("ideas", []):
        if "_category" in entry:
            # _category style: idea defs are direct non-underscore keys
            for idea_name, idea_def in entry.items():
                if not idea_name.startswith("_") and isinstance(idea_def, dict):
                    _check_loc(idea_name, "idea name")
        else:
            for k, v in entry.items():
                if k.startswith("_"): continue
                if isinstance(v, dict):
                    for idea_name, idea_def in v.items():
                        if isinstance(idea_def, dict):
                            _check_loc(idea_name, "idea name")

    # decisions: decision name and desc
    for entry in config.get("decisions", []):
        for k, v in entry.items():
            if k.startswith("_"): continue
            if isinstance(v, list):
                for dec in v:
                    if isinstance(dec, dict):
                        did = dec.get("id")
                        if did:
                            _check_loc(did, "decision name")
                            _check_loc(dec.get("desc", f"{did}_desc"), "decision desc")

    # decisions_categories: category name and desc
    for entry in config.get("decisions_categories", []):
        for k, v in entry.items():
            if k.startswith("_"): continue
            if isinstance(v, dict):
                cid = v.get("id", k)
                _check_loc(cid, "decision_category name")

    # characters: character ID as localisation key
    for entry in config.get("characters", []):
        for k, v in entry.items():
            if not k.startswith("_") and isinstance(v, dict):
                _check_loc(k, "character")

    # dynamic_modifiers: name
    for entry in config.get("dynamic_modifiers", []):
        for k, v in entry.items():
            if not k.startswith("_") and isinstance(v, dict):
                _check_loc(k, "dynamic_modifier")

    # wargoals: name
    for entry in config.get("wargoals", []):
        for k, v in entry.items():
            if not k.startswith("_") and isinstance(v, dict):
                _check_loc(k, "wargoal")

    # opinion_modifiers: modifier name
    for entry in config.get("opinion_modifiers", []):
        for k in entry:
            if not k.startswith("_") and isinstance(entry[k], dict):
                _check_loc(k, "opinion_modifier")

    # technologies: tech name
    for entry in config.get("technologies", []):
        for k, v in entry.items():
            if not k.startswith("_") and isinstance(v, dict):
                _check_loc(k, "technology")

    # bookmarks: bookmark name
    for entry in config.get("bookmarks", []):
        for k, v in entry.items():
            if not k.startswith("_") and isinstance(v, dict):
                bid = v.get("name", k)
                _check_loc(bid, "bookmark")

    # autonomy: autonomy name
    for entry in config.get("autonomy", []):
        for k, v in entry.items():
            if not k.startswith("_") and isinstance(v, dict):
                _check_loc(k, "autonomy")

    # country_leader / unit_leader: leader ID
    for section in ("country_leader", "unit_leader"):
        for entry in config.get(section, []):
            for k, v in entry.items():
                if not k.startswith("_") and isinstance(v, dict):
                    _check_loc(k, section)

    # game_rules: rule name
    for entry in config.get("game_rules", []):
        for k, v in entry.items():
            if not k.startswith("_") and isinstance(v, dict):
                _check_loc(k, "game_rule")

    # state_category: category name
    for entry in config.get("state_category", []):
        for k, v in entry.items():
            if not k.startswith("_") and isinstance(v, dict):
                _check_loc(k, "state_category")
