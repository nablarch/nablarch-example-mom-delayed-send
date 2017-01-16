package com.nablarch.example.form;

import java.sql.Timestamp;
import java.util.Map;

import nablarch.core.db.statement.autoproperty.CurrentDateTime;
import nablarch.core.db.statement.autoproperty.UserId;

/**
 * 送信メッセージフォーム。
 *
 * @author Nabu Rakutaro
 */
public class SendMessagingForm {

    /** 送信電文連番 */
    private final String sendMessageSequence;

    /** 更新ユーザID */
    @UserId
    private final String updatedUserId;

    /** 更新日時 */
    @CurrentDateTime
    private final Timestamp updatedDate;

    /**
     * デフォルトコンストラクタ。
     * @param data 初期化に使用するパラメータ
     */
    public SendMessagingForm(Map<String, ?> data) {
       sendMessageSequence = (String) data.get("sendMessageSequence");
       updatedUserId = (String) data.get("updatedUserId");
       updatedDate = (Timestamp) data.get("updatedDate");
    }

    /**
     * 送信電文連番を取得する。
     * @return 送信電文連番
     */
    public String getSendMessageSequence() {
        return sendMessageSequence;
    }

    /**
     * 更新ユーザIDを取得する。
     * @return 更新ユーザID
     */
    public String getUpdatedUserId() {
        return updatedUserId;
    }

    /**
     * 更新日時を取得する。
     * @return 更新日時
     */
    public Timestamp getUpdatedDate() {
        return updatedDate;
    }
}
