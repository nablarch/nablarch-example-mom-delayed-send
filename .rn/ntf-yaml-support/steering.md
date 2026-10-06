# Goal

NTF（Nablarch Testing Framework）のAI対応として、AIが読み書きできないバイナリ形式のExcelテストデータをYAML形式に移行する。
参照: https://github.com/Fintan-contents/nablarch-system-development-guide/pull/211

対象プロジェクト: `nablarch-example-mom-delayed-send`

対象は本リポジトリに存在するNTFのExcelテストデータ全件（現時点で1件、`.xlsx`）：
- `src/test/java/com/nablarch/example/ProjectInsertMessageRequestTest.xlsx`

# Acceptance criteria

- `develop` ブランチから作成した `ntf-yaml-support` ブランチで全作業が行われている
- 作業前に既存の全テストがパスすることを確認済みである
- `pom.xml` に `nablarch-testing-yaml:1.0.0-SNAPSHOT` が test スコープの依存として追加されている
- `pom.xml` の `<build><plugins>` に `nablarch-testing-converter:1.0.0-SNAPSHOT` がビルドプラグイン（plugin直下 `<configuration>` に変換パラメータを設定し、CLIで `convert` ゴールを実行）として追加されている（test依存ではない）
- `src/test/resources/unit-test.xml` に `YamlTestDataParser` コンポーネントと `yamlInterpreters` リストが追加されている
- 変換対象の全てのテスト用Excelファイルがそれぞれ対応するYAMLファイルに変換されている（サンプリングでExcelとYAMLの内容が一致することを確認済み）
- 変換後、変換対象だったExcelファイルが全て削除されている
- YAMLテストデータを使った状態で全テストがパスしている
- Excelファイルなしで全テストがパスしていることを確認済みであり、間違えてExcelでパスしていない

# Assumptions

- `nablarch-testing-yaml:1.0.0-SNAPSHOT` と `nablarch-testing-converter:1.0.0-SNAPSHOT` はローカルMavenリポジトリ（`~/.m2`）に存在する（確認済み）
- テスト実行にはH2インメモリDBを使用し、DBセットアップ済みである
- JDK 17 / Maven 3.9.9以降 / H2 などビルド・テスト実行環境は整備済みである
- YAMLファイルの出力先は `src/test/java` 配下（Excelと同じ場所）とし、`nablarch.test.resource-root` の設定変更は不要
- 変換ツール（`nablarch-testing-converter`）の実行手順は `/home/k10949/workspace/nablarch-testing-converter/README.md` に従う

# Build / Test 手順（README確認結果）

対象プロジェクトの `README.md` を確認した結果、本プロジェクトのビルド・テスト手順は以下の通り：

- `-P gsp` のようなプロファイル指定は不要。エンティティ生成を行う `gsp-dba-maven-plugin` は `generate-sources` フェーズに直接バインドされているため、`mvn test`（または `mvn package`）の実行に含まれる。README の「データベースのセットアップ及びエンティティクラスの作成は `mvn package` の実行に含まれる」の記載と一致。
- エンティティ生成を個別に行う場合は `mvn generate-resources`。
- ビルド・テストは `mvn clean test` を使用する。
- **NTFのメッセージ解決は日本語ロケール前提のため、テストは `LANG=ja_JP.UTF-8 LC_ALL=ja_JP.UTF-8` を指定して実行する**（`C.UTF-8` だとメッセージ解決に失敗しテストが落ちる）。
  - 例: `LANG=ja_JP.UTF-8 LC_ALL=ja_JP.UTF-8 mvn clean test`

# Scripts

- `scripts/dump_xlsx.py` — Task #3 のサンプリング比較用。openpyxl 等が未インストールの環境で、Excel テストデータ(.xlsx)の各シートのセル値を標準ライブラリ(zipfile + xml.etree)のみでテキストダンプする。Excel内部の phonetic ruby（ふりがな, `<rPh>`）はセルの実値ではないため除外して出力する。使い方: `python3 .rn/ntf-yaml-support/scripts/dump_xlsx.py <path-to-xlsx>`。

