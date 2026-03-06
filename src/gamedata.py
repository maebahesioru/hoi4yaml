import re
import json
import difflib
from pathlib import Path
from .utils import warn

CACHE_FILE = Path(__file__).parent.parent / ".hoi4cache.json"

_hoi4_path = None
_state_map = None
_province_map = None
_country_map = None
_ideology_set = None
_trait_set = None
_country_leader_trait_set = None
_unit_leader_trait_set = None
_tech_category_set = None
_building_max = None
_resource_set = None
_sub_unit_set = None
_equipment_type_set = None
_wargoal_type_set = None
_modifier_name_set = None
_extra_state_map = {}


def find_hoi4_path():
    global _hoi4_path
    if _hoi4_path is not None:
        return _hoi4_path
    candidates = [
        "C:/Program Files (x86)/Steam/steamapps/common/Hearts of Iron IV",
        "C:/Program Files/Steam/steamapps/common/Hearts of Iron IV",
        *(f"{d}:/Steam/steamapps/common/Hearts of Iron IV" for d in "DEFGH"),
        *(f"{d}:/SteamLibrary/steamapps/common/Hearts of Iron IV" for d in "DEFGH"),
        *(f"{d}:/steamapps/common/Hearts of Iron IV" for d in "DEFGH"),
        "/mnt/c/Program Files (x86)/Steam/steamapps/common/Hearts of Iron IV",
        "/mnt/c/Program Files/Steam/steamapps/common/Hearts of Iron IV",
        *(f"/mnt/{d.lower()}/Steam/steamapps/common/Hearts of Iron IV" for d in "DEFGH"),
        *(f"/mnt/{d.lower()}/SteamLibrary/steamapps/common/Hearts of Iron IV" for d in "DEFGH"),
        "~/Library/Application Support/Steam/steamapps/common/Hearts of Iron IV",
        "~/.steam/steam/steamapps/common/Hearts of Iron IV",
        "~/.local/share/Steam/steamapps/common/Hearts of Iron IV",
    ]
    for c in candidates:
        p = Path(c).expanduser()
        if p.exists():
            _hoi4_path = p; return _hoi4_path
    return None


def _load_cache():
    if not CACHE_FILE.exists():
        return None
    try:
        data = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        hoi4 = find_hoi4_path()
        if hoi4:
            check_paths = [hoi4 / "common/national_focus", hoi4 / "common/units/equipment",
                           hoi4 / "common/units", hoi4 / "common/resources"]
            mtime = max((p.stat().st_mtime for p in check_paths if p.exists()), default=0)
            if data.get("mtime") != mtime:
                return None
        return data
    except Exception:
        return None


def _save_cache(data):
    try:
        hoi4 = find_hoi4_path()
        if hoi4:
            check_paths = [hoi4 / "common/national_focus", hoi4 / "common/units/equipment",
                           hoi4 / "common/units", hoi4 / "common/resources"]
            data["mtime"] = max((p.stat().st_mtime for p in check_paths if p.exists()), default=0)
        CACHE_FILE.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass


