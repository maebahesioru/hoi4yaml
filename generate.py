#!/usr/bin/env python3
"""HoI4 Mod Generator - YAML → HoI4 mod files (and back)"""

import sys
import time
import shutil
import zipfile
import yaml
from pathlib import Path

from src.utils import G, Y, R, B, X, _load_yaml_with_lines, apply_vars, apply_templates, apply_conditions
from src.utils import write
import src.utils as _utils
from src.clausewitz import parse_clausewitz
from src.gamedata import get_game_maps, find_hoi4_path, _extra_state_map
from src.gamedata import resolve_state as _resolve_state
import src.gamedata as _gd
from src.icons import _mod_localisation
from src.validation import validate, extract_mod_states, load_extra_mod_paths
from src.generators import gen_section, gen_localisation

SECTIONS = {
    "national_focus":        ("common/national_focus",              "txt"),
    "continuous_focus":      ("common/continuous_focus",            "txt"),
    "events":                ("events",                             "txt"),
    "ideas":                 ("common/ideas",                       "txt"),
    "decisions":             ("common/decisions",                   "txt"),
    "decisions_categories":  ("common/decisions/categories",        "txt"),
    "technologies":          ("common/technologies",                "txt"),
    "technology_sharing":    ("common/technology_sharing",          "txt"),
    "doctrines":             ("common/doctrines",                   "txt"),
    "doctrines_folders":     ("common/doctrines/folders",           "txt"),
    "doctrines_grand":       ("common/doctrines/grand_doctrines",   "txt"),
    "doctrines_tracks":      ("common/doctrines/tracks",            "txt"),
    "doctrines_sub_air":     ("common/doctrines/subdoctrines/air",  "txt"),
    "doctrines_sub_land":    ("common/doctrines/subdoctrines/land", "txt"),
    "doctrines_sub_sea":     ("common/doctrines/subdoctrines/sea",  "txt"),
    "on_actions":            ("common/on_actions",                  "txt"),
    "characters":            ("common/characters",                  "txt"),
    "portraits":             ("common/portraits",                   "txt"),
    "country_leader":        ("common/country_leader",              "txt"),
    "unit_leader":           ("common/unit_leader",                 "txt"),
    "abilities":             ("common/abilities",                   "txt"),
    "aces":                  ("common/aces",                        "txt"),
    "scripted_triggers":     ("common/scripted_triggers",           "txt"),
    "scripted_effects":      ("common/scripted_effects",            "txt"),
    "scripted_localisation": ("common/scripted_localisation",       "txt"),
    "scripted_gui":          ("common/scripted_guis",               "txt"),
    "scripted_variables":    ("common/scripted_variables",          "txt"),
    "opinion_modifiers":     ("common/opinion_modifiers",           "txt"),
    "dynamic_modifiers":     ("common/dynamic_modifiers",           "txt"),
    "triggered_modifiers":   ("common/triggered_modifiers",         "txt"),
    "modifiers":             ("common/modifiers",                   "txt"),
    "wargoals":              ("common/wargoals",                    "txt"),
    "bookmarks":             ("common/bookmarks",                   "txt"),
    "country_tags":          ("common/country_tags",                "txt"),
    "country_tag_aliases":   ("common/country_tag_aliases",         "txt"),
    "country_colors":        ("common/countries",                   "txt"),
    "cosmetic_tags":         ("common/cosmetic_tags",               "txt"),
    "autonomy":              ("common/autonomy",                    "txt"),
    "autonomous_states":     ("common/autonomous_states",           "txt"),
    "factions":              ("common/factions",                    "txt"),
    "factions_goals":        ("common/factions/goals",              "txt"),
    "factions_icons":        ("common/factions/icons",              "txt"),
    "factions_member_upgrades": ("common/factions/member_upgrades", "txt"),
    "factions_member_groups": ("common/factions/member_upgrades/member_groups", "txt"),
    "factions_rules":        ("common/factions/rules",              "txt"),
    "factions_rules_groups": ("common/factions/rules/groups",       "txt"),
    "factions_templates":    ("common/factions/templates",          "txt"),
    "factions_upgrades":     ("common/factions/upgrades",           "txt"),
    "factions_upgrades_groups": ("common/factions/upgrades/groups", "txt"),
    "occupation_laws":       ("common/occupation_laws",             "txt"),
    "game_rules":            ("common/game_rules",                  "txt"),
    "difficulty_settings":   ("common/difficulty_settings",         "txt"),
    "focus_inlay_windows":   ("common/focus_inlay_windows",         "txt"),
    "frontend":              ("common/frontend",                    "txt"),
    "frontend_backgrounds":  ("common/frontend/backgrounds",        "txt"),
    "peace_conference":      ("common/peace_conference",            "txt"),
    "peace_conference_ai":   ("common/peace_conference/ai_peace",   "txt"),
    "peace_conference_categories": ("common/peace_conference/categories", "txt"),
    "peace_conference_cost_modifiers": ("common/peace_conference/cost_modifiers", "txt"),
    "intelligence_agencies": ("common/intelligence_agencies",       "txt"),
    "intelligence_agency_upgrades": ("common/intelligence_agency_upgrades", "txt"),
    "operations":            ("common/operations",                  "txt"),
    "raids":                 ("common/raids",                       "txt"),
    "raids_categories":      ("common/raids/categories",            "txt"),
    "profile_backgrounds":   ("common/profile_backgrounds",         "txt"),
    "profile_pictures":      ("common/profile_pictures",            "txt"),
    "scorers_country":       ("common/scorers/country",             "txt"),
    "resistance_activity":   ("common/resistance_activity",         "txt"),
    "resistance_compliance_modifiers": ("common/resistance_compliance_modifiers", "txt"),
    "military_industrial_organization": ("common/military_industrial_organization", "txt"),
    "mio_ai_bonus_weights":  ("common/military_industrial_organization/ai_bonus_weights", "txt"),
    "mio_organizations":     ("common/military_industrial_organization/organizations", "txt"),
    "mio_policies":          ("common/military_industrial_organization/policies", "txt"),
    "scientist_traits":      ("common/scientist_traits",            "txt"),
    "names":                 ("common/names",                       "txt"),
    "unit_tags":             ("common/unit_tags",                   "txt"),
    "ribbons":               ("common/ribbons",                     "txt"),
    "unit_medals":           ("common/unit_medals",                 "txt"),
    "collections":           ("common/collections",                 "txt"),
    "bop":                   ("common/bop",                         "txt"),
    "ideologies":            ("common/ideologies",                  "txt"),
    "idea_tags":             ("common/idea_tags",                   "txt"),
    "modifier_definitions":  ("common/modifier_definitions",        "txt"),
    "script_constants":      ("common/script_constants",            "txt"),
    "scorers":               ("common/scorers",                     "txt"),
    "strategic_locations":   ("common/strategic_locations",         "txt"),
    "technology_tags":       ("common/technology_tags",             "txt"),
    "mtth":                  ("common/mtth",                        "txt"),
    "acclimatation":         ("common",                             "txt"),
    "ai_attitudes":          ("common",                             "txt"),
    "ai_personalities":      ("common",                             "txt"),
    "alerts":                ("common",                             "txt"),
    "combat_tactics":        ("common",                             "txt"),
    "event_modifiers":       ("common",                             "txt"),
    "graphicalculturetype":  ("common",                             "txt"),
    "region_colors":         ("common",                             "txt"),
    "script_enums":          ("common",                             "txt"),
    "triggered_modifiers":   ("common/triggered_modifiers",         "txt"),
    "weather":               ("common",                             "txt"),
    "equipment_groups":      ("common/equipment_groups",            "txt"),
    "generation":            ("common/generation",                  "txt"),
    "ai_areas":              ("common/ai_areas",                    "txt"),
    "ai_equipment":          ("common/ai_equipment",                "txt"),
    "ai_faction_theaters":   ("common/ai_faction_theaters",         "txt"),
    "ai_navy":               ("common/ai_navy",                     "txt"),
    "ai_navy_fleet":         ("common/ai_navy/fleet",               "txt"),
    "ai_navy_goals":         ("common/ai_navy/goals",               "txt"),
    "ai_navy_taskforce":     ("common/ai_navy/taskforce",           "txt"),
    "operation_phases":      ("common/operation_phases",            "txt"),
    "operation_tokens":      ("common/operation_tokens",            "txt"),
    "ai_strategy":           ("common/ai_strategy",                 "txt"),
    "ai_focuses":            ("common/ai_focuses",                  "txt"),
    "ai_peace":              ("common/ai_peace",                    "txt"),
    "ai_templates":          ("common/ai_templates",                "txt"),
    "ai_equipment_designs":  ("common/ai_equipment_designs",        "txt"),
    "ai_strategy_plans":     ("common/ai_strategy_plans",           "txt"),
    "equipment":             ("common/units/equipment",             "txt"),
    "equipment_modules":     ("common/units/equipment/modules",     "txt"),
    "equipment_upgrades":    ("common/units/equipment/upgrades",    "txt"),
    "units":                 ("common/units",                       "txt"),
    "units_codenames":       ("common/units/codenames_operatives",  "txt"),
    "units_critical_parts":  ("common/units/critical_parts",        "txt"),
    "units_names":           ("common/units/names",                 "txt"),
    "units_names_divisions": ("common/units/names_divisions",       "txt"),
    "units_names_railway_guns": ("common/units/names_railway_guns", "txt"),
    "units_names_ships":     ("common/units/names_ships",           "txt"),
    "units_modifiers":       ("common/units/unit_modifiers",        "txt"),
    "buildings":             ("common/buildings",                   "txt"),
    "resources":             ("common/resources",                   "txt"),
    "terrain":               ("common/terrain",                     "txt"),
    "state_category":        ("common/state_category",              "txt"),
    "named_colors":          ("common/named_colors",                "txt"),
    "medals":                ("common/medals",                      "txt"),
    "map_modes":             ("common/map_modes",                   "txt"),
    "strategic_regions":     ("map/strategicregions",               "txt"),
    "supply_areas":          ("map/supplyareas",                    "txt"),
    "map_adjacency_rules":   ("map",                                "txt"),
    "map_continent":         ("map",                                "txt"),
    "map_railways":          ("map",                                "txt"),
    "map_ambient_object":    ("map",                                "txt"),
    "map_buildings":         ("map",                                "txt"),
    "map_cities":            ("map",                                "txt"),
    "map_colors":            ("map",                                "txt"),
    "map_positions":         ("map",                                "txt"),
    "map_seasons":           ("map",                                "txt"),
    "map_supply_nodes":      ("map",                                "txt"),
    "map_terrain":           ("map/terrain",                        "txt"),
    "map_unitstacks":        ("map",                                "txt"),
    "map_weatherpositions":  ("map",                                "txt"),
    "special_projects":      ("common/special_projects",            "txt"),
    "special_projects_tags": ("common/special_projects/project_tags", "txt"),
    "special_projects_projects": ("common/special_projects/projects", "txt"),
    "special_projects_rewards": ("common/special_projects/prototype_rewards", "txt"),
    "special_projects_specialization": ("common/special_projects/specialization", "txt"),
    "timed_activities":      ("common/timed_activities",            "txt"),
    "scripted_diplomatic_actions": ("common/scripted_diplomatic_actions", "txt"),
    "defines":               ("common/defines",                     "lua"),
    "history_countries":     ("history/countries",                  "txt"),
    "history_general":       ("history/general",                    "txt"),
    "history_states":        ("history/states",                     "txt"),
    "history_units":         ("history/units",                      "txt"),
    "history_provinces":     ("history/provinces",                  "txt"),
    "script":                ("script",                             "lua"),
    "country_metadata":      ("country_metadata",                   "txt"),
    "dlc_metadata":          ("dlc_metadata/dlc_info",              "txt"),
    "tutorial":              ("tutorial",                           "txt"),
    "interface":             ("interface",                          "gfx"),
    "interface_gui":         ("interface",                          "gui"),
    "gfx_army_icons":        ("gfx/army_icons",                    "txt"),
    "gfx_maparrows":         ("gfx/maparrows",                     "txt"),
    "gfx_naval_combat":      ("gfx",                               "txt"),
    "gfx_posteffect":        ("gfx",                               "txt"),
    "gfx_3dviewenv":         ("gfx/3dviewenv",                     "txt"),
    "gfx_train_db":          ("gfx/train_gfx_database",            "txt"),
    "gfx_equipment_icons":   ("gfx/interface/equipmentdesigner/graphic_db", "txt"),
    "gfx_entities":          ("gfx/entities",                      "asset"),
    "gfx_particles":         ("gfx/particles",                     "asset"),
    "gfx_models":            ("gfx/models",                        "asset"),
    "music":                 ("music",                              "asset"),
    "music_hoi2":            ("music/hoi2",                        "asset"),
    "music_hoi3":            ("music/hoi3",                        "asset"),
    "sound":                 ("sound",                             "asset"),
    "sound_gui":             ("sound/gui",                         "asset"),
    "sound_animations":      ("sound/animations",                  "asset"),
    "sound_menu":            ("sound/menu",                        "asset"),
    "sound_weather":         ("sound/weather",                     "asset"),
}


