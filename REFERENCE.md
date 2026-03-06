# hoi4yaml — Complete Reference

YAML → HoI4 mod files generator. Designed for AI-assisted modding.

GitHub: https://github.com/maebahesioru/hoi4yaml

---

## Install

```bash
pip install git+https://github.com/maebahesioru/hoi4yaml.git
```

Or clone and install locally:

```bash
git clone https://github.com/maebahesioru/hoi4yaml.git
cd hoi4yaml
pip install -e .
```

---

## CLI

```bash
hoi4yaml mod.yaml              # generate mod files
hoi4yaml mod.yaml --clean      # delete output first, then generate
hoi4yaml mod.yaml --check      # validate only, no output
hoi4yaml mod.yaml --diff       # write changed files only
hoi4yaml mod.yaml --dry-run    # show what would be written, no output
hoi4yaml mod.yaml --zip        # generate + zip
hoi4yaml --list                # show all sections, shorthands, validations
hoi4yaml --list-states japan   # search state IDs by name
hoi4yaml --list-countries ger  # search country TAGs by name
hoi4yaml --import path/to/dir  # convert Clausewitz files → YAML
hoi4yaml --init                # create mod.yaml scaffold
```

Output goes to `output/<mod_name>/`.

---

## mod.yaml structure

Every mod.yaml has a `mod:` block at the top, followed by sections.

```yaml
mod:
  name: My Mod
  version: "1.0.0"
  supported_version: "1.14.*"
  tags: [Historical]
  # mod_paths: [path/to/other/mod]  # optional: load GFX/traits/states from other mods

vars:
  TAG: GER   # use as $TAG anywhere in the file

templates:
  my_template:
    cost: 10
    ai_will_do: 1

localisation:
  english:
    MY_key: "My Text"
  japanese:
    MY_key: "テキスト"
```

---

## Sections

Each section is a list of entries. Every entry has a `_file` key that sets the output filename.

