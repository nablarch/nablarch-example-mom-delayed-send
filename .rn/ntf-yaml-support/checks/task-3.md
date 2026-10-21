# task-3 Completion Check

## Completion Criteria

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| 変換対象の全 Excel に対応する YAML が生成されている | OK | 対象 Excel は `src/test/java/com/nablarch/example/ProjectInsertMessageRequestTest.xlsx` の1ファイル（シート `setUpDb` / `testSendMessage`）。`mvn com.nablarch.framework:nablarch-testing-converter:1.0.0-SNAPSHOT:convert`（pom の `<configuration>` を使用）で `Converted 1 file(s).` / BUILD SUCCESS。`ProjectInsertMessageRequestTest/setUpDb.yaml`（0 バイト）と `ProjectInsertMessageRequestTest/testSendMessage.yaml` を生成。シート数とYAML数が一致 | - | - |
| サンプリング比較で Excel と YAML の内容が一致している | OK | `scripts/compare_samples.py` で `testSendMessage.yaml` 9件（testShots / SETUP_TABLE / EXPECTED_REQUEST_HEADER_MESSAGES / EXPECTED_REQUEST_BODY_MESSAGES / EXPECTED_TABLE の各ブロックから抽出）と、データなしシート `setUpDb` の空 YAML を照合し全一致（rc=0）。下記 Sampling Comparison 参照 | - | - |
| 変換後の YAML がコミットされている | OK | YAML 2ファイルと `scripts/`（`dump_xlsx.py` / `compare_samples.py`）を Task #3 コミットに含めた。Excel は未削除（Task #4 で削除） | - | - |

## Sampling Comparison（task-3 のみ）
| YAML ファイル | 比較件数 | レコードキー/行 | Excel 値 | YAML 値 | 一致 |
| --- | --- | --- | --- | --- | --- |
| src/test/java/com/nablarch/example/ProjectInsertMessageRequestTest/testSendMessage.yaml | 9 | testShots no=1 / diConfig (testSendMessage!G4) | 'messaging-async-send-boot.xml' | 'messaging-async-send-boot.xml' | OK |
| src/test/java/com/nablarch/example/ProjectInsertMessageRequestTest/testSendMessage.yaml | 9 | testShots no=1 / description（改行含む） (testSendMessage!B4) | '正常系ケース\n\n電文が想定通り送信され、テーブルの処理ステータスが送信済みに更新されること。' | '正常系ケース\n\n電文が想定通り送信され、テーブルの処理ステータスが送信済みに更新されること。' | OK |
| src/test/java/com/nablarch/example/ProjectInsertMessageRequestTest/testSendMessage.yaml | 9 | SETUP_TABLE[1] SEND_MESSAGE_SEQUENCE (testSendMessage!A14) | '0000010001' | '0000010001' | OK |
| src/test/java/com/nablarch/example/ProjectInsertMessageRequestTest/testSendMessage.yaml | 9 | SETUP_TABLE[1] PROJECT_START_DATE (testSendMessage!E14) | '2010-9-18 00:00:00.0' | '2010-9-18 00:00:00.0' | OK |
| src/test/java/com/nablarch/example/ProjectInsertMessageRequestTest/testSendMessage.yaml | 9 | EXPECTED_REQUEST_HEADER_MESSAGES[1] 電文連番 (testSendMessage!C24) | '0000010001' | '0000010001' | OK |
| src/test/java/com/nablarch/example/ProjectInsertMessageRequestTest/testSendMessage.yaml | 9 | EXPECTED_REQUEST_BODY_MESSAGES[1] プロジェクト名 (testSendMessage!B32) | 'プロジェクト００１' | 'プロジェクト００１' | OK |
| src/test/java/com/nablarch/example/ProjectInsertMessageRequestTest/testSendMessage.yaml | 9 | EXPECTED_REQUEST_BODY_MESSAGES[1] 備考 length (testSendMessage!K31) | '1024' | '1024' | OK |
| src/test/java/com/nablarch/example/ProjectInsertMessageRequestTest/testSendMessage.yaml | 9 | EXPECTED_TABLE[1] STATUS (testSendMessage!P39) | '1' | '1' | OK |
| src/test/java/com/nablarch/example/ProjectInsertMessageRequestTest/testSendMessage.yaml | 9 | EXPECTED_TABLE[1] UPDATED_DATE (testSendMessage!T39) | '2014-09-13 12:34:56.0' | '2014-09-13 12:34:56.0' | OK |
| src/test/java/com/nablarch/example/ProjectInsertMessageRequestTest/setUpDb.yaml | 0（元データ0件のため全件=0件。空ファイルであることを確認） | （元シートにデータなし） | （空） | （空） | OK |

- 比較方法: `python3 -I .rn/ntf-yaml-support/scripts/compare_samples.py <xlsx> <yaml-dir>`（Excel のセル値と YAML の値を文字列で完全一致比較）。`dump_xlsx.py` で Excel 全セルをダンプし、目視でも YAML 全体と照合した。
- 補足: YAML の電文ブロックの `directives` に Excel に無い `file-type: "Fixed"` が出力される。converter が NTF の読み取り処理（`FixedLengthFile`）を通して電文を読むため付く暗黙の属性で、Excel 由来のデータ値の差異ではない（`text-encoding: "MS932"` は Excel と一致）。
- 参考: 生成 YAML は、旧移行コミット `6932e57` 時点の `testSendMessage.yaml` と `diff` で完全一致。

## .xls/.xlsx 併存チェック（該当時のみ）
- 併存の有無: なし（`find` で `.xls` 0件、`.xlsx` 1件のみ）
- 差分確認結果の保存先: 該当なし
- 未使用側（通常 `.xlsx`）の削除: 該当なし

## QA Expert Review

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Meaningful tests/verification | - | - |
| Edge case coverage | - | - |

## Expert Reviews (code changes only)

N/A — no code changes in this task.

## Overall Verdict

- Self-check: OK
- QA: -
- Language expert: N/A
- Software-engineering expert: N/A
- Ready for user review: -