def load_configs(yaml_files):
    merged = {}
    for f in yaml_files:
        config = _load_yaml_with_lines(Path(f).read_text(encoding="utf-8"))
        for key, value in config.items():
            if key in merged and isinstance(value, list):
                merged[key].extend(value)
            elif key in merged and isinstance(value, dict):
                merged[key].update(value)
            else:
                merged[key] = value
    return merged


def preprocess(config):
    variables = config.get("vars", {})
    templates = config.get("templates", {})
    if variables:
        config = apply_vars(config, variables)
    if templates:
        config = apply_templates(config, templates)
    return apply_conditions(config)


def generate(yaml_files, clean=False, dry_run=False, output_dir=Path("output"), do_zip=False, diff_only=False):
    _utils._file_count = 0
    _utils._warn_count = 0

    config = preprocess(load_configs(yaml_files))
    info = config.get("mod", {})
    mod_name = info.get("name", "my_mod").lower().replace(" ", "_")
    mod_dir = output_dir / mod_name

    if clean and mod_dir.exists() and not dry_run:
        shutil.rmtree(mod_dir)
        print(f"{Y}Cleaned:{X} {mod_dir}/")

    _gd._extra_state_map.update(extract_mod_states(config))
    _, extra_states, _, _, _ = load_extra_mod_paths(info.get("mod_paths", []))
    _gd._extra_state_map.update(extra_states)

    print(f"{B}Generating:{X} {info.get('name', mod_name)}")
    validate(config)

    loc = config.get("localisation", {})
    if loc and isinstance(next(iter(loc.values())), dict):
        _mod_localisation.update(loc.get("english", {}))
    else:
        _mod_localisation.update(loc)

    for section, (subdir, ext) in SECTIONS.items():
        if section in config:
            gen_section(mod_dir, config[section], subdir, ext=ext, dry_run=dry_run, diff_only=diff_only)

    if "localisation" in config:
        gen_localisation(mod_dir, config["localisation"], dry_run=dry_run, diff_only=diff_only)

    if do_zip and not dry_run:
        zip_path = output_dir / f"{mod_name}.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in mod_dir.rglob("*"):
                zf.write(f, f.relative_to(output_dir))
        print(f"{G}Zipped:{X} {zip_path}")

    warns = f"  {Y}{_utils._warn_count} warnings{X}" if _utils._warn_count else ""
    print(f"\nDone → {mod_dir}/  ({G}{_utils._file_count} files{X}{warns})\n")


