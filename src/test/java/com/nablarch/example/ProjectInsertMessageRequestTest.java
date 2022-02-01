package com.nablarch.example;

import nablarch.test.core.batch.BatchRequestTestSupport;
import nablarch.test.junit5.extension.batch.BatchRequestTest;
import org.junit.jupiter.api.Test;

/**
 * ユーザ削除情報メッセージ(リクエストID:ProjectInsertMessage)のテスト。
 */
@BatchRequestTest
class ProjectInsertMessageRequestTest{

    BatchRequestTestSupport support;

    @Test
    void testSendMessage() {
        support.execute(support.testName.getMethodName());
    }
}

