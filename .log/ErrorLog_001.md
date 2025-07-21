# エラーログ - ErrorLog_001.md

## 発生日時
2025/7/21 (月)

## エラー概要
`meals/src/meals/repositories/__init__.py` ファイルでインポートパスが間違っています。モジュールパスが `meals.repositories` ではなく `meals.src.meals.repositories` を参照しています。

## 原因分析
リポジトリモジュールのインポート文で、正しいパスが使用されていません。現在のインポート文は:

```python
from meals.repositories.base import BaseRepository
from meals.repositories.meal_plan import MealPlanRepository
from meals.repositories.recipe import RecipeRepository
from meals.repositories.shopping_list import ShoppingListRepository
```

しかし、プロジェクト構造から見ると、正しいインポートパスは:

```python
from meals.src.meals.repositories.base import BaseRepository
from meals.src.meals.repositories.meal_plan import MealPlanRepository
from meals.src.meals.repositories.recipe import RecipeRepository
from meals.src.meals.repositories.shopping_list import ShoppingListRepository
```

または、相対インポートを使用する場合:

```python
from .base import BaseRepository
from .meal_plan import MealPlanRepository
from .recipe import RecipeRepository
from .shopping_list import ShoppingListRepository
```

## 修正箇所
`meals/src/meals/repositories/__init__.py` ファイル内のインポート文

## 修正内容
相対インポートを使用して修正します:

```python
"""
Repositories package for the meal planner application.
"""

from .base import BaseRepository
from .meal_plan import MealPlanRepository
from .recipe import RecipeRepository
from .shopping_list import ShoppingListRepository

__all__ = [
    "BaseRepository",
    "MealPlanRepository",
    "RecipeRepository",
    "ShoppingListRepository",
]
```

## 影響範囲
このエラーにより、アプリケーションが起動時にインポートエラーを引き起こす可能性があります。リポジトリモジュールを使用するすべてのコードに影響します。

## 予防策
1. パッケージ内のモジュールをインポートする場合は、相対インポートを使用する（`.module` または `..module`）
2. プロジェクト構造に合わせたインポートパスを使用する
3. インポートをテストするユニットテストを作成する
4. 新しいモジュールを追加する際は、既存のインポートパターンに従う