# Rules

- commit every change; one completion marker per task
- push は行わない（コミットのみ実施し、リモートへの push は最後にユーザーが行う）
- テストクラス（`.java`）は変更しない
- `develop` から新規作成した `ntf-yaml-support` ブランチで作業する
- steering.md は各タスクで更新し、当該タスクのコミットに含める
- git add は明示的なパス指定のみ（`git add -A` / `git add .` 禁止）
- テストはExcelファイルが存在しない状態で最終パスを確認する
- YAML変換後はサンプリングでExcelとYAMLの内容を比較してから削除する
- サンプリング比較で差異が見つかった場合は修正せずユーザーに報告して停止する
- user review は順調な場合は task 毎のユーザー確認を不要とし連続して進める。NG・FAILURE/BUILD FAILURE・その他エラー・サンプリング差異が発生した場合のみ、修正を試みず（差異時は修正せず）ユーザーに報告して停止する

# Tasks

### #1: 現状のビルド・テストで全PASSを確認する

**Purpose**: `develop` から `ntf-yaml-support` ブランチを作成し、変更前の状態で全テストがパスすることを確認する。

**Prerequisites**: none

**Steps**:

- [x] `develop` ブランチの存在を確認し、そこから `ntf-yaml-support` ブランチを新規作成する
- [x] 対象プロジェクトの README を確認し、ビルド・テストの実行手順を把握する
- [x] 隣接プロジェクトの `.rn/` 配下MDを参照し、steering.md と scripts の初版を作成する
- [x] README で確認した手順でテストを実行し、全テストがパスすることを確認する（`mvn clean test`。失敗があれば報告して止まる）
- [x] 結果を `checks/task-1.md` に記録する（self-check列のみ）
- [x] 変更ファイル（check ファイルおよび更新した steering.md）をコミットする
- [x] self-check (OK/NG per completion criterion, record in checks/task-1.md)
- [x] QA expert review (Agent: general-purpose / Opus 4.8)
- [x] user review（順調のため確認省略。方針変更あり — Rules 参照）

**Completion criteria**:

- `ntf-yaml-support` ブランチが `develop` ブランチから作成されている
- `mvn test` が全テストパスで終了している（BUILD SUCCESS）

### #2: 設定変更 — pom.xml と unit-test.xml にYAML対応を追加

**Purpose**: `pom.xml` に `nablarch-testing-yaml`（test 依存）を追加し、`nablarch-testing-converter` を `<build><plugins>` のビルドプラグインとして追加し、`unit-test.xml` に `yamlInterpreters` リストと `YamlTestDataParser` コンポーネントの設定を追加する。設定内容は隣接プロジェクト（nablarch-example-web / nablarch-example-batch）のYAML対応設定を参考にする。converter はテスト実行時には不要で XLS→YAML 変換時のみ使う Maven プラグインのため、test 依存ではなくビルドプラグインとして宣言する。

**Prerequisites**: #1

**Steps**:

- [x] `pom.xml` に `nablarch-testing-yaml:1.0.0-SNAPSHOT`（test scope）を追加する
- [x] `pom.xml` の `<build><plugins>` に `nablarch-testing-converter:1.0.0-SNAPSHOT` をビルドプラグインとして追加する（`<configuration>` に from=xls / to=yaml / input / output / overwrite を設定。web/batch 準拠）
- [x] `unit-test.xml` に `yamlInterpreters` リストと `YamlTestDataParser` コンポーネントを追加する（隣接プロジェクトを参考）
- [x] `mvn dependency:resolve` で yaml 依存が解決できること、`mvn help:describe -Dplugin=com.nablarch.framework:nablarch-testing-converter:1.0.0-SNAPSHOT` で converter プラグインの `convert` ゴールが解決できることを確認する
- [x] 変更したファイルをコミットする
- [x] self-check (OK/NG per completion criterion, record in checks/task-2.md)
- [x] QA expert review (Agent: general-purpose / Opus 4.8)
- [x] language expert review (Agent: general-purpose / Opus 4.8)
- [x] software-engineering expert review (Agent: general-purpose / Opus 4.8)
- [x] user review（順調のため確認省略）

