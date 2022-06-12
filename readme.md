# 数独をプログラムで解く

数独の解き方について、自身が考えた考え方ですべての問題を解くことができるかを試したくて作成しました。

解く方法としては、自分が実際に解くときに行っている数字候補の絞り方を使用して解きます。

※このツールでは、自分自身で各セルの値を設定したり、各セルの候補の数字を自分自身で絞ったりすることはできません。

## 使用方法

1. ソースをダウンロードします。
1. pythonの仮想環境を作成します。(推奨)(Windows Command Promptの例)
    ~~~
    > python -m venv venv
    > venv\Scripts\activate
    (venv)> python -m pip --upgrade pip
    ~~~
1. 必要なライブラリを設定します。
    ~~~
    (venv)> pip install -r requirements.txt
    ~~~
1. 解きたい問題をmain.pyのmain関数のbase_data変数に設定します。
    ~~~python
    # 各列を数字のみの文字列で設定します。
    # 空白は0として設定します。
    base_data = [
        '001040009',
        '000000507',
        '009086000',
        '708000000',
        '000007930',
        '900060720',
        '204000801',
        '010000005',
        '007001402',
    ]
    ~~~
1. プログラムを起動します。
    ~~~
    (venv)> python main.py
    ~~~
1. GUIが起動するので、GUI上のボタンを操作して問題を解きます。

## 解法としているロジックについて

大きく分けて2つの行程で解いていきます。

1. 候補を絞る
    1. 3 x 3の正方形領域で数値が設定されているセルの値を候補から除く
    1. 横一列の領域で数値が設定されているセルの値を候補から除く
    1. 縦一列の領域で数値が設定されているセルの値を候補から除く
1. 絞られた候補から値を選択する
    1. 候補が一つになっているセルの値を設定する
    1. 3 x 3の正方形領域ですでに設定されているセルの値とかぶらず、領域内でそのセルだけに存在する数値候補があった場合にその値を設定する。
    1. 横一列の領域ですでに設定されているセルの値とかぶらず、領域内でそのセルだけに存在する数値候補があった場合にその値を設定する。
    1. 縦一列の領域ですでに設定されているセルの値とかぶらず、領域内でそのセルだけに存在する数値候補があった場合にその値を設定する。

## 今後おこないたいこと

空いている時間があればやりたい修正

- TODO: ソースのリファクタリング
- TODO: テストコードの作成
- TODO: UIで3 x 3ごとに処理していて重いため、一つのパネル上に載せるよう修正
- TODO: 自身の考えでは3個ずつの塊が大切になるロジックがある想定で作成していたが、必要なさそうなので、各グループを行列からリストのデータとして扱うよう修正
- TODO: 各セルの値の設定、候補の個別設定を行える用修正(自分自身の力で解けるモード)
- TODO: ボタン操作等の履歴を管理して前の状態に戻すことができる。
- TODO: 操作を行ったときに、どこが変更したかのログを表示する
- TODO: データの設定をソース上ではなく、アプリ上え行うことができるようにする
- TODO: 画像を取り込んで初期設定を行えるようにする(DeepLearningを使ってみたい)