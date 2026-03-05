# hoi4yaml

YAML → HoI4 mod files generator. Designed for AI-assisted modding with shorthand syntax and extensive validation.

YAML → HoI4 modファイルジェネレーター。AIによるmod制作を前提に設計されており、ショートハンド構文と充実したバリデーションを備えています。

## Install / インストール

```bash
pip install git+https://github.com/maebahesioru/hoi4yaml.git
```

## Usage / 使い方

```bash
hoi4yaml mod.yaml          # generate mod files / modファイルを生成
hoi4yaml mod.yaml --clean  # clean output first / 出力先を削除してから生成
hoi4yaml --list            # show all sections, shorthands, and validations / 一覧表示
```

## mod.yaml structure / 構造

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

## Shorthands / ショートハンド

| Shorthand | Expands to / 展開後 |
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

Run `hoi4yaml --list` for the full list. / 全一覧は `hoi4yaml --list` で確認できます。

## Validation / バリデーション

Automatically checks for 30+ common mistakes including:
以下を含む30種類以上のよくあるミスを自動検出します：

- Unknown ideology/trait/tech category/modifier/resource/unit/equipment names (from game files)
  イデオロギー・トレイト・テックカテゴリ・モディファイア・リソース・ユニット・装備名の誤り（ゲームファイルから取得）
- Wrong effect in trigger context and vice versa / エフェクト/トリガーの混在
- `modifier: {...}` block in effect context (does nothing) / エフェクト内の`modifier`ブロック（無効）
- Missing required fields in `set_politics`, `add_popularity`, `create_wargoal` / 必須フィールド漏れ
- `add_core_of` vs `add_core` argument confusion / 引数の混同
- Event missing `is_triggered_only` or `mean_time_to_happen` / イベントの発火条件漏れ
- Technology missing `path` or `folder` / テクノロジーのツリー定義漏れ
- Building level exceeding game maximum / ビルディング上限超過
- Missing localisation keys, duplicate IDs, unknown GFX keys / ローカライズキー漏れ・ID重複・GFXキー不明

Run `hoi4yaml --list` for the full list. / 全一覧は `hoi4yaml --list` で確認できます。

## Requirements / 動作要件

- Python 3.10+
- Hearts of Iron IV installed (auto-detected via Steam) / HoI4インストール済み（Steamから自動検出）