| Section | Output path |
|---|---|
| `abilities` | `common/abilities/*.txt` |
| `acclimatation` | `common/*.txt` |
| `aces` | `common/aces/*.txt` |
| `ai_areas` | `common/ai_areas/*.txt` |
| `ai_attitudes` | `common/*.txt` |
| `ai_equipment` | `common/ai_equipment/*.txt` |
| `ai_equipment_designs` | `common/ai_equipment_designs/*.txt` |
| `ai_faction_theaters` | `common/ai_faction_theaters/*.txt` |
| `ai_focuses` | `common/ai_focuses/*.txt` |
| `ai_navy` | `common/ai_navy/*.txt` |
| `ai_navy_fleet` | `common/ai_navy/fleet/*.txt` |
| `ai_navy_goals` | `common/ai_navy/goals/*.txt` |
| `ai_navy_taskforce` | `common/ai_navy/taskforce/*.txt` |
| `ai_peace` | `common/ai_peace/*.txt` |
| `ai_personalities` | `common/*.txt` |
| `ai_strategy` | `common/ai_strategy/*.txt` |
| `ai_strategy_plans` | `common/ai_strategy_plans/*.txt` |
| `ai_templates` | `common/ai_templates/*.txt` |
| `alerts` | `common/*.txt` |
| `autonomous_states` | `common/autonomous_states/*.txt` |
| `autonomy` | `common/autonomy/*.txt` |
| `bookmarks` | `common/bookmarks/*.txt` |
| `bop` | `common/bop/*.txt` |
| `buildings` | `common/buildings/*.txt` |
| `characters` | `common/characters/*.txt` |
| `collections` | `common/collections/*.txt` |
| `combat_tactics` | `common/*.txt` |
| `continuous_focus` | `common/continuous_focus/*.txt` |
| `cosmetic_tags` | `common/cosmetic_tags/*.txt` |
| `country_colors` | `common/countries/*.txt` |
| `country_leader` | `common/country_leader/*.txt` |
| `country_metadata` | `country_metadata/*.txt` |
| `country_tag_aliases` | `common/country_tag_aliases/*.txt` |
| `country_tags` | `common/country_tags/*.txt` |
| `decisions` | `common/decisions/*.txt` |
| `decisions_categories` | `common/decisions/categories/*.txt` |
| `defines` | `common/defines/*.lua` |
| `difficulty_settings` | `common/difficulty_settings/*.txt` |
| `dlc_metadata` | `dlc_metadata/dlc_info/*.txt` |
| `doctrines` | `common/doctrines/*.txt` |
| `doctrines_folders` | `common/doctrines/folders/*.txt` |
| `doctrines_grand` | `common/doctrines/grand_doctrines/*.txt` |
| `doctrines_sub_air` | `common/doctrines/subdoctrines/air/*.txt` |
| `doctrines_sub_land` | `common/doctrines/subdoctrines/land/*.txt` |
| `doctrines_sub_sea` | `common/doctrines/subdoctrines/sea/*.txt` |
| `doctrines_tracks` | `common/doctrines/tracks/*.txt` |
| `dynamic_modifiers` | `common/dynamic_modifiers/*.txt` |
| `equipment` | `common/units/equipment/*.txt` |
| `equipment_groups` | `common/equipment_groups/*.txt` |
| `equipment_modules` | `common/units/equipment/modules/*.txt` |
| `equipment_upgrades` | `common/units/equipment/upgrades/*.txt` |
| `event_modifiers` | `common/*.txt` |
| `events` | `events/*.txt` |
| `factions` | `common/factions/*.txt` |
| `factions_goals` | `common/factions/goals/*.txt` |
| `factions_icons` | `common/factions/icons/*.txt` |
| `factions_member_upgrades` | `common/factions/member_upgrades/*.txt` |
| `factions_member_groups` | `common/factions/member_upgrades/member_groups/*.txt` |
| `factions_rules` | `common/factions/rules/*.txt` |
| `factions_rules_groups` | `common/factions/rules/groups/*.txt` |
| `factions_templates` | `common/factions/templates/*.txt` |
| `factions_upgrades` | `common/factions/upgrades/*.txt` |
| `factions_upgrades_groups` | `common/factions/upgrades/groups/*.txt` |
| `focus_inlay_windows` | `common/focus_inlay_windows/*.txt` |
| `frontend` | `common/frontend/*.txt` |
| `frontend_backgrounds` | `common/frontend/backgrounds/*.txt` |
| `game_rules` | `common/game_rules/*.txt` |
| `generation` | `common/generation/*.txt` |
| `gfx_3dviewenv` | `gfx/3dviewenv/*.txt` |
| `gfx_army_icons` | `gfx/army_icons/*.txt` |
| `gfx_entities` | `gfx/entities/*.asset` |
| `gfx_equipment_icons` | `gfx/interface/equipmentdesigner/graphic_db/*.txt` |
| `gfx_maparrows` | `gfx/maparrows/*.txt` |
| `gfx_models` | `gfx/models/*.asset` |
| `gfx_models_anim_blend` | `gfx/models/anim_blend_test/*.asset` |
| `gfx_models_buildings` | `gfx/models/buildings/*.asset` |
| `gfx_models_buildings_canal_locks` | `gfx/models/buildings/canal_locks/*.asset` |
| `gfx_models_buildings_dams` | `gfx/models/buildings/dams/*.asset` |
| `gfx_models_buildings_landmarks` | `gfx/models/buildings/landmarks/*.asset` |
| `gfx_models_mapitems` | `gfx/models/mapitems/*.asset` |
| `gfx_models_supply_trains` | `gfx/models/supply/trains/*.asset` |
| `gfx_models_units` | `gfx/models/units/*.asset` |
| `gfx_models_units_armored_ev` | `gfx/models/units/armored_engineering_vehicles/*.asset` |
| `gfx_models_units_command_vehicles` | `gfx/models/units/command_vehicles/*.asset` |
| `gfx_models_units_flame_tanks` | `gfx/models/units/flame_tanks/*.asset` |
| `gfx_models_units_helicopters` | `gfx/models/units/helicopters/*.asset` |
| `gfx_models_units_howitzers` | `gfx/models/units/howitzers/*.asset` |
| `gfx_models_units_land_cruisers` | `gfx/models/units/land_cruisers/*.asset` |
| `gfx_models_units_planes` | `gfx/models/units/planes/*.asset` |
| `gfx_models_units_railway_guns` | `gfx/models/units/railway_guns/*.asset` |
| `gfx_models_units_ships` | `gfx/models/units/ships/*.asset` |
| `gfx_models_units_tanks` | `gfx/models/units/tanks/*.asset` |
| `gfx_models_units_trains` | `gfx/models/units/trains/*.asset` |
| `gfx_models_units_vehicles` | `gfx/models/units/vehicles/*.asset` |
| `gfx_naval_combat` | `gfx/*.txt` |
| `gfx_particles` | `gfx/particles/*.asset` |
| `gfx_particles_environment` | `gfx/particles/environment/*.asset` |
| `gfx_particles_infantry` | `gfx/particles/infantry/*.asset` |
| `gfx_particles_vehicles` | `gfx/particles/vehicles/*.asset` |
| `gfx_posteffect` | `gfx/*.txt` |
| `gfx_train_db` | `gfx/train_gfx_database/*.txt` |
| `graphicalculturetype` | `common/*.txt` |
| `history_countries` | `history/countries/*.txt` |
| `history_general` | `history/general/*.txt` |
| `history_provinces` | `history/provinces/*.txt` |
| `history_states` | `history/states/*.txt` |
| `history_units` | `history/units/*.txt` |
| `idea_tags` | `common/idea_tags/*.txt` |
| `ideas` | `common/ideas/*.txt` |
| `ideologies` | `common/ideologies/*.txt` |
| `intelligence_agencies` | `common/intelligence_agencies/*.txt` |
| `intelligence_agency_upgrades` | `common/intelligence_agency_upgrades/*.txt` |
| `interface` | `interface/*.gfx` |
| `interface_gui` | `interface/*.gui` |
| `interface_building_roster` | `interface/building_roster/*.gfx` |
| `interface_buildings` | `interface/buildings/*.gfx` |
| `interface_career_profile` | `interface/career_profile/*.gfx` |
| `interface_doctrines` | `interface/doctrines/*.gfx` |
| `interface_equipmentdesigner` | `interface/equipmentdesigner/*.gfx` |
| `interface_equipmentdesigner_planes` | `interface/equipmentdesigner/planes/*.gfx` |
| `interface_equipmentdesigner_ships` | `interface/equipmentdesigner/ships/*.gfx` |
| `interface_equipmentdesigner_tanks` | `interface/equipmentdesigner/tanks/*.gfx` |
| `interface_factions` | `interface/factions/*.gfx` |
| `interface_integrity` | `interface/integrity/*.gfx` |
| `interface_intl_market` | `interface/international_market/*.gfx` |
| `interface_mio` | `interface/military_industrial_organization/*.gfx` |
| `interface_military_raids` | `interface/military_raids/*.gfx` |
| `interface_notifications` | `interface/notifications/*.gfx` |
| `interface_pdx_online` | `interface/pdx_online/*.gfx` |
| `interface_special_projects` | `interface/special_projects/*.gfx` |
| `interface_widgets` | `interface/widgets/*.gfx` |
| `map_adjacency_rules` | `map/*.txt` |
| `map_ambient_object` | `map/*.txt` |
| `map_buildings` | `map/*.txt` |
| `map_cities` | `map/*.txt` |
| `map_colors` | `map/*.txt` |
| `map_continent` | `map/*.txt` |
| `map_modes` | `common/map_modes/*.txt` |
| `map_positions` | `map/*.txt` |
| `map_railways` | `map/*.txt` |
| `map_seasons` | `map/*.txt` |
| `map_supply_nodes` | `map/*.txt` |
| `map_terrain` | `map/terrain/*.txt` |
| `map_unitstacks` | `map/*.txt` |
| `map_weatherpositions` | `map/*.txt` |
| `medals` | `common/medals/*.txt` |
| `military_industrial_organization` | `common/military_industrial_organization/*.txt` |
| `mio_ai_bonus_weights` | `common/military_industrial_organization/ai_bonus_weights/*.txt` |
| `mio_organizations` | `common/military_industrial_organization/organizations/*.txt` |
| `mio_policies` | `common/military_industrial_organization/policies/*.txt` |
| `modifier_definitions` | `common/modifier_definitions/*.txt` |
| `modifiers` | `common/modifiers/*.txt` |
| `mtth` | `common/mtth/*.txt` |
| `music` | `music/*.asset` |
| `music_hoi2` | `music/hoi2/*.asset` |
| `music_hoi3` | `music/hoi3/*.asset` |
| `named_colors` | `common/named_colors/*.txt` |
| `names` | `common/names/*.txt` |
| `national_focus` | `common/national_focus/*.txt` |
| `occupation_laws` | `common/occupation_laws/*.txt` |
| `on_actions` | `common/on_actions/*.txt` |
| `operation_phases` | `common/operation_phases/*.txt` |
| `operation_tokens` | `common/operation_tokens/*.txt` |
| `operations` | `common/operations/*.txt` |
| `opinion_modifiers` | `common/opinion_modifiers/*.txt` |
| `pdx_online_assets` | `pdx_online_assets/interface/*.gfx` |
| `peace_conference` | `common/peace_conference/*.txt` |
| `peace_conference_ai` | `common/peace_conference/ai_peace/*.txt` |
| `peace_conference_categories` | `common/peace_conference/categories/*.txt` |
| `peace_conference_cost_modifiers` | `common/peace_conference/cost_modifiers/*.txt` |
| `portraits` | `common/portraits/*.txt` |
| `profile_backgrounds` | `common/profile_backgrounds/*.txt` |
| `profile_pictures` | `common/profile_pictures/*.txt` |
| `raids` | `common/raids/*.txt` |
| `raids_categories` | `common/raids/categories/*.txt` |
| `region_colors` | `common/*.txt` |
| `resistance_activity` | `common/resistance_activity/*.txt` |
| `resistance_compliance_modifiers` | `common/resistance_compliance_modifiers/*.txt` |
| `resources` | `common/resources/*.txt` |
| `ribbons` | `common/ribbons/*.txt` |
| `scientist_traits` | `common/scientist_traits/*.txt` |
| `scorers` | `common/scorers/*.txt` |
| `scorers_country` | `common/scorers/country/*.txt` |
| `script` | `script/*.lua` |
| `script_constants` | `common/script_constants/*.txt` |
| `script_enums` | `common/*.txt` |
| `scripted_diplomatic_actions` | `common/scripted_diplomatic_actions/*.txt` |
| `scripted_effects` | `common/scripted_effects/*.txt` |
| `scripted_gui` | `common/scripted_guis/*.txt` |
| `scripted_localisation` | `common/scripted_localisation/*.txt` |
| `scripted_triggers` | `common/scripted_triggers/*.txt` |
| `scripted_variables` | `common/scripted_variables/*.txt` |
| `sound` | `sound/*.asset` |
| `sound_animations` | `sound/animations/*.asset` |
| `sound_gui` | `sound/gui/*.asset` |
| `sound_gui_gtd` | `sound/gui/gtd/*.asset` |
| `sound_gui_sea` | `sound/gui/sea/*.asset` |
| `sound_menu` | `sound/menu/*.asset` |
| `sound_weather` | `sound/weather/*.asset` |
| `special_projects` | `common/special_projects/*.txt` |
| `special_projects_projects` | `common/special_projects/projects/*.txt` |
| `special_projects_rewards` | `common/special_projects/prototype_rewards/*.txt` |
| `special_projects_specialization` | `common/special_projects/specialization/*.txt` |
| `special_projects_tags` | `common/special_projects/project_tags/*.txt` |
| `state_category` | `common/state_category/*.txt` |
| `strategic_locations` | `common/strategic_locations/*.txt` |
| `strategic_regions` | `map/strategicregions/*.txt` |
| `supply_areas` | `map/supplyareas/*.txt` |
| `technologies` | `common/technologies/*.txt` |
| `technology_sharing` | `common/technology_sharing/*.txt` |
| `technology_tags` | `common/technology_tags/*.txt` |
| `terrain` | `common/terrain/*.txt` |
| `timed_activities` | `common/timed_activities/*.txt` |
| `triggered_modifiers` | `common/triggered_modifiers/*.txt` |
| `tutorial` | `tutorial/*.txt` |
| `unit_leader` | `common/unit_leader/*.txt` |
| `unit_medals` | `common/unit_medals/*.txt` |
| `unit_tags` | `common/unit_tags/*.txt` |
| `units` | `common/units/*.txt` |
| `units_codenames` | `common/units/codenames_operatives/*.txt` |
| `units_critical_parts` | `common/units/critical_parts/*.txt` |
| `units_modifiers` | `common/units/unit_modifiers/*.txt` |
| `units_names` | `common/units/names/*.txt` |
| `units_names_divisions` | `common/units/names_divisions/*.txt` |
| `units_names_railway_guns` | `common/units/names_railway_guns/*.txt` |
| `units_names_ships` | `common/units/names_ships/*.txt` |
| `wargoals` | `common/wargoals/*.txt` |
| `weather` | `common/*.txt` |
| `localisation` | `localisation/mod_l_<lang>.yml` |

