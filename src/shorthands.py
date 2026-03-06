from .gamedata import resolve_state
from .icons import guess_icon, auto_layout_focuses


def expand_events(entries):
    result = []
    for entry in entries:
        entry = dict(entry)
        for etype in ("country_event", "news_event", "state_event"):
            if etype not in entry:
                continue
            expanded = []
            for ev in entry[etype]:
                ev = dict(ev)
                eid = ev.get("id", "")
                ev.setdefault("title", f"{eid}.t")
                ev.setdefault("desc",  f"{eid}.d")
                if "option" in ev:
                    ev["option"] = [
                        dict(opt, name=opt.get("name", f"{eid}.{chr(ord('a') + i)}"))
                        for i, opt in enumerate(ev["option"])
                    ]
                expanded.append(ev)
            entry[etype] = expanded
        result.append(entry)
    return result


def expand_shorthands(data):
    if isinstance(data, list):
        return [expand_shorthands(i) for i in data]
    if not isinstance(data, dict):
        return data

    out = {}
    if "id" in data and "icon" not in data and ("x" in data or "y" in data or "rel_pos" in data):
        out["icon"] = guess_icon(str(data["id"]))
    for k, v in data.items():
        if k == "focus" and isinstance(v, list) and v and isinstance(v[0], dict) and "id" in v[0]:
            v = auto_layout_focuses([dict(f) for f in v])
        if k == "prereq":
            if isinstance(v, list):
                out["prerequisite"] = {"focus": v[0]} if len(v) == 1 else {"focus": v}
            else:
                out["prerequisite"] = {"focus": v}
        elif k == "prereq_or":
            items = v if isinstance(v, list) else [v]
            out["prerequisite"] = [{"focus": f} for f in items]
        elif k == "ai_will_do":
            if isinstance(v, (int, float)):
                out["ai_will_do"] = {"factor": v}
            elif isinstance(v, dict) and "factor" in v:
                modifiers = []
                base = {"factor": v["factor"]}
                for mk, mv in v.items():
                    if mk == "factor":
                        continue
                    if mk == "if" and isinstance(mv, list):
                        for item in mv:
                            mod = {"factor": item.pop("mult", 1)}; mod.update(item); modifiers.append(mod)
                    elif mk == "if" and isinstance(mv, dict):
                        mod = {"factor": mv.pop("mult", 1)}; mod.update(mv); modifiers.append(mod)
                result = dict(base)
                if modifiers:
                    result["modifier"] = modifiers
                out["ai_will_do"] = expand_shorthands(result)
            else:
                out["ai_will_do"] = expand_shorthands(v)
        elif k == "reward":
            out["completion_reward"] = expand_shorthands(v)
        elif k == "rel_pos":
            out["relative_position_id"] = v
        elif k == "hidden":
            out["hidden_effect"] = expand_shorthands(v)
        elif k == "timed_idea" and isinstance(v, dict):
            idea = v["idea"]; days = v.get("days", 30)
            out["add_ideas"] = idea
            out["if"] = {"limit": {"NOT": {"has_idea": idea}}, "add_ideas": idea}
            out["_timed_idea_note"] = f"Set days_remove = {days} on idea '{idea}' definition"
        elif k == "regiments" and isinstance(v, list):
            out["regiment"] = [{"type": list(r.keys())[0], "column": i % 5, "row": i // 5}
                               for i, r in enumerate(v) for _ in range(list(r.values())[0])]
        elif k == "support_companies" and isinstance(v, list):
            out["support"] = [{"type": list(s.keys())[0], "column": i, "row": 0}
                              for i, s in enumerate(v)]
        elif k == "add_state_building" and isinstance(v, dict):
            sid = resolve_state(v["state"]) if "state" in v else v.get("state_id")
            payload = expand_shorthands({"add_building_construction": {
                "type": v["type"], "level": v.get("level", 1),
                "instant_build": "yes" if v.get("instant", True) else "no"
            }})
            out[sid] = {**out[sid], **payload} if sid in out and isinstance(out.get(sid), dict) else payload
        elif k == "add_state_manpower" and isinstance(v, dict):
            sid = resolve_state(v["state"]) if "state" in v else v.get("state_id")
            payload = {"add_manpower": v["value"]}
            out[sid] = {**out[sid], **payload} if sid in out and isinstance(out.get(sid), dict) else payload
        elif k == "sprites":
            out["spriteTypes"] = {"spriteType": expand_shorthands(v)}
        elif k == "set_tech":
            techs = v if isinstance(v, list) else [v]
            out["set_technology"] = {t: 1 for t in techs}
        elif k == "set_ruling_party":
            out["set_politics"] = {"ruling_party": v, "elections_allowed": "no", "election_frequency": 48}
        elif k == "add_pop" and isinstance(v, dict):
            for ideology, pop in v.items():
                out.setdefault("add_popularity", [])
                if not isinstance(out["add_popularity"], list):
                    out["add_popularity"] = [out["add_popularity"]]
                out["add_popularity"].append({"ideology": ideology, "popularity": pop})
        elif k == "color" and "color_ui" not in data:
            out["color"] = v; out["color_ui"] = v
        else:
            out[k] = expand_shorthands(v)
    return out
