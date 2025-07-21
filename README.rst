献立管理アプリケーション
====================

料理の献立を効率的に管理・保存できるiOSアプリケーションです。ユーザーが日々の食事計画を立て、レシピや食材情報を整理し、栄養バランスを考慮した献立作成をサポートします。

機能
----

* 献立の作成・保存
* レシピの追加と管理
* レシピと献立の関連付け
* 買い物リストの生成
* レシピと献立の検索・フィルタリング
* オフライン使用

開発環境のセットアップ
--------------------

1. Python 3.8以上をインストール
2. 仮想環境を作成: ``python -m venv venv``
3. 仮想環境を有効化:
   * Windows: ``venv\Scripts\activate``
   * macOS/Linux: ``source venv/bin/activate``
4. 依存関係をインストール: ``pip install -e .``
5. 開発モードで実行: ``briefcase dev``

ビルド方法
--------

iOS向けにビルド:

.. code-block:: bash

    briefcase build iOS
    briefcase run iOS

ライセンス
--------

BSD 3-Clause License