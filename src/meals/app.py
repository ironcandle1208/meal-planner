"""
料理の献立管理アプリケーション

BeeWare (Toga) を使用したiOS向け献立管理アプリケーション
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from meals.utils.exceptions import DatabaseException, MealPlannerException


class MealPlannerApp(toga.App):
    """
    献立管理アプリケーションのメインクラス
    """
    
    def startup(self):
        """
        アプリケーションの起動時に呼び出される
        タブベースのインターフェースを構築する
        """
        # メインコンテナ
        main_box = toga.Box(style=Pack(direction=COLUMN))
        
        # タブコンテナの作成
        self.tabs = toga.OptionContainer(style=Pack(flex=1))
        
        # 献立タブ
        meal_plans_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        meal_plans_label = toga.Label("献立管理", style=Pack(padding=5))
        meal_plans_box.add(meal_plans_label)
        
        # レシピタブ
        recipes_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        recipes_label = toga.Label("レシピ管理", style=Pack(padding=5))
        recipes_box.add(recipes_label)
        
        # 買い物リストタブ
        shopping_list_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        shopping_list_label = toga.Label("買い物リスト", style=Pack(padding=5))
        shopping_list_box.add(shopping_list_label)
        
        # タブの追加
        self.tabs.add("献立", meal_plans_box)
        self.tabs.add("レシピ", recipes_box)
        self.tabs.add("買い物リスト", shopping_list_box)
        
        # メインボックスにタブを追加
        main_box.add(self.tabs)
        
        # メインウィンドウの設定
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()
        
        # データベースの初期化などの処理をここで行う
        try:
            self._initialize_app()
        except (MealPlannerException, DatabaseException) as e:
            self.main_window.info_dialog(
                "初期化エラー",
                f"アプリケーションの初期化中にエラーが発生しました: {str(e)}"
            )
    
    def _initialize_app(self):
        """
        アプリケーションの初期化処理
        データベースの接続やモデルの初期化などを行う
        """
        from meals.utils.database import init_db
        
        # データベースの初期化
        init_db()


def main():
    """
    アプリケーションのエントリーポイント
    """
    return MealPlannerApp("献立管理", "com.example.meals")