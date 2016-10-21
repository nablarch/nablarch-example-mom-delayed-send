package com.nablarch.example;

import org.junit.Test;

import com.nablarch.example.test.BatchRequestTestBase;

/**
 * ユーザ削除情報メッセージ(リクエストID:ProjectInsertMessage)のテスト。
 */
public class ProjectInsertMessageRequestTest extends BatchRequestTestBase {

    @Test
    public void testSendMessage() {
        execute();
    }
}