**Completion criteria**:

- `pom.xml` に `nablarch-testing-yaml:1.0.0-SNAPSHOT` が test スコープで追加されている
- `pom.xml` の `<build><plugins>` に `nablarch-testing-converter:1.0.0-SNAPSHOT` がビルドプラグインとして追加されている
- `unit-test.xml` に `yamlInterpreters` リストと `testDataParser` コンポーネント（`YamlTestDataParser`）が追加されている
- `mvn dependency:resolve` が成功し（yaml依存の解決エラーなし）、converter プラグインの `convert` ゴールが `mvn help:describe` で解決できる

### #3: ExcelテストデータをYAMLに変換

**Purpose**: `nablarch-testing-converter` を使って ExcelのテストデータをYAML形式に変換し、各テストのソースツリー内に配置して、変換内容をサンプリングで確認する。

**Prerequisites**: #2

**Steps**:

- [x] 対象 Excel ファイルの所在を確認する（`ProjectInsertMessageRequestTest.xlsx` 1件）
- [x] 同名の `.xls` と `.xlsx` が併存していないか確認する（併存なし。`.xlsx` のみ）
- [x] `nablarch-testing-converter` の手順に従い、全ての対象ExcelファイルをYAML変換する（`Converted 1 file(s). / BUILD SUCCESS`）
- [x] 変換後、各YAMLファイルについてExcelの内容とサンプリングで比較し、一致を確認する（全ブロック一致、差異なし）
- [x] サンプリング比較結果を `checks/task-3.md` に記録する
- [x] 変換したYAMLファイルをコミットする（Excelはまだ削除しない）
- [x] self-check (OK/NG per completion criterion, record in checks/task-3.md)
- [x] QA expert review (Agent: general-purpose / Opus 4.8)
- [x] user review（順調のため確認省略）

**Completion criteria**:

- 変換対象の全てのExcelファイルに対応するYAMLファイルが生成されている
- サンプリング比較（各ファイル最低3件、元データが3件未満の場合は元データ件数分）でExcelとYAMLの内容が一致している
- 変換後のYAMLファイルがコミットされている

### #4: Excelを削除する

**Purpose**: 変換対象だった Excel を削除してコミットする。

**Prerequisites**: #3

**Steps**:

- [x] 変換対象となった Excel ファイルを削除する
- [x] 削除結果（残存Excelが0件であること）を `checks/task-4.md` に記録する（Excelなしでの `mvn clean test` 実行とその結果の確認は Task #5 で行う）
- [x] Excelファイル削除をコミットする
- [x] self-check (OK/NG per completion criterion, record in checks/task-4.md)
- [x] QA expert review (Agent: general-purpose / Opus 4.8)
- [x] user review（順調のため確認省略）

**Completion criteria**:

- 変換対象だった全 Excel ファイルが削除されている
- 削除がコミットされている

### #5: YAMLテストデータで全テストをパスさせる

**Purpose**: Excelなしで全テストがパスすることを確認する。

**Prerequisites**: #4

**Steps**:

- [x] `mvn test` が BUILD SUCCESS になることを確認する
- [x] テストログで YamlTestDataParser が実際に使われていることを確認する
- [x] self-check (OK/NG per completion criterion, record in checks/task-5.md)
- [x] QA expert review (Agent: general-purpose / Opus 4.8)
- [x] language expert review (Agent: general-purpose / Opus 4.8) — 本タスクはコード変更なし（設定変更はTask #2で実施・レビュー済み）のため N/A
- [x] software-engineering expert review (Agent: general-purpose / Opus 4.8) — 同上 N/A
- [x] user review（順調のため確認省略）

**Completion criteria**:

- `mvn test` が BUILD SUCCESS で終了する（全テストパス、Excel ファイルなし）
- テストログで YamlTestDataParser が実際に使われていることが確認できる
</content>
</invoke>