def do_import(path_str):
    path = Path(path_str)
    files = [path] if path.is_file() else list(path.rglob("*.txt")) + list(path.rglob("*.gfx")) + list(path.rglob("*.asset"))
    result = {}
    for f in files:
        try:
            parsed = parse_clausewitz(f.read_text(encoding="utf-8-sig", errors="ignore"))
            if parsed:
                result[f.stem] = parsed
                print(f"  {G}imported:{X} {f}")
        except Exception as e:
            print(f"  {R}skip:{X} {f} ({e})")
    out = Path("imported.yaml")
    out.write_text(yaml.dump(result, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"\n{G}Saved:{X} {out}")


def do_init():
    print(f"{B}hoi4yaml init{X} - New mod setup\n")
    name    = input("Mod name: ").strip() or "My Mod"
    version = input("Version [1.0.0]: ").strip() or "1.0.0"
    hoi4ver = input("Supported HoI4 version [*]: ").strip() or "*"
    tags    = input("Tags (comma separated) [Historical]: ").strip() or "Historical"
    scaffold = {
        "mod": {"name": name, "version": version, "supported_version": hoi4ver,
                "tags": [t.strip() for t in tags.split(",")]},
        "vars": {"MOD_TAG": name.upper().replace(" ", "_")[:3]},
        "localisation": {"english": {}, "japanese": {}},
    }
    out = Path("mod.yaml")
    if out.exists():
        if input(f"{Y}mod.yaml already exists. Overwrite? [y/N]:{X} ").strip().lower() != "y":
            print("Aborted."); return
    out.write_text(yaml.dump(scaffold, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"\n{G}Created:{X} mod.yaml")


def do_list():
    print(f"{B}Supported sections:{X}\n")
    for section, (subdir, ext) in SECTIONS.items():
        print(f"  {G}{section:<25}{X} → {subdir}/*.{ext}")
    print(f"\n  {G}{'localisation':<25}{X} → localisation/mod_l_<lang>.yml")
    print(f"  {G}{'templates':<25}{X} → (used for _template inheritance)")
    print(f"  {G}{'vars':<25}{X} → (used for $VAR substitution)")
    print(f"\n{B}Shorthands:{X}\n")
    shorthands = [
        ("prereq: X",              "prerequisite: {{ focus: X }} (AND)"),
        ("prereq: [A, B]",         "prerequisite: {{ focus: A focus: B }} (AND, both required)"),
        ("prereq_or: [A, B]",      "prerequisite: {{ focus: A }} prerequisite: {{ focus: B }} (OR)"),
        ("reward:",                "completion_reward:"),
        ("rel_pos: X",             "relative_position_id: X"),
        ("hidden: {{...}}",        "hidden_effect: {{...}}"),
        ("ai_will_do: N",          "ai_will_do: {{ factor: N }}"),
        ("ai_will_do.if: [...]",   "modifier blocks with factor/conditions"),
        ("add_state_building:",    "state_id = {{ add_building_construction = {{...}} }}"),
        ("add_state_manpower:",    "state_id = {{ add_manpower = N }}"),
        ("regiments: [...]",       "regiment blocks with column/row auto-assigned"),
        ("support_companies: [...]","support blocks with column/row auto-assigned"),
        ("sprites: [...]",         "spriteTypes: {{ spriteType: [...] }}"),
        ("set_tech: [A, B]",       "set_technology: {{ A: 1, B: 1 }}"),
        ("set_ruling_party: X",    "set_politics: {{ ruling_party: X, elections_allowed: no, election_frequency: 48 }}"),
        ("add_pop: {{X: 0.1}}",    "add_popularity: {{ ideology: X, popularity: 0.1 }}"),
        ("_category: country",     "ideas: {{ country: {{...}} }}"),
        ("_wrap: characters",      "characters: {{...}}"),
        ("_template: X",           "inherit from templates.X"),
        ("_if: false",             "skip this entry"),
    ]
    for short, expanded in shorthands:
        print(f"  {G}{short:<30}{X} → {expanded}")
    print(f"\n{B}Common mistakes (validated):{X}\n")
    notes = [
        ("ideology/ruling_party",  "checked against game data"),
        ("traits",                 "checked per context: country_leader vs unit_leader"),
        ("categories (tech)",      "checked against tech categories from game files"),
        ("building levels",        "checked against state_max from game files"),
        ("resources",              "checked against game data (oil/aluminium/steel etc.)"),
        ("unit types",             "checked against sub_unit definitions from game files"),
        ("equipment types",        "checked against equipment definitions from game files"),
        ("modifier names",         "checked against 638 modifier names from game files"),
        ("wargoal types",          "checked against wargoal_types from game files"),
        ("effect in trigger block","has_war/is_major etc. in completion_reward → WARN"),
        ("trigger in effect block","add_stability etc. in trigger/limit → WARN"),
        ("modifier in effect ctx", "modifier: {{...}} in completion_reward does nothing → WARN"),
        ("set_technology type key","set_technology: {{type: X}} is wrong syntax → WARN"),
        ("add_tech_bonus category","missing category field → WARN"),
        ("set_politics fields",    "missing ruling_party/elections_allowed/election_frequency → WARN"),
        ("add_popularity fields",  "missing ideology/popularity → WARN"),
        ("create_wargoal fields",  "missing type/target → WARN"),
        ("equipment_bonus instant","missing instant: yes → only new production affected → WARN"),
        ("add_core_of vs add_core","add_core_of=TAG, add_core=state_id — reversed → WARN"),
        ("capital province ID",    "capital takes province ID not state ID → WARN"),
        ("load_oob reference",     "checked against history_units entries → WARN"),
        ("technology path/folder", "missing path or folder → won't appear in tech tree → WARN"),
        ("event fire condition",   "no is_triggered_only or mean_time_to_happen → WARN"),
        ("event option name",      "option without name key → WARN"),
        ("news_event in option",   "fires for ALL countries → WARN"),
        ("add_to_variable",        "without clamp_variable → WARN"),
        ("remove_ideas",           "on removal_cost: -1 ideas → WARN"),
        ("character (singular)",   "should be 'characters' → WARN"),
        ("ai_will_do: {{factor: 0}}","AI never picks this → WARN"),
        ("random_list non-numeric","weights must be numbers → WARN"),
        ("GFX keys",               "checked against game + mod sprite definitions"),
        ("localisation keys",      "missing loc keys for events/focuses/ideas → WARN"),
        ("duplicate IDs",          "focus IDs and event IDs checked for duplicates"),
    ]
    for key, note in notes:
        print(f"  {G}{key:<30}{X} {note}")


def parse_args(args):
    flags = set()
    files = []
    output_dir = Path("output")
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--output" and i + 1 < len(args):
            output_dir = Path(args[i + 1]); i += 2
        elif a.startswith("--"):
            flags.add(a); i += 1
        else:
            files.append(a); i += 1
    return files or ["mod.yaml"], flags, output_dir


def main():
    args = sys.argv[1:]

    if not args or args[0] == "--list":
        do_list(); return
    if args[0] == "--init":
        do_init(); return
    if args[0] == "--import":
        if len(args) < 2:
            print(f"{R}Usage:{X} generate.py --import <file_or_dir>"); return
        do_import(args[1]); return

    if args[0] == "--list-states":
        import difflib
        query = args[1].lower() if len(args) > 1 else ""
        state_map, _, _ = get_game_maps()
        if query:
            exact = {n: sid for n, sid in state_map.items() if query in n}
            fuzzy = {n: state_map[n] for n in difflib.get_close_matches(query, state_map.keys(), n=10, cutoff=0.4)}
            results = {**exact, **fuzzy}
            if query.isdigit():
                qid = int(query)
                id_to_name = {v: k for k, v in state_map.items()}
                for sid in range(max(1, qid - 2), qid + 3):
                    if sid in id_to_name:
                        results[id_to_name[sid]] = sid
        else:
            results = dict(sorted(state_map.items(), key=lambda x: x[1])[:30])
        for name, sid in sorted(results.items(), key=lambda x: x[1]):
            print(f"  {sid:4}  {name}")
        return

    if args[0] == "--list-countries":
        query = args[1].lower() if len(args) > 1 else ""
        _, _, country_map = get_game_maps()
        results = {n: t for n, t in country_map.items() if not query or query in n or query in t.lower()}
        for name, tag in sorted(results.items(), key=lambda x: x[1]):
            print(f"  {tag}  {name}")
        return

    files, flags, output_dir = parse_args(args)

    if "--validate" in flags or "--check" in flags:
        config = preprocess(load_configs(files))
        validate(config)
        if _utils._warn_count == 0:
            print(f"{G}No issues found.{X}")
        return

    kw = dict(
        clean=("--clean" in flags),
        dry_run=("--dry-run" in flags),
        output_dir=output_dir,
        do_zip=("--zip" in flags),
        diff_only=("--diff" in flags),
    )
    generate(files, **kw)

    if "--watch" in flags:
        print(f"{B}Watching for changes...{X} (Ctrl+C to stop)")
        mtimes = {f: Path(f).stat().st_mtime for f in files}
        while True:
            time.sleep(1)
            if any(Path(f).stat().st_mtime != mtimes[f] for f in files):
                mtimes = {f: Path(f).stat().st_mtime for f in files}
                print("Change detected, regenerating...")
                generate(files, **kw)


if __name__ == "__main__":
    main()