def load_game_maps(hoi4_path):
    state_key_to_id = {}
    state_key_to_province = {}
    for f in (hoi4_path / "history/states").glob("*.txt"):
        text = f.read_text(encoding="utf-8-sig", errors="ignore")
        id_m  = re.search(r'\bid\s*=\s*(\d+)', text)
        key_m = re.search(r'\bname\s*=\s*"(STATE_\d+)"', text)
        if id_m and key_m:
            state_key_to_id[key_m.group(1)] = int(id_m.group(1))
            vp_m = re.search(r'victory_points\s*=\s*\{\s*(\d+)', text)
            prov_m = re.search(r'provinces\s*=\s*\{[^}]*?(\d+)', text, re.DOTALL)
            prov = int(vp_m.group(1)) if vp_m else (int(prov_m.group(1)) if prov_m else None)
            if prov:
                state_key_to_province[key_m.group(1)] = prov

    state_name_to_id = {}
    state_name_to_province = {}
    loc_file = hoi4_path / "localisation/english/state_names_l_english.yml"
    if loc_file.exists():
        for m in re.finditer(r'(STATE_\d+):0\s+"([^"]+)"', loc_file.read_text(encoding="utf-8-sig", errors="ignore")):
            key, name = m.group(1), m.group(2)
            nl = name.lower()
            if key in state_key_to_id:
                state_name_to_id[nl] = state_key_to_id[key]
            if key in state_key_to_province:
                state_name_to_province[nl] = state_key_to_province[key]

    country_name_to_tag = {}
    tag_order = []
    for f in sorted((hoi4_path / "common/country_tags").glob("*.txt")):
        for tag in re.findall(r'^([A-Z]{3})\s*=', f.read_text(encoding="utf-8-sig", errors="ignore"), re.MULTILINE):
            tag_order.append(tag)
    loc_dir = hoi4_path / "localisation/english"
    combined = "\n".join(f.read_text(encoding="utf-8-sig", errors="ignore")
                         for f in loc_dir.glob("*.yml") if f.exists())
    for tag in tag_order:
        m = re.search(rf'^\s*{tag}:0\s+"([^"]+)"', combined, re.MULTILINE)
        if m:
            name = m.group(1).lower()
            if name not in country_name_to_tag:
                country_name_to_tag[name] = tag

    ideologies = set()
    for f in (hoi4_path / "common/ideologies").glob("*.txt"):
        text = f.read_text(encoding="utf-8-sig", errors="ignore")
        for m in re.finditer(r'^\s*(\w+)\s*=\s*\{', text, re.MULTILINE):
            ideologies.add(m.group(1))
        for block in re.findall(r'types\s*=\s*\{([^}]+)\}', text, re.DOTALL):
            for m in re.finditer(r'(\w+)\s*=\s*\{', block):
                ideologies.add(m.group(1))
    ideologies -= {"types", "dynamic_faction_names", "color", "war_impact_on_world_tension",
                   "faction_impact_on_world_tension", "rules", "can_be_randomly_selected"}

    country_leader_traits = set()
    unit_leader_traits = set()
    for f in (hoi4_path / "common/country_leader").glob("*.txt"):
        text = f.read_text(encoding="utf-8-sig", errors="ignore")
        for block in re.findall(r'leader_traits\s*=\s*\{(.+?)^\}', text, re.DOTALL | re.MULTILINE):
            for m in re.finditer(r'^\t(\w+)\s*=\s*\{', block, re.MULTILINE):
                country_leader_traits.add(m.group(1))
    for f in (hoi4_path / "common/unit_leader").glob("*.txt"):
        text = f.read_text(encoding="utf-8-sig", errors="ignore")
        for block in re.findall(r'leader_traits\s*=\s*\{(.+?)^\}', text, re.DOTALL | re.MULTILINE):
            for m in re.finditer(r'^\t(\w+)\s*=\s*\{', block, re.MULTILINE):
                unit_leader_traits.add(m.group(1))
    traits = country_leader_traits | unit_leader_traits

    tech_categories = set()
    tag_file = hoi4_path / "common/technology_tags/00_technology.txt"
    if tag_file.exists():
        for m in re.finditer(r'^\s+(\w+)\s*$', tag_file.read_text(encoding="utf-8-sig", errors="ignore"), re.MULTILINE):
            tech_categories.add(m.group(1))

    building_max = {}
    for f in (hoi4_path / "common/buildings").glob("*.txt"):
        text = f.read_text(encoding="utf-8-sig", errors="ignore")
        for m in re.finditer(r'^\t(\w+)\s*=\s*\{', text, re.MULTILINE):
            name = m.group(1)
            snippet = text[m.start():m.start()+600]
            cap = re.search(r'level_cap\s*=\s*\{([^}]+)\}', snippet, re.DOTALL)
            if cap:
                sm = re.search(r'state_max\s*=\s*(\d+)', cap.group(1))
                if sm:
                    building_max[name] = int(sm.group(1))

    resources = set()
    for f in (hoi4_path / "common/resources").glob("*.txt"):
        for m in re.finditer(r'^\t(\w+)\s*=\s*\{', f.read_text(encoding="utf-8-sig", errors="ignore"), re.MULTILINE):
            resources.add(m.group(1))

    sub_units = set()
    for f in (hoi4_path / "common/units").glob("*.txt"):
        text = f.read_text(encoding="utf-8-sig", errors="ignore")
        for block in re.findall(r'sub_units\s*=\s*\{(.+?)^\}', text, re.DOTALL | re.MULTILINE):
            for m in re.finditer(r'^\t(\w+)\s*=\s*\{', block, re.MULTILINE):
                sub_units.add(m.group(1))

    equipment_types = set()
    for f in (hoi4_path / "common/units/equipment").glob("*.txt"):
        text = f.read_text(encoding="utf-8-sig", errors="ignore")
        for block in re.findall(r'^equipments\s*=\s*\{(.+?)^\}', text, re.DOTALL | re.MULTILINE):
            for m in re.finditer(r'^\t(\w+)\s*=\s*\{', block, re.MULTILINE):
                equipment_types.add(m.group(1))

    wargoal_types = set()
    for f in (hoi4_path / "common/wargoals").glob("*.txt"):
        text = f.read_text(encoding="utf-8-sig", errors="ignore")
        for block in re.findall(r'wargoal_types\s*=\s*\{(.+?)^\}', text, re.DOTALL | re.MULTILINE):
            for m in re.finditer(r'^\t(\w+)\s*=\s*\{', block, re.MULTILINE):
                wargoal_types.add(m.group(1))

    modifier_names = set()
    for f in (hoi4_path / "common/ideas").glob("*.txt"):
        for block in re.findall(r'modifier\s*=\s*\{([^}]+)\}', f.read_text(encoding="utf-8-sig", errors="ignore")):
            for m in re.finditer(r'\t\t\t(\w+)\s*=', block):
                modifier_names.add(m.group(1))
    for f in (hoi4_path / "common/modifier_definitions").glob("*.txt"):
        for m in re.finditer(r'^\t(\w+)\s*=\s*\{', f.read_text(encoding="utf-8-sig", errors="ignore"), re.MULTILINE):
            modifier_names.add(m.group(1))

    return (state_name_to_id, state_name_to_province, country_name_to_tag, ideologies, traits,
            tech_categories, building_max, country_leader_traits, unit_leader_traits,
            resources, sub_units, equipment_types, wargoal_types, modifier_names)