---

## Special entry keys

| Key | Meaning |
|---|---|
| `_file: name` | Output filename (without extension) |
| `_namespace: X` | Event namespace (default: same as `_file`) |
| `_category: country` | Wrap content in `ideas: { country: { ... } }` |
| `_wrap: characters` | Wrap content in `characters: { ... }` |
| `_template: X` | Inherit from `templates.X`, then override |
| `_if: false` | Skip this entry entirely — must be Python `false` (not a string or expression) |

---

## Shorthands

### Focus tree

```yaml
national_focus:
  - _file: my_focuses
    focus_tree:
      id: my_tree
      country:
        factor: 0
        modifier:
          add: 10
          tag: GER
      focus:
        - id: GER_focus_1
          x: 0
          y: 0
          cost: 10
          # icon and desc are auto-assigned from id if omitted
          prereq: GER_focus_0          # → prerequisite: { focus: GER_focus_0 }  (AND)
          prereq: [A, B]               # → prerequisite: { focus: [A, B] }       (AND, both)
          prereq_or: [A, B]            # → prerequisite: { focus: A }            (OR)
                                       #   prerequisite: { focus: B }
          rel_pos: GER_focus_0         # → relative_position_id: GER_focus_0
          reward:                      # → completion_reward:
            add_political_power: 100
          ai_will_do: 5                # → ai_will_do: { factor: 5 }
          hidden:                      # → hidden_effect:
            set_country_flag: my_flag
```

