# hoi4yaml

YAML → HoI4 mod files generator. Designed for AI-assisted modding with shorthand syntax and extensive validation.

## Install

```bash
pip install git+https://github.com/maebahesioru/hoi4yaml.git
```

## Usage

```bash
hoi4yaml mod.yaml          # generate mod files
hoi4yaml mod.yaml --clean  # clean output first
hoi4yaml --list            # show all sections, shorthands, and validations
```

## mod.yaml structure

```yaml
mod:
  name: My Mod
  version: "1.0"
  supported_version: "1.14.*"

national_focus:
  - _file: my_focuses
    focus_tree:
      id: my_focus_tree
      country:
        factor: 0
        modifier:
          add: 10
          tag: GER
      focus:
        - id: GER_first_focus
          x: 0
          y: 0
          reward:
            add_political_power: 100

events:
  - _file: my_events
    country_event:
      - id: my_events.1
        title: my_events.1.t
        desc: my_events.1.d
        is_triggered_only: yes
        option:
          - name: my_events.1.a
            add_political_power: 50

localisation:
  english:
    my_events.1.t: "A New Beginning"
    my_events.1.d: "The nation stands at a crossroads."
    my_events.1.a: "Press forward."
```

## Shorthands

| Shorthand | Expands to |
|---|---|
| `prereq: X` | `prerequisite: { focus: X }` |
| `prereq_or: [A, B]` | two separate `prerequisite` blocks (OR) |
| `reward:` | `completion_reward:` |
| `rel_pos: X` | `relative_position_id: X` |
| `hidden: {...}` | `hidden_effect: {...}` |
| `ai_will_do: 5` | `ai_will_do: { factor: 5 }` |
| `set_tech: [A, B]` | `set_technology: { A: 1, B: 1 }` |
| `set_ruling_party: X` | `set_politics: { ruling_party: X, elections_allowed: no, election_frequency: 48 }` |
| `add_pop: { fascism: 0.1 }` | `add_popularity: { ideology: fascism, popularity: 0.1 }` |
| `add_state_building:` | state-scoped `add_building_construction` |
| `regiments: [...]` | regiment blocks with auto column/row |

Run `hoi4yaml --list` for the full list.

## Validation

Automatically checks for 30+ common mistakes including:
- Unknown ideology/trait/tech category/modifier/resource/unit/equipment names (from game files)
- Wrong effect in trigger context and vice versa
- `modifier: {...}` block in effect context (does nothing)
- Missing required fields in `set_politics`, `add_popularity`, `create_wargoal`
- `add_core_of` vs `add_core` argument confusion
- Event missing `is_triggered_only` or `mean_time_to_happen`
- Technology missing `path` or `folder`
- Building level exceeding game maximum
- Missing localisation keys, duplicate IDs, unknown GFX keys

Run `hoi4yaml --list` for the full list.

## Requirements

- Python 3.10+
- Hearts of Iron IV installed (auto-detected via Steam)
