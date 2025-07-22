"""
料理の献立管理アプリケーション

BeeWare (Toga) を使用したiOS向け献立管理アプリケーション
"""

import sys
import threading
import time
import traceback

import toga

from meals.utils.database import backup_database, init_db, restore_database
from meals.utils.exceptions import DatabaseException, MealPlannerException, RecoveryException
from meals.utils.logger import logger
from meals.utils.performance import measure_execution_time
from meals.utils.ui import run_in_background, show_loading, hide_loading
from meals.views.main_window import MainView


class MealPlannerApp(toga.App):
    """
    献立管理アプリケーションのメインクラス
    """
    
    @measure_execution_time
    def startup(self):
        """
        アプリケーションの起動時に呼び出される
        タブベースのインターフェースを構築する
        """
        # メインウィンドウの設定
        self.main_window = toga.MainWindow(title=self.formal_name)
        
        # スプラッシュスクリーンを表示
        splash_box = toga.Box(style=toga.style.Pack(
            direction="column",
            alignment="center",
            flex=1,
            background_color=(1, 1, 1, 1),
        ))
        
        # アプリ名ラベル
        app_name_label = toga.Label(
            "献立管理",
            style=toga.style.Pack(
                text_align="center",
                font_size=24,
                font_weight="bold",
                padding=(20, 5),
            )
        )
        
        # ローディングインジケーター
        activity_indicator = toga.ActivityIndicator(style=toga.style.Pack(padding=10))
        activity_indicator.start()
        
        # ローディングメッセージ
        loading_label = toga.Label(
            "読み込み中...",
            style=toga.style.Pack(text_align="center", padding=10)
        )
        
        # スプラッシュスクリーンにコンポーネントを追加
        splash_box.add(app_name_label)
        splash_box.add(activity_indicator)
        splash_box.add(loading_label)
        
        # スプラッシュスクリーンを表示
        self.main_window.content = splash_box
        self.main_window.show()
        
        # 非同期で初期化処理を実行
        self._async_initialize()
    
    @run_in_background
    def _async_initialize(self):
        """
        非同期でアプリケーションを初期化する
        """
        try:
            logger.info("Starting application")
            
            # データベースの初期化
            self._initialize_app()
            
            # UIスレッドでメインビューを作成
            self.add_background_task(self._create_main_view)
            
            logger.info("Application started successfully")
        except (MealPlannerException, DatabaseException) as e:
            logger.error(f"Initialization error: {str(e)}")
            self.add_background_task(lambda: self._handle_initialization_error(e))
        except Exception as e:
            logger.critical(f"Unexpected error: {str(e)}")
            logger.critical(traceback.format_exc())
            self.add_background_task(lambda: self.main_window.info_dialog(
                "重大なエラー",
                f"予期しないエラーが発生しました: {str(e)}\n\n"
                "アプリケーションを再起動してください。"
            ))
    
    def _create_main_view(self):
        """
        メインビューを作成する
        """
        # メインビューの作成
        self.main_view = MainView(self)
    
    def _initialize_app(self):
        """
        アプリケーションの初期化処理
        データベースの接続やモデルの初期化などを行う
        """
        # データベースの初期化
        init_db()
    
    def _handle_initialization_error(self, error):
        """
        初期化エラーを処理する
        """
        # データベースのバックアップを作成
        backup_path = backup_database()
        
        if isinstance(error, DatabaseException):
            # データベースエラーの場合、復旧を試みる
            if self.main_window.question_dialog(
                "データベースエラー",
                f"データベースの初期化中にエラーが発生しました: {str(error)}\n\n"
                "データベースを再作成しますか？"
            ):
                try:
                    # データベースを再作成
                    logger.info("Attempting to recreate database")
                    init_db(max_retries=5)
                    
                    # メインビューの作成
                    self.main_view = MainView(self)
                    
                    self.main_window.info_dialog(
                        "復旧成功",
                        "データベースの再作成に成功しました。"
                    )
                    logger.info("Database recovery successful")
                    return
                except Exception as e:
                    logger.error(f"Database recovery failed: {str(e)}")
                    if backup_path:
                        # バックアップからの復元を試みる
                        if self.main_window.question_dialog(
                            "復旧失敗",
                            f"データベースの再作成に失敗しました: {str(e)}\n\n"
                            "バックアップから復元しますか？"
                        ):
                            try:
                                if restore_database(backup_path):
                                    # 復元成功
                                    self.main_window.info_dialog(
                                        "復元成功",
                                        "バックアップからの復元に成功しました。"
                                    )
                                    
                                    # 再初期化
                                    init_db()
                                    
                                    # メインビューの作成
                                    self.main_view = MainView(self)
                                    
                                    logger.info("Database restore successful")
                                    return
                                else:
                                    raise RecoveryException("バックアップからの復元に失敗しました。")
                            except Exception as e:
                                logger.error(f"Database restore failed: {str(e)}")
                                self.main_window.info_dialog(
                                    "復元失敗",
                                    f"バックアップからの復元に失敗しました: {str(e)}\n\n"
                                    "アプリケーションを終了します。"
                                )
                                sys.exit(1)
        
        # その他のエラーまたは復旧を試みない場合
        self.main_window.info_dialog(
            "初期化エラー",
            f"アプリケーションの初期化中にエラーが発生しました: {str(error)}\n\n"
            "アプリケーションを再起動してください。"
        )


def main():
    """
    アプリケーションのエントリーポイント
    """
    return MealPlannerApp("献立管理", "com.example.meals")