x/y are auto-calculated from prereq graph if omitted.
icon is auto-guessed from focus id keywords if omitted.
desc is auto-set to `{id}_desc` if omitted.

### Ideas

```yaml
ideas:
  - _file: my_ideas
    _category: country        # → ideas: { country: { ... } }
    my_idea:
      picture: GFX_idea_my_idea
      removal_cost: -1
      modifier:
        stability_factor: 0.05
```

### Events

```yaml
events:
  - _file: my_events
    _namespace: my_mod        # must match event ID prefix
    country_event:            # fires for a country
      - id: my_mod.1
        # title and desc auto-set to my_mod.1.t / my_mod.1.d if omitted
        is_triggered_only: yes
        option:
          - name: my_mod.1.a  # auto-set to my_mod.1.a if omitted
            add_political_power: 50
    news_event:               # fires for ALL countries (use sparingly)
      - id: my_mod.2
        is_triggered_only: yes
        option:
          - name: my_mod.2.a
    state_event:              # fires for a state scope
      - id: my_mod.3
        is_triggered_only: yes
        option:
          - name: my_mod.3.a
```

### History

```yaml
history_countries:
  - _file: GER
    capital: 11650            # province ID (not state ID)
    set_tech:                 # → set_technology: { infantry_weapons: 1, ... }
      - infantry_weapons
      - tech_support
    set_ruling_party: fascism # → set_politics: { ruling_party: fascism, elections_allowed: no, election_frequency: 48 }
    add_pop:                  # → add_popularity: { ideology: fascism, popularity: 0.3 }
      fascism: 0.3

history_states:
  - _file: 64_berlin
    state:
      id: 64
      name: STATE_64
      history:
        owner: GER
        add_core_of: GER

history_units:
  - _file: GER_1936
    division_template:
      - name: "Infantry Division"
        regiments:            # → regiment blocks with column/row auto-assigned
          - infantry: 9
          - artillery_brigade: 1
        support_companies:
          - engineer: 1
```

