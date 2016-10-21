--******************************************************************************
-- ユーザ削除情報メッセージ送信用のデータを取得する
--******************************************************************************
SELECT_SEND_DATA =
SELECT
  SEND_MESSAGE_SEQUENCE,
  PROJECT_NAME,
  PROJECT_TYPE,
  PROJECT_CLASS,
  TO_CHAR(PROJECT_START_DATE, 'yyyyMMdd') as PROJECT_START_DATE,
  TO_CHAR(PROJECT_END_DATE, 'yyyyMMdd') as PROJECT_END_DATE,
  CLIENT_ID,
  PROJECT_MANAGER,
  PROJECT_LEADER,
  USER_ID,
  NOTE,
  SALES,
  COST_OF_GOODS_SOLD,
  SGA,
  ALLOCATION_OF_CORP_EXPENSES,
  STATUS,
  INSERT_USER_ID,
  INSERT_DATE,
  UPDATED_USER_ID,
  UPDATED_DATE
FROM
    INS_PROJECT_SEND_MESSAGE
WHERE
    STATUS = '0'
ORDER BY
    SEND_MESSAGE_SEQUENCE

--******************************************************************************
-- ステータスを送信済みに更新する
--******************************************************************************
UPDATE_NORMAL_END =
UPDATE
    INS_PROJECT_SEND_MESSAGE
SET
    STATUS = '1',
    UPDATED_USER_ID = :updatedUserId,
    UPDATED_DATE = :updatedDate
WHERE
    SEND_MESSAGE_SEQUENCE = :sendMessageSequence

--******************************************************************************
-- ステータスをエラーに更新する
--******************************************************************************
UPDATE_ABNORMAL_END =
UPDATE
    INS_PROJECT_SEND_MESSAGE
SET
    STATUS = '9',
    UPDATED_USER_ID = :updatedUserId,
    UPDATED_DATE = :updatedDate
WHERE
    SEND_MESSAGE_SEQUENCE = :sendMessageSequence