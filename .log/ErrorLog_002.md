# エラーログ - ErrorLog_001.md

## 発生日時
2025年7月22日 (火)

## エラー概要
`meals/src/meals/viewmodels/__init__.py`ファイルでのインポートエラー。相対インポートではなく絶対インポートが使用されているため、モジュールが正しく解決されない問題が発生しています。

## 原因分析
現在の`__init__.py`ファイルでは、以下のようなインポート文が使用されています：

```python
from meals.viewmodels.base import BaseViewModel
from meals.viewmodels.meal_plan import MealPlanViewModel
from meals.viewmodels.recipe import RecipeViewModel
from meals.viewmodels.shopping_list import ShoppingListViewModel
```

これらは絶対インポートパスを使用していますが、同じパッケージ内のモジュールをインポートする場合は相対インポートを使用するべきです。Pythonのパッケージ構造では、同じパッケージ内のモジュールをインポートする場合、相対インポートを使用することが推奨されています。

## 修正箇所
`meals/src/meals/viewmodels/__init__.py`ファイル内のインポート文

## 修正内容
絶対インポートから相対インポートに変更します：

```python
from .base import BaseViewModel
from .meal_plan import MealPlanViewModel
from .recipe import RecipeViewModel
from .shopping_list import ShoppingListViewModel
```

## 影響範囲
このエラーにより、`meals/src/meals/viewmodels`パッケージからのインポートが失敗し、アプリケーション全体でViewModelクラスが利用できなくなる可能性があります。修正により、正しくモジュールがインポートされるようになります。

## 予防策
1. パッケージ内のモジュールをインポートする際は、相対インポートを使用する
2. インポート文を追加する前に、プロジェクト内の既存のインポートパターンを確認する
3. 新しいモジュールを作成する際は、インポートの一貫性を保つためのガイドラインを設ける