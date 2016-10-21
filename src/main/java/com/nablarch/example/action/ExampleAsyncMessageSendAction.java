package com.nablarch.example.action;

import nablarch.core.db.statement.SqlRow;
import nablarch.fw.DataReader;
import nablarch.fw.ExecutionContext;
import nablarch.fw.messaging.action.AsyncMessageSendAction;
import nablarch.fw.reader.DatabaseRecordReader;
import nablarch.fw.reader.DatabaseTableQueueReader;

/**
 * 応答不要メッセージング送信を行う業務アクションクラス。
 *
 * @author Nabu Rakutaro
 */
public class ExampleAsyncMessageSendAction extends AsyncMessageSendAction {
    @Override
    public DataReader<SqlRow> createReader(ExecutionContext ctx) {
        DatabaseRecordReader reader = new DatabaseRecordReader();
        reader.setStatement(createStatement());
        return new DatabaseTableQueueReader(reader, 5000, "SEND_MESSAGE_SEQUENCE");
    }
}
