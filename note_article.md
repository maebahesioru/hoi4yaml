# AIと一緒にHoI4 modを作るツールを作った話

## はじめに

Hearts of Iron IV（HoI4）のmodを作ったことがある人なら分かると思うが、あのClausewitz形式のファイルは書くのがしんどい。

```
focus = {
    id = GER_rearm
    icon = GFX_focus_generic_military_mission
    x = 0
    y = 0
    cost = 10
    completion_reward = {
        add_political_power = 100
    }
}
```

フォーカスが20個あれば、x/yの座標計算だけで頭がおかしくなる。iconのGFX名も覚えられない。localisationファイルは言語ごとに別ファイルで、英語を書いたら同じ内容をフランス語・ドイツ語・スペイン語……と10言語分コピーしなければならない。

しかも最近はAIにmodを書かせたい。でもAIにClausewitz形式を直接書かせると、構文ミスや存在しないtraitを平気で使ってくる。バリデーションがない。

そこで作ったのが **hoi4yaml** だ。

---

## hoi4yamlとは

YAMLでHoI4 modを書くと、Clausewitz形式のファイルを自動生成するツール。

```bash
pip install git+https://github.com/maebahesioru/hoi4yaml.git
hoi4yaml mod.yaml
```

これだけで`common/`・`history/`・`localisation/`などのファイルが全部出てくる。

---

## 何が嬉しいのか

### 1. x/y座標を書かなくていい

フォーカスツリーのx/y位置は、prereq（前提フォーカス）のグラフから自動計算される。

```yaml
national_focus:
  - _file: GER_focuses
    focus_tree:
      focus:
        - id: GER_rearm
          cost: 10
          reward:
            add_political_power: 100

        - id: GER_army
          prereq: GER_rearm
          cost: 10
          reward:
            army_experience: 50
```

`x`も`y`も書いていない。でも生成されたファイルには正しい座標が入っている。

### 2. iconとpictureを書かなくていい

フォーカスのiconは、ゲームのNFファイルとlocalisationを学習して、IDのキーワードから自動推定する。

国家精神のpictureも同様。ゲームのideaファイルとlocalisationのセマンティックマッチで推定し、マッチしなければ`GFX_idea_{id}`にフォールバックする。

### 3. localisationはenglishだけ書けばいい

```yaml
localisation:
  english:
    GER_rearm: "Rearmament"
    GER_rearm_desc: "Germany begins its rearmament."
```

これだけで、french・german・spanish・russian・polish・braz_por・japanese・korean・simp_chineseの全言語ファイルが自動生成される。もちろん特定言語だけ翻訳を上書きすることもできる。

### 4. ショートハンドが充実している

```yaml
# これが
set_tech:
  - infantry_weapons
  - tech_support

# こう展開される
set_technology = {
    infantry_weapons = 1
    tech_support = 1
}
```

他にも`prereq`・`reward`・`rel_pos`・`add_state_building`・`regiments`など多数。

### 5. ステート名・国名を自動解決

ステートIDや国タグを覚えなくていい。

```yaml
add_state_building:
  state: Liberia   # → 7959
  type: industrial_complex
  level: 1

add_opinion_modifier:
  target: ethiopia  # → ETH
  modifier: LIB_african_solidarity
```

ゲームの`history/states/`とlocalisationから名前→IDのマッピングを構築し、書いた名前を自動でIDに変換する。大文字小文字は無視される。

### 6. バリデーションが40種類以上

ゲームファイルから動的に取得した正しいデータと照合する。

- 存在しないideologyを指定したらERROR
- 存在しないtraitを指定したらWARN（候補も表示）
- localisationキーが抜けていたらWARN
- 翻訳されていない言語があったらWARN
- 重複IDがあったらERROR

AIが書いたYAMLをそのまま流し込んでも、ミスを早期に検出できる。

---

## 実際に作ったもの：リベリアmod

試しにリベリア（LIB）の拡張modを作った。1936年のリベリアは独立を保つアフリカの数少ない国のひとつで、ファイアストーン社のゴム農園問題や、アメリコ・リベリア人と先住民の対立など、面白い歴史的背景がある。

YAMLで書いた内容：

- **フォーカスツリー 26本**（経済・軍事・汎アフリカ・政治改革・外交・鉄鉱石・連合国加入）
- **国家精神 15個**
- **キャラクター 6人**（大統領・将軍・政治顧問）
- **イベント 9本**
- **決定事項 5本**
- **英語・日本語ローカライゼーション**

x/y座標は一切書いていない。iconもpictureもほぼ書いていない。全部自動。

```yaml
# フォーカスの例（x/y/icon全部省略）
- id: LIB_iron_ore_survey
  prereq: LIB_modernize_economy
  cost: 10
  reward:
    country_event: { id: LIB.7 }
```