### Opinion modifiers

```yaml
opinion_modifiers:
  - _file: my_opinion_modifiers
    _wrap: opinion_modifiers   # REQUIRED — must wrap in opinion_modifiers = { }
    my_modifier:
      value: 30
      decay: 1
      max: 30
```

### Characters

```yaml
characters:
  - _file: my_characters
    _wrap: characters
    GER_leader:
      name: "Adolf Hitler"
      portraits:
        civilian:
          large: GFX_portrait_GER_hitler
      country_leader:
        ideology: nazism
        traits: [dictator]
```

### Technologies

```yaml
technologies:
  - _file: my_techs
    my_tech:
      research_cost: 1.5
      start_year: 1936
      folder:
        name: infantry_folder
        position: { x: 0, y: 0 }
      path:
        - leads_to_tech: my_tech_2
          research_cost_factor: 1
      categories: [infantry]
      on_research_complete:
        add_political_power: 50
```

### Interface / GFX

```yaml
interface:
  - _file: my_interface
    sprites:                  # → spriteTypes: { spriteType: [...] }
      - name: GFX_my_sprite
        texturefile: "gfx/interface/my_sprite.dds"
```

---

## Name resolution

State names and country names are automatically resolved:

```yaml
# States: name → ID
add_state_building:
  state: berlin       # → resolved to state ID (e.g. 64)
  type: industrial_complex
  level: 3

# Countries: name → TAG
add_opinion_modifier:
  target: ethiopia    # → ETH
  modifier: my_modifier

owner: germany        # → GER
```

Use `hoi4yaml --list-states <query>` and `hoi4yaml --list-countries <query>` to look up IDs/TAGs.

---

## Variables and templates

```yaml
vars:
  TAG: GER
  PREFIX: ger_focus

templates:
  standard_focus:
    cost: 10
    ai_will_do: 1

national_focus:
  - _file: $TAG_focuses
    focus_tree:
      focus:
        - id: $PREFIX_first
          _template: standard_focus
          x: 0
          y: 0
          reward:
            add_political_power: 100
```

---

## Validation

The following are automatically checked on every run:

