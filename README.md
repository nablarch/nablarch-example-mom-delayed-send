nablarch-example-mom-delayed-send
====================================
Nablarch FrameworkのMOM応答不要メッセージングの送信側のExampleで、テーブルをキューとして使ったメッセージングを用いて構築しています。
MOM応答不要メッセージングの受信側のExampleと組み合わせて使用します。

以下にメッセージングのシステムのうち、本Exampleが対象とする箇所を示します。

![概要](./fig/abstract.png "概要")

※図中の「オンライン処理アプリケーション等」と「バッチアプリケーション」の部分はExampleの提供はありません。

## 実行手順

### 1.動作環境
実行環境に以下のソフトウェアがインストールされている事を前提とします。
* Java Version : 8
* Maven 3.0.5以降

補足：
MOMは、MOM応答不要メッセージングの受信側のExampleに組み込まれたものを使用します。
RDBMSは、本Exampleに組み込まれたものを使用します。

### 2. プロジェクトリポジトリの取得
Gitを使用している場合、アプリケーションを配置したいディレクトリにて「git clone」コマンドを実行してください。
以下、コマンドの例です。

    $mkdir c:\example
    $cd c:\example
    $git clone https://github.com/nablarch/nablarch-example-mom-delayed-send.git

Gitを使用しない場合、最新のタグからzipをダウンロードし、任意のディレクトリへ展開してください。

### 3. アプリケーションのビルド
#### 3.1. データベースのセットアップ及びエンティティクラスの作成
まず、データベースのセットアップ及びエンティティクラスの作成を行います。以下のコマンドを実行してください。

    $cd nablarch-example-mom-delayed-send
    $mvn -P gsp clean generate-resources
    $mvn -P gsp install:install-file

#### 3.2. アプリケーションのビルド
次に、アプリケーションをビルドします。以下のコマンドを実行してください。

    $mvn clean package

### 4. アプリケーションの起動

先にMOM応答不要メッセージングの受信側のExampleを起動しておいてください。

以下のコマンドで、MOM応答不要メッセージングの送信側のExampleが起動します。

    $mvn -P gsp gsp-dba:import-schema
    $mvn exec:java -Dexec.mainClass=nablarch.fw.launcher.Main -Dexec.args="'-diConfig' 'messaging-async-send-boot.xml' '-requestPath' 'SENDAPP' '-userId' 'batch_user' '-messageRequestId' 'ProjectInsertMessage'"

なお、 `maven-assembly-plugin` を使用して実行可能jarの生成を行っているため、以下のコマンドでもアプリケーションを実行することが可能です。

    $java -jar target/application-5u9.jar -diConfig classpath:messaging-async-send-boot.xml -requestPath SENDAPP -userId batch_user -messageRequestId ProjectInsertMessage

起動に成功すると以下のようなログがコンソールに出力され、メッセージが送信されます。

    2016-06-09 09:58:41.874 -INFO- ROO [null] @@@@ APPLICATION SETTINGS @@@@
            system settings = {
            }
            business date = [20140123]
    2016-06-09 09:58:42.264 -INFO- ROO [201606090958418740001] read database record. key info: {SEND_MESSAGE_SEQUENCE=0000000001}
    2016-06-09 09:58:42.358 -INFO- ROO [201606090958422640002] @@@@ SENT MESSAGE @@@@
            thread_name    = [pool-1-thread-1]
            message_id     = [ID:S1306C00419-T1-20683-1465433922061-1:1:1:1:1]
            destination    = [TEST.REQUEST]
            correlation_id = [null]
            reply_to       = [null]
            time_to_live   = [0]
            message_body   = [ProjectInsertMessage0000000001100                 プロジェクト００１
                                                                                                    development
                                                                                                                        s
                                                                                                                                            20100918201504091        鈴木
                                                                                                                                                                                         佐藤
                                                                                                                                                                                                             100      備考欄




                                                          10000    1000     2000     3000           ]


自動的に終了はしないため、ctrl + c等で終了させてください。

### 5. DBの確認方法

1. http://www.h2database.com/html/cheatSheet.html からH2をインストールしてください。

2. {インストールフォルダ}/bin/h2.bat を実行してください(コマンドプロンプトが開く)。  
  ※h2.bat実行中はExampleアプリケーションからDBへアクセスすることができないため、Exampleアプリケーションを停止しておいてください。

3. ブラウザから http://localhost:8082 を開き、以下の情報でH2コンソールにログインしてください。
   JDBC URLの{dbファイルのパス}には、`SAMPLE.h2.db`ファイルの格納ディレクトリまでのパスを指定してください。  
  JDBC URL：jdbc:h2:{dbファイルのパス}/SAMPLE  
  ユーザ名：SAMPLE  
  パスワード：SAMPLE