def get_game_maps():
    global _state_map, _province_map, _country_map, _ideology_set, _trait_set
    global _country_leader_trait_set, _unit_leader_trait_set, _tech_category_set, _building_max
    global _resource_set, _sub_unit_set, _equipment_type_set, _wargoal_type_set, _modifier_name_set
    if _state_map is None:
        cache = _load_cache()
        if cache and "state_map" in cache:
            _state_map = {k: int(v) for k, v in cache["state_map"].items()}
            _province_map = {k: int(v) for k, v in cache.get("province_map", {}).items()}
            _country_map = cache["country_map"]
            _ideology_set = set(cache.get("ideologies", []))
            _trait_set = set(cache.get("traits", []))
            _country_leader_trait_set = set(cache.get("country_leader_traits", []))
            _unit_leader_trait_set = set(cache.get("unit_leader_traits", []))
            _tech_category_set = set(cache.get("tech_categories", []))
            _building_max = cache.get("building_max", {})
            _resource_set = set(cache.get("resources", []))
            _sub_unit_set = set(cache.get("sub_units", []))
            _equipment_type_set = set(cache.get("equipment_types", []))
            _wargoal_type_set = set(cache.get("wargoal_types", []))
            _modifier_name_set = set(cache.get("modifier_names", []))
        else:
            hoi4 = find_hoi4_path()
            if hoi4:
                (_state_map, _province_map, _country_map, _ideology_set, _trait_set,
                 _tech_category_set, _building_max, _country_leader_trait_set, _unit_leader_trait_set,
                 _resource_set, _sub_unit_set, _equipment_type_set,
                 _wargoal_type_set, _modifier_name_set) = load_game_maps(hoi4)
                c = _load_cache() or {}
                c.update({"state_map": _state_map, "province_map": _province_map,
                          "country_map": _country_map, "ideologies": list(_ideology_set),
                          "traits": list(_trait_set),
                          "country_leader_traits": list(_country_leader_trait_set),
                          "unit_leader_traits": list(_unit_leader_trait_set),
                          "tech_categories": list(_tech_category_set),
                          "building_max": _building_max,
                          "resources": list(_resource_set),
                          "sub_units": list(_sub_unit_set),
                          "equipment_types": list(_equipment_type_set),
                          "wargoal_types": list(_wargoal_type_set),
                          "modifier_names": list(_modifier_name_set)})
                _save_cache(c)
            else:
                _state_map = _province_map = _country_map = {}
                _ideology_set = _trait_set = _tech_category_set = set()
                _country_leader_trait_set = _unit_leader_trait_set = set()
                _resource_set = _sub_unit_set = _equipment_type_set = set()
                _wargoal_type_set = _modifier_name_set = set()
                _building_max = {}
    return {**_state_map, **_extra_state_map}, _province_map, _country_map


def resolve_state(value):
    if isinstance(value, int):
        return value
    state_map, _, _ = get_game_maps()
    key = str(value).lower()
    if key in state_map:
        return state_map[key]
    close = difflib.get_close_matches(key, state_map.keys(), n=3, cutoff=0.5)
    hint = f" — did you mean: {[f'{n}={state_map[n]}' for n in close]}?" if close else ""
    raise ValueError(f"Unknown state: '{value}'{hint}")


def resolve_location(value):
    if isinstance(value, int):
        return value
    _, province_map, _ = get_game_maps()
    key = str(value).lower()
    if key in province_map:
        return province_map[key]
    return resolve_state(value)


def resolve_tag(value):
    if isinstance(value, str) and re.match(r'^[A-Z]{3}$', value):
        return value
    _, _, country_map = get_game_maps()
    key = str(value).lower()
    if key in country_map:
        return country_map[key]
    close = difflib.get_close_matches(key, country_map.keys(), n=3, cutoff=0.5)
    hint = f" — did you mean: {[f'{n}={country_map[n]}' for n in close]}?" if close else ""
    raise ValueError(f"Unknown country: '{value}'{hint}")


def resolve_game_refs(data):
    if isinstance(data, list):
        return [resolve_game_refs(i) for i in data]
    if not isinstance(data, dict):
        return data
    out = {}
    for k, v in data.items():
        if k == "location" and isinstance(v, str) and not v.isdigit():
            try: out[k] = resolve_location(v)
            except ValueError as e: warn(str(e)); out[k] = v
        elif k == "capital" and isinstance(v, str) and not v.isdigit():
            try: out[k] = resolve_state(v)
            except ValueError as e: warn(str(e)); out[k] = v
        elif k in ("owner", "controller", "tag", "add_core_of", "remove_core_of",
                   "original_tag", "default_country", "target") and isinstance(v, str) and not re.match(r'^[A-Z]{3}$', v):
            try: out[k] = resolve_tag(v)
            except ValueError as e: warn(str(e)); out[k] = v
        else:
            out[k] = resolve_game_refs(v)
    return out