```yaml
# 国家精神の例（picture省略）
LIB_spirit_iron_industry:
  cost: 0
  removal_cost: -1
  modifier:
    industrial_capacity_factory: 0.05
    production_speed_industrial_complex_factor: 0.1
```

---

## AIとの相性

このツールはAIが使うことを前提に設計している。

- **ショートハンドが多い** → AIが書く量が減る
- **バリデーションが厳しい** → AIのミスを早期検出
- **自動推定が多い** → AIがicon名やGFX名を覚えなくていい
- **YAMLは構造が明確** → AIが構文ミスをしにくい

実際、このリベリアmodの大部分はAIと対話しながら書いた。「もっとフォーカスを追加して」と言えば追加してくれるし、バリデーションエラーが出れば自動で修正する。

---

## 対応セクション：190種類以上

HoI4の`common/`以下のほぼ全セクションに対応している。一部を挙げると：

| カテゴリ | 対応セクション例 |
|---|---|
| common/ | national_focus, ideas, decisions, characters, events, technologies, traits, buildings, resources, ... |
| history/ | countries, states, units |
| interface/ | countryguimodule, unitstatsgui, ... |
| gfx/ | spriteTypes, objectTypes, ... |
| map/ | strategic_regions, supply_areas, ... |

`hoi4yaml --list`で全セクション・全ショートハンド・全バリデーションの一覧が出る。

---

## 初回ビルドが遅い理由：ゲームファイルを学習している

初回ビルドは30秒ほどかかる。2回目以降は2秒以下。

何をしているかというと、初回にHoI4のゲームファイルを丸ごと読んで学習し、`.hoi4cache.json`にキャッシュしている。

学習している内容：

- **フォーカスのicon推定用** — ゲームの全NFファイルを読んで「このIDキーワードにはこのicon」というマッピングを構築
- **国家精神のpicture推定用** — ゲームの全ideaファイルを読んで「このlocalisationテキストにはこのpicture」というマッピングを構築（Jaccard類似度）
- **バリデーション用** — 有効なtrait名・ideology名・modifier名・building名などをゲームファイルから取得

ハードコードは最小限で、ゲームのアップデートに自動追従する設計になっている。

---

## バリデーションエラーの実例

AIが書いたYAMLにどんなミスが出るか、実際の例：

```
[ERROR] Unknown ideology: 'fascist' — valid: democratic, fascism, communism, neutrality
[WARN]  Unknown trait (unit_leader): 'artillery_officer' — did you mean: ['career_officer', 'cavalry_officer']?
[WARN]  localisation: japanese is missing 3 translation(s): LIB_new_focus, LIB_new_spirit, LIB_new_event
[ERROR] Duplicate focus id: LIB_reform_military
[WARN]  modifier 'army_attack_bonus' not found — did you mean: 'army_attack_factor'?
```

`fascist`は`fascism`が正しい。`artillery_officer`というtraitは存在しない。こういうミスをAIは平気でやる。バリデーションがなければゲームを起動するまで気づかない。

---

## フォーカスツリーのレイアウトアルゴリズム

x/y自動計算の仕組みを簡単に説明する。

**y座標**はpreqグラフの深さで決まる。prereqがなければy=0、prereqのy+1がそのフォーカスのy。

**x座標**は葉ノードから割り当てる。子を持たないフォーカスにカウンターを2ずつ増やしながら割り当て、親は子のx座標の中央値に配置する。HoI4のフォーカスはx間隔が2単位なので、カウンターも2ずつ増やす。

```
LIB_lone_star (root)
├── LIB_firestone_question
│   ├── LIB_rubber_boom      → x=0
│   └── LIB_american_ties    → x=2
│       親: x=(0+2)/2=1
├── LIB_reform_military      → x=4
└── LIB_voice_of_africa      → x=6
    親: x=(0+6)/2=3
```

prereq_orで複数の親を持つフォーカスは、全親のx中央値に配置される。



```bash
# インストール
pip install git+https://github.com/maebahesioru/hoi4yaml.git

# 生成
hoi4yaml mod.yaml

# クリーンビルド
hoi4yaml mod.yaml --clean

# バリデーションのみ
hoi4yaml mod.yaml --check

# セクション・ショートハンド一覧
hoi4yaml --list
```

HoI4がSteam経由でインストールされていれば、ゲームファイルのパスは自動検出される。

---

## リポジトリ

https://github.com/maebahesioru/hoi4yaml

REFERENCE.mdに全機能のドキュメントがある（1300行超）。

---

## おわりに

HoI4 modは「作りたいものは明確なのに、書くのが面倒」という状況になりやすい。このツールはその「面倒」をできるだけ取り除くことを目指している。

AIと組み合わせれば、アイデアを話すだけでmodのベースが出来上がる。あとはゲームで動かしながら調整するだけ。

興味があればぜひ試してみてほしい。