| Check | Details |
|---|---|
| Ideology names | Checked against game files |
| Trait names | Checked per context (country_leader vs unit_leader) |
| Tech category names | Checked against game files |
| Building levels | Checked against state_max from game files |
| Resource names | oil, aluminium, steel, etc. |
| Unit types | sub_unit definitions from game files |
| Equipment types | equipment definitions from game files |
| Modifier names | 638 modifier names from game files |
| Wargoal types | wargoal_types from game files |
| Country TAGs | Checked against all tags in game files |
| Duplicate key in YAML | `add_opinion_modifier` twice → WARN (use list) |
| Effect in trigger block | has_war/is_major in completion_reward → WARN |
| Trigger in effect block | add_stability in trigger/limit → WARN |
| `modifier:` in effect context | Does nothing → WARN |
| `set_technology: {type: X}` | Wrong syntax → WARN |
| `add_tech_bonus` missing category | → WARN |
| `set_politics` missing fields | ruling_party/elections_allowed/election_frequency → WARN |
| `add_popularity` missing fields | ideology/popularity → WARN |
| `create_wargoal` missing fields | type/target → WARN |
| `equipment_bonus` missing `instant` | → WARN |
| `add_core_of` vs `add_core` | Reversed arguments → WARN |
| `capital` looks like state ID | Takes province ID, not state ID → WARN |
| `load_oob` reference | Checked against history_units entries → WARN |
| Technology missing `path`/`folder` | Won't appear in tech tree → WARN |
| Event missing fire condition | No is_triggered_only or mean_time_to_happen → WARN |
| Event option missing `name` | → WARN |
| `news_event` in effect context | Fires for ALL countries → WARN |
| `add_to_variable` without `clamp_variable` | → WARN |
| `remove_ideas` on non-removable idea | removal_cost: -1 → WARN |
| `character` (singular) | Should be `characters` → WARN |
| `ai_will_do: {factor: 0}` | AI never picks this → WARN |
| `random_list` non-numeric keys | Weights must be numbers → WARN |
| Unknown GFX keys | Checked against game + mod sprites → WARN |
| Missing localisation keys | For events/focuses/ideas → WARN |
| Duplicate IDs | Focus IDs and event IDs → WARN |

### add_state_building / add_state_manpower

```yaml
reward:
  add_state_building:
    state: berlin          # state name or ID
    type: industrial_complex
    level: 3
    instant: true          # default: true
  add_state_manpower:
    state: 64              # state ID
    value: 10000
```

Expands to:
```
64 = {
    add_building_construction = { type = industrial_complex level = 3 instant_build = yes }
    add_manpower = 10000
}
```

### timed_idea

```yaml
reward:
  timed_idea:
    idea: my_timed_idea
    days: 180
```

Expands to `add_ideas = my_timed_idea` plus an `if` block that only adds the idea if not already present. The `days` value is informational only — `days_remove` must also be set on the idea definition itself.

Also supports `state_id` as an alternative to `state` in `add_state_building`/`add_state_manpower`:

```yaml
add_state_building:
  state_id: 64       # use state_id if you already know the numeric ID
  type: industrial_complex
  level: 3
```

### ai_will_do with conditions

```yaml
ai_will_do: 1                  # simple: factor 1

ai_will_do:                    # with conditional modifiers
  factor: 1
  if:
    - has_war: yes
      mult: 2                  # multiply factor by 2 if at war
    - tag: GER
      mult: 0                  # never pick if Germany
```

Expands to:
```
ai_will_do = {
    factor = 1
    modifier = { factor = 2 has_war = yes }
    modifier = { factor = 0 tag = GER }
}
```

### support_companies

```yaml
history_units:
  - _file: GER_1936
    division_template:
      - name: "Infantry Division"
        regiments:
          - infantry: 9      # value = number of battalions of that type
          - artillery_brigade: 1
        support_companies:
          - engineer: 1
          - recon: 1
```

`regiments` value is the **count** of battalions. `infantry: 9` creates 9 infantry battalions, auto-assigned to column/row (5 per row). `support_companies` value is always 1 (one company per slot).

Expands to `regiment = { type = infantry column = 0 row = 0 }` ... `support = { type = engineer column = 0 row = 0 }` etc.

### Decisions

```yaml
decisions:
  - _file: my_decisions
    my_category:              # decision category key (must match decisions_categories)
      my_decision:
        icon: generic_political_discourse
        cost: 50              # political power cost
        days_remove: 60       # duration (0 = instant)
        available:            # trigger: when can it be taken
          tag: GER
          has_war: no
        visible:              # trigger: when is it shown (optional)
          tag: GER
        modifier:             # ongoing effect while active
          stability_factor: 0.05
        complete_effect:      # fires when taken
          add_political_power: 25
        remove_effect:        # fires when duration ends
          add_stability: 0.05
        ai_will_do:
          factor: 1

decisions_categories:
  - _file: my_categories
    my_category:
      icon: generic_political_discourse
      picture: GFX_decision_cat_my_category
```

### Unit leaders (field_marshal / corps_commander / navy_leader)

