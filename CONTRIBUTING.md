# 献立管理アプリ開発への貢献

このプロジェクトへの貢献に興味をお持ちいただき、ありがとうございます。このドキュメントでは、開発環境のセットアップ方法や貢献のガイドラインについて説明します。

## 開発環境のセットアップ

1. リポジトリをクローンします：
   ```
   git clone https://github.com/yourusername/meal-planner.git
   cd meal-planner
   ```

2. Python 3.8以上をインストールします。

3. 仮想環境を作成し、有効化します：
   ```
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate  # Windows
   ```

4. 依存関係をインストールします：
   ```
   pip install -e .
   ```

5. 開発モードで実行します：
   ```
   briefcase dev
   ```

## テストの実行

テストを実行するには：

```
python -m pytest
```

## コーディング規約

- PEP 8に従ってください。
- コードにはドキュメンテーション文字列を追加してください。
- 新しい機能には必ずテストを追加してください。

## プルリクエストのプロセス

1. 新しいブランチを作成します：
   ```
   git checkout -b feature/your-feature-name
   ```

2. 変更をコミットします：
   ```
   git commit -m "Add your feature description"
   ```

3. リモートにプッシュします：
   ```
   git push origin feature/your-feature-name
   ```

4. プルリクエストを作成します。

## ビルドとパッケージング

iOSアプリをビルドするには：

```
briefcase build iOS
briefcase run iOS
```

## ライセンス

このプロジェクトはBSD 3-Clauseライセンスの下で公開されています。詳細はLICENSEファイルを参照してください。