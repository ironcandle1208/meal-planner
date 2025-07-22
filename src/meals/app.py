"""
料理の献立管理アプリケーション

BeeWare (Toga) を使用したiOS向け献立管理アプリケーション
"""

import toga

from meals.utils.exceptions import DatabaseException, MealPlannerException
from meals.views.main_window import MainView


class MealPlannerApp(toga.App):
    """
    献立管理アプリケーションのメインクラス
    """
    
    def startup(self):
        """
        アプリケーションの起動時に呼び出される
        タブベースのインターフェースを構築する
        """
        # メインウィンドウの設定
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.show()
        
        # データベースの初期化などの処理をここで行う
        try:
            self._initialize_app()
            
            # メインビューの作成
            self.main_view = MainView(self)
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