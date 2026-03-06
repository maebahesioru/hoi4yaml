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
| `national_focus` | `common/national_focus/*.txt` |
| `events` | `events/*.txt` |
| `ideas` | `common/ideas/*.txt` |
| `decisions` | `common/decisions/*.txt` |
| `decisions_categories` | `common/decisions/categories/*.txt` |
| `technologies` | `common/technologies/*.txt` |
| `on_actions` | `common/on_actions/*.txt` |
| `characters` | `common/characters/*.txt` |
| `portraits` | `common/portraits/*.txt` |
| `country_leader` | `common/country_leader/*.txt` |
| `unit_leader` | `common/unit_leader/*.txt` |
| `scripted_triggers` | `common/scripted_triggers/*.txt` |
| `scripted_effects` | `common/scripted_effects/*.txt` |
| `scripted_localisation` | `common/scripted_localisation/*.txt` |
| `opinion_modifiers` | `common/opinion_modifiers/*.txt` |
| `dynamic_modifiers` | `common/dynamic_modifiers/*.txt` |
| `wargoals` | `common/wargoals/*.txt` |
| `equipment` | `common/units/equipment/*.txt` |
| `units` | `common/units/*.txt` |
| `buildings` | `common/buildings/*.txt` |
| `history_countries` | `history/countries/*.txt` |
| `history_states` | `history/states/*.txt` |
| `history_units` | `history/units/*.txt` |
| `interface` | `interface/*.gfx` |
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
| `_if: false` | Skip this entry entirely |

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
    country_event:
      - id: my_mod.1
        # title and desc auto-set to my_mod.1.t / my_mod.1.d if omitted
        is_triggered_only: yes
        option:
          - name: my_mod.1.a  # auto-set to my_mod.1.a if omitted
            add_political_power: 50
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

### sprites

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
