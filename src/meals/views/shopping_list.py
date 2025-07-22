"""
ShoppingList view for the meal planner application.
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from meals.viewmodels.shopping_list import ShoppingListViewModel


class ShoppingListView:
    """ShoppingList view for the meal planner application."""
    
    def __init__(self, app):
        """Initialize the shopping list view."""
        self.app = app
        self.content = None
        self.shopping_list_vm = ShoppingListViewModel()
        
        # UI components
        self.shopping_lists_list = None
        self.shopping_list_details = None
        self.name_input = None
        self.start_date_input = None
        self.end_date_input = None
        self.items_table = None
        
        # Create the view
        self._create_view()
        
        # Register event handlers
        self._register_handlers()
        
        # Load initial data
        self._load_data()
    
    def _create_view(self):
        """Create the view."""
        # Main container
        self.content = toga.Box(style=Pack(direction=COLUMN, padding=10))
        
        # Title
        title_label = toga.Label(
            "買い物リスト管理",
            style=Pack(padding=(0, 0, 10, 0), font_size=18, font_weight="bold")
        )
        self.content.add(title_label)
        
        # Split view for list and details
        split_container = toga.SplitContainer(style=Pack(flex=1))
        
        # Shopping lists list
        list_container = toga.Box(style=Pack(direction=COLUMN, padding=5))
        list_label = toga.Label("買い物リスト一覧", style=Pack(padding=(0, 0, 5, 0), font_weight="bold"))
        self.shopping_lists_list = toga.Table(
            headings=["名前", "開始日", "終了日"],
            style=Pack(flex=1),
        )
        
        # Buttons for list actions
        list_actions = toga.Box(style=Pack(direction=ROW, padding=5))
        add_button = toga.Button("追加")
        add_button.on_press = self.on_add_shopping_list
        generate_button = toga.Button("献立から生成")
        generate_button.on_press = self.on_generate_from_meal_plans
        delete_button = toga.Button("削除")
        delete_button.on_press = self.on_delete_shopping_list
        
        list_actions.add(add_button)
        list_actions.add(generate_button)
        list_actions.add(delete_button)
        
        list_container.add(list_label)
        list_container.add(self.shopping_lists_list)
        list_container.add(list_actions)
        
        # Shopping list details
        details_container = toga.ScrollContainer(style=Pack(flex=1))
        details_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
        details_label = toga.Label("買い物リスト詳細", style=Pack(padding=(0, 0, 5, 0), font_weight="bold"))
        
        # Form for shopping list details
        form_container = toga.Box(style=Pack(direction=COLUMN, padding=5))
        
        # Name input
        name_box = toga.Box(style=Pack(direction=ROW, padding=2))
        name_label = toga.Label("名前:", style=Pack(width=100, padding=(0, 5, 0, 0)))
        self.name_input = toga.TextInput(style=Pack(flex=1))
        name_box.add(name_label)
        name_box.add(self.name_input)
        
        # Date range inputs
        date_range_box = toga.Box(style=Pack(direction=COLUMN, padding=2))
        
        start_date_box = toga.Box(style=Pack(direction=ROW, padding=2))
        start_date_label = toga.Label("開始日:", style=Pack(width=100, padding=(0, 5, 0, 0)))
        self.start_date_input = toga.DateInput(style=Pack(flex=1))
        start_date_box.add(start_date_label)
        start_date_box.add(self.start_date_input)
        
        end_date_box = toga.Box(style=Pack(direction=ROW, padding=2))
        end_date_label = toga.Label("終了日:", style=Pack(width=100, padding=(0, 5, 0, 0)))
        self.end_date_input = toga.DateInput(style=Pack(flex=1))
        end_date_box.add(end_date_label)
        end_date_box.add(self.end_date_input)
        
        date_range_box.add(start_date_box)
        date_range_box.add(end_date_box)
        
        # Items table
        items_box = toga.Box(style=Pack(direction=COLUMN, padding=2))
        items_label = toga.Label("アイテム:", style=Pack(padding=(0, 0, 5, 0)))
        self.items_table = toga.Table(
            headings=["材料名", "分量", "単位", "カテゴリ", "購入済み"],
            style=Pack(flex=1, height=200),
        )
        
        # Filter options
        filter_box = toga.Box(style=Pack(direction=ROW, padding=2))
        filter_label = toga.Label("フィルタ:", style=Pack(width=100, padding=(0, 5, 0, 0)))
        filter_selection = toga.Selection(
            items=["全て", "未購入のみ", "購入済みのみ"],
            style=Pack(flex=1),
        )
        filter_selection.on_select = self.on_filter_changed
        filter_box.add(filter_label)
        filter_box.add(filter_selection)
        
        # Category filter
        category_box = toga.Box(style=Pack(direction=ROW, padding=2))
        category_label = toga.Label("カテゴリ:", style=Pack(width=100, padding=(0, 5, 0, 0)))
        category_selection = toga.Selection(
            items=["全て", "野菜", "肉", "魚", "乳製品", "穀物", "果物", "調味料", "その他"],
            style=Pack(flex=1),
        )
        category_selection.on_select = self.on_category_changed
        category_box.add(category_label)
        category_box.add(category_selection)
        
        # Buttons for items actions
        items_actions = toga.Box(style=Pack(direction=ROW, padding=2))
        add_item_button = toga.Button("アイテムを追加")
        add_item_button.on_press = self.on_add_item
        edit_item_button = toga.Button("アイテムを編集")
        edit_item_button.on_press = self.on_edit_item
        remove_item_button = toga.Button("アイテムを削除")
        remove_item_button.on_press = self.on_remove_item
        mark_purchased_button = toga.Button("購入済みにする")
        mark_purchased_button.on_press = self.on_mark_purchased
        
        items_actions.add(add_item_button)
        items_actions.add(edit_item_button)
        items_actions.add(remove_item_button)
        items_actions.add(mark_purchased_button)
        
        items_box.add(items_label)
        items_box.add(filter_box)
        items_box.add(category_box)
        items_box.add(self.items_table)
        items_box.add(items_actions)
        
        # Add form elements
        form_container.add(name_box)
        form_container.add(date_range_box)
        form_container.add(items_box)
        
        # Buttons for details actions
        details_actions = toga.Box(style=Pack(direction=ROW, padding=5))
        save_button = toga.Button("保存")
        save_button.on_press = self.on_save_shopping_list
        cancel_button = toga.Button("キャンセル")
        cancel_button.on_press = self.on_cancel_edit
        
        details_actions.add(save_button)
        details_actions.add(cancel_button)
        
        details_box.add(details_label)
        details_box.add(form_container)
        details_box.add(details_actions)
        
        # Add details box to scroll container
        details_container.content = details_box
        
        # Add containers to split view
        split_container.content = [list_container, details_container]
        
        # Add split view to main container
        self.content.add(split_container)
    
    def _register_handlers(self):
        """Register event handlers."""
        # Register handlers for shopping list view model
        self.shopping_list_vm.register_error_handler("create_shopping_list", self._on_shopping_list_error)
        self.shopping_list_vm.register_error_handler("update_shopping_list", self._on_shopping_list_error)
        self.shopping_list_vm.register_error_handler("delete_shopping_list", self._on_shopping_list_error)
        self.shopping_list_vm.register_error_handler(
            "generate_shopping_list_from_meal_plans", self._on_shopping_list_error
        )
        
        self.shopping_list_vm.register_success_handler("create_shopping_list", self._on_shopping_list_success)
        self.shopping_list_vm.register_success_handler("update_shopping_list", self._on_shopping_list_success)
        self.shopping_list_vm.register_success_handler("delete_shopping_list", self._on_shopping_list_deleted)
        self.shopping_list_vm.register_success_handler(
            "generate_shopping_list_from_meal_plans", self._on_shopping_list_success
        )
        
        # Set up table selection handler
        self.shopping_lists_list.on_select = self.on_shopping_list_selected
    
    def _load_data(self):
        """Load initial data."""
        # Load shopping lists
        shopping_lists = self.shopping_list_vm.get_all_shopping_lists()
        self._update_shopping_lists_list(shopping_lists)
    
    def _update_shopping_lists_list(self, shopping_lists):
        """Update the shopping lists list."""
        # Clear the list
        self.shopping_lists_list.data = []
        
        # Add shopping lists to the list
        for shopping_list in shopping_lists:
            start_date_str = shopping_list.date_range_start.strftime("%Y-%m-%d")
            end_date_str = shopping_list.date_range_end.strftime("%Y-%m-%d")
            
            self.shopping_lists_list.data.append(
                (shopping_list.name, start_date_str, end_date_str)
            )
    
    def _on_shopping_list_error(self, error):
        """Handle shopping list error."""
        self.app.main_window.info_dialog("エラー", str(error))
    
    def _on_shopping_list_success(self, shopping_list):
        """Handle shopping list success."""
        self.app.main_window.info_dialog("成功", "買い物リストが保存されました")
        self._load_data()
    
    def _on_shopping_list_deleted(self, result):
        """Handle shopping list deleted."""
        if result:
            self.app.main_window.info_dialog("成功", "買い物リストが削除されました")
            self._load_data()
    
    def on_add_shopping_list(self, widget):
        """Handle add shopping list button press."""
        # Clear form fields
        self.name_input.value = ""
        self.start_date_input.value = None
        self.end_date_input.value = None
        self.items_table.data = []
    
    def on_generate_from_meal_plans(self, widget):
        """Handle generate from meal plans button press."""
        # In a real implementation, we would show a dialog to select date range and generate a shopping list
        # For now, this is just a placeholder
        pass
    
    def on_delete_shopping_list(self, widget):
        """Handle delete shopping list button press."""
        # Get selected shopping list
        selection = self.shopping_lists_list.selection
        if selection is None:
            self.app.main_window.info_dialog("エラー", "買い物リストを選択してください")
            return
        
        # Confirm deletion
        if self.app.main_window.question_dialog("確認", "選択した買い物リストを削除しますか？"):
            # Delete shopping list
            # Note: In a real implementation, we would need to get the shopping list ID
            # For now, this is just a placeholder
            pass
    
    def on_save_shopping_list(self, widget):
        """Handle save shopping list button press."""
        # Get form values
        name = self.name_input.value
        start_date = self.start_date_input.value
        end_date = self.end_date_input.value
        
        # Validate form values
        if not name:
            self.app.main_window.info_dialog("エラー", "名前を入力してください")
            return
        
        if not start_date:
            self.app.main_window.info_dialog("エラー", "開始日を選択してください")
            return
        
        if not end_date:
            self.app.main_window.info_dialog("エラー", "終了日を選択してください")
            return
        
        if start_date > end_date:
            self.app.main_window.info_dialog("エラー", "開始日は終了日より前である必要があります")
            return
        
        # Create shopping list data
        shopping_list_data = {
            "name": name,
            "date_range_start": start_date,
            "date_range_end": end_date,
        }
        
        # Get items data
        # In a real implementation, we would get the items from the table
        items_data = []
        
        # Create or update shopping list
        # Note: In a real implementation, we would check if we're editing an existing shopping list
        # For now, we'll just create a new one
        self.shopping_list_vm.create_shopping_list(shopping_list_data, items_data)
    
    def on_cancel_edit(self, widget):
        """Handle cancel edit button press."""
        # Clear form fields
        self.name_input.value = ""
        self.start_date_input.value = None
        self.end_date_input.value = None
        self.items_table.data = []
    
    def on_shopping_list_selected(self, table, row):
        """Handle shopping list selection."""
        # In a real implementation, we would load the selected shopping list details
        # For now, this is just a placeholder
        pass
    
    def on_filter_changed(self, widget):
        """Handle filter selection change."""
        # In a real implementation, we would filter the items table
        # For now, this is just a placeholder
        pass
    
    def on_category_changed(self, widget):
        """Handle category selection change."""
        # In a real implementation, we would filter the items table by category
        # For now, this is just a placeholder
        pass
    
    def on_add_item(self, widget):
        """Handle add item button press."""
        # In a real implementation, we would show a dialog to add an item
        # For now, this is just a placeholder
        pass
    
    def on_edit_item(self, widget):
        """Handle edit item button press."""
        # In a real implementation, we would show a dialog to edit the selected item
        # For now, this is just a placeholder
        pass
    
    def on_remove_item(self, widget):
        """Handle remove item button press."""
        # In a real implementation, we would remove the selected item
        # For now, this is just a placeholder
        pass
    
    def on_mark_purchased(self, widget):
        """Handle mark purchased button press."""
        # In a real implementation, we would mark the selected item as purchased
        # For now, this is just a placeholder
        pass