```yaml
characters:
  - _file: my_characters
    _wrap: characters
    GER_rommel:
      name: "Erwin Rommel"
      portraits:
        army:
          large: GFX_portrait_GER_rommel
      field_marshal:
        traits: [brilliant_strategist, desert_fox]
        skill: 4
        attack_skill: 4
        defense_skill: 3
        planning_skill: 4
        logistics_skill: 3
    GER_guderian:
      name: "Heinz Guderian"
      portraits:
        army:
          large: GFX_portrait_GER_guderian
      corps_commander:
        traits: [panzer_leader, fast_planner]
        skill: 4
        attack_skill: 5
        defense_skill: 2
        planning_skill: 4
        logistics_skill: 3
    GER_raeder:
      name: "Erich Raeder"
      portraits:
        navy:
          large: GFX_portrait_GER_raeder
      navy_leader:
        traits: [fleet_in_being_expert]
        skill: 3
        attack_skill: 3
        defense_skill: 3
        maneuvering_skill: 2
        coordination_skill: 3
```

### on_actions

```yaml
on_actions:
  - _file: my_on_actions
    on_startup:
      effect:
        GER = { add_political_power: 50 }
    on_monthly_GER:
      effect:
        add_political_power: 5
    on_war_won:
      effect:
        add_stability: 0.05
```

### scripted_triggers / scripted_effects

```yaml
scripted_triggers:
  - _file: my_triggers
    my_is_major_democracy:
      is_major: yes
      has_government: democratic

scripted_effects:
  - _file: my_effects
    my_boost_industry:
      add_ideas: my_industry_spirit
      add_political_power: 50
```

Use them in other blocks:

```yaml
reward:
  my_boost_industry: yes    # calls the scripted effect

trigger:
  my_is_major_democracy: yes  # calls the scripted trigger
```

### Complete minimal mod example

```yaml
mod:
  name: My First Mod
  version: "1.0"
  supported_version: "1.14.*"

national_focus:
  - _file: GER_focuses
    focus_tree:
      id: GER_focus_tree
      country:
        factor: 0
        modifier:
          add: 10
          tag: GER
      focus:
        - id: GER_rearm
          x: 0
          y: 0
          cost: 10
          reward:
            add_political_power: 100

ideas:
  - _file: GER_ideas
    _category: country
    GER_war_economy:
      picture: generic_production_bonus
      removal_cost: -1
      modifier:
        industrial_capacity_factory: 0.1

decisions:
  - _file: GER_decisions
    GER_political:
      GER_rally_the_nation:
        icon: generic_political_discourse
        cost: 50
        days_remove: 30
        available:
          tag: GER
        complete_effect:
          add_stability: 0.05

characters:
  - _file: GER_characters
    _wrap: characters
    GER_hitler:
      name: "Adolf Hitler"
      portraits:
        civilian:
          large: GFX_portrait_GER_Hitler
      country_leader:
        ideology: nazism
        traits: [dictator]

events:
  - _file: GER_events
    country_event:
      - id: GER_events.1
        is_triggered_only: yes
        option:
          - name: GER_events.1.a
            add_political_power: 50

opinion_modifiers:
  - _file: GER_opinion_modifiers
    _wrap: opinion_modifiers
    GER_rival:
      value: -30
      decay: 1
      min: -30

history_countries:
  - _file: GER
    capital: 11650
    set_tech:
      - infantry_weapons
      - tech_support
    set_ruling_party: fascism
    add_pop:
      fascism: 0.5
    recruit_character: GER_hitler

localisation:
  english:
    GER_rearm: "Rearmament"
    GER_rearm_desc: "Germany begins its secret rearmament program."
    GER_war_economy: "War Economy"
    GER_war_economy_desc: "The nation's industry is geared toward military production."
    GER_rally_the_nation: "Rally the Nation"
    GER_rally_the_nation_desc: "A nationwide rally to boost morale."
    GER_events.1.t: "A New Dawn"
    GER_events.1.d: "Germany stands at a crossroads."
    GER_events.1.a: "Press forward."
    GER_hitler: "Adolf Hitler"
    GER_rival: "Rival Nation"
```



```yaml
interface:
  - _file: my_interface
    sprites:
      - name: GFX_my_focus
        texturefile: "gfx/interface/my_focus.dds"
      - name: GFX_my_idea
        texturefile: "gfx/interface/my_idea.dds"
```

Expands to `spriteTypes = { spriteType = [ ... ] }`.

### set_tech outside history

`set_tech` works anywhere an effect is valid:

```yaml
reward:
  set_tech:
    - infantry_weapons
    - tech_support
```

### _namespace default

If `_namespace` is omitted, it defaults to the value of `_file`:

```yaml
events:
  - _file: my_events          # namespace = "my_events" automatically
    country_event:
      - id: my_events.1       # must start with "my_events."
```

