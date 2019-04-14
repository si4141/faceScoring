# 顔のスコア付け

## 顔画像取得スクリプトの使い方

実行の前に、Bing APIのキーを取得する必要がある。

以下のようにMicrosoftアカウントを作って取得する。

[Bingの画像検索APIを使って画像を大量に収集する](https://qiita.com/ysdyt/items/49e99416079546b65dfc)

各モジュール内でパラメータを設定した後、以下のように実行

```bash
# 画像のダウンロード
python get_picture_from_bing.py
# 顔画像の検出
python trim_face.py
```

## 開発環境

環境定義ファイルは作ってないけど、おそらく以下で動きます。
OpenCVの導入方法は覚えてないです。

- python3.7
- requests
- OpenCV (4.0.0?)

## 注意

**APIキーはgitで共有しない!!!**

間違って公開すると不正利用されてしまうので、envファイルに書いて、実行時に読み込む。

プロジェクトのディレクトリ直下にenvという名前でファイルを作って以下のようにする。

faceScoring/env
```
[BingAPI]
API_KEY = 取得したAPIキー
```