### prereq AND vs OR

```yaml
prereq: A                     # prerequisite: { focus: A }
prereq: [A, B]                # prerequisite: { focus: [A, B] }  — both required (AND)
prereq_or: [A, B]             # prerequisite: { focus: A }
                              # prerequisite: { focus: B }       — either one (OR)
```

### Cache file

`.hoi4cache.json` is created automatically in the project root after the first run. It caches game data (states, countries, ideologies, traits, modifiers, etc.) to speed up subsequent runs. It is invalidated automatically when game files change. Safe to delete — it will be rebuilt on next run. Already in `.gitignore`.

---

```yaml
# color is automatically copied to color_ui if color_ui is omitted
named_colors:
  - _file: my_colors
    my_color:
      color: [0.5, 0.2, 0.1]   # → color + color_ui both set
```

---

## CLI flags (complete)

```bash
hoi4yaml mod.yaml                    # generate
hoi4yaml mod.yaml --clean            # delete output dir first
hoi4yaml mod.yaml --check            # validate only, no output
hoi4yaml mod.yaml --validate         # same as --check
hoi4yaml mod.yaml --diff             # write changed files only
hoi4yaml mod.yaml --dry-run          # show what would be written, no output
hoi4yaml mod.yaml --zip              # generate + zip archive
hoi4yaml mod.yaml --watch            # watch for file changes, regenerate automatically
hoi4yaml mod.yaml --output ./dist    # set output directory (default: ./output)
hoi4yaml a.yaml b.yaml               # merge multiple YAML files into one mod
hoi4yaml --list                      # show all sections, shorthands, validations
hoi4yaml --list-states japan         # search state IDs by name
hoi4yaml --list-countries ger        # search country TAGs by name
hoi4yaml --import path/to/dir        # convert Clausewitz files → YAML
```

`--import` saves output to `imported.yaml` in the current directory. Each file becomes a top-level key named after the filename stem.

### vars substitution scope

`$VAR` substitution works everywhere in the file, including `_file`, `_namespace`, and all keys/values:

```yaml
vars:
  TAG: GER
  PREFIX: ger

national_focus:
  - _file: $TAG_focuses        # → GER_focuses.txt
    _namespace: $PREFIX        # → ger
    focus_tree:
      focus:
        - id: $PREFIX_first_focus
```

```bash
hoi4yaml --import path/to/dir        # convert Clausewitz files → YAML
hoi4yaml --init                      # create mod.yaml scaffold
```

### Multiple YAML files

Split a large mod across multiple files — they are merged at load time:

```bash
hoi4yaml base.yaml focuses.yaml events.yaml
```

Lists are concatenated, dicts are merged. Useful for organizing large mods.

---

## mod_paths — referencing other mods

Load GFX keys, traits, states, ideologies, and localisation keys from other installed mods to avoid false validation warnings:

```yaml
mod:
  name: My Mod
  mod_paths:
    - C:/Users/.../mod/kaiserreich
    - C:/Users/.../mod/road_to_56
```

---

## Common pitfalls

**opinion_modifiers must be wrapped:**
```yaml
opinion_modifiers:
  - _file: my_file
    _wrap: opinion_modifiers   # without this, HoI4 won't load the file
    my_modifier:
      value: 30
```

**Multiple blocks of the same key — use a list:**
```yaml
# WRONG — second entry silently overwrites first
add_opinion_modifier:
  target: ETH
  modifier: X
add_opinion_modifier:
  target: SAF
  modifier: X

# CORRECT
add_opinion_modifier:
  - target: ETH
    modifier: X
  - target: SAF
    modifier: X
```

**Event namespace must match ID prefix:**
```yaml
events:
  - _file: my_events
    _namespace: my_mod    # event IDs must start with "my_mod."
    country_event:
      - id: my_mod.1
```

**capital takes province ID, not state ID:**
```yaml
history_countries:
  - _file: GER
    capital: 11650    # province ID (> 1000), NOT state ID
```

**add_core_of vs add_core:**
```yaml
add_core_of: GER    # takes TAG
add_core: 64        # takes state ID
```

---

## File encoding

- `.txt` files: UTF-8 without BOM
- `.yml` localisation files: UTF-8 with BOM (required by HoI4)

This is handled automatically.

---

## Project structure

```
generate.py          # entry point: CLI, generate(), SECTIONS map
src/
  clausewitz.py      # Clausewitz reader/writer
  utils.py           # write(), warn(), YAML loader, apply_vars/templates
  gamedata.py        # game data loading, cache, name resolution
  icons.py           # focus icon guessing, auto-layout
  shorthands.py      # shorthand expansion
  validation.py      # all validation logic
  generators.py      # gen_section(), gen_localisation()
```
