"""
MealPlan view for the meal planner application.
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from meals.viewmodels.meal_plan import MealPlanViewModel
from meals.viewmodels.recipe import RecipeViewModel


class MealPlanView:
    """MealPlan view for the meal planner application."""
    
    def __init__(self, app):
        """Initialize the meal plan view."""
        self.app = app
        self.content = None
        self.meal_plan_vm = MealPlanViewModel()
        self.recipe_vm = RecipeViewModel()
        
        # UI components
        self.meal_plans_list = None
        self.meal_plan_details = None
        self.date_input = None
        self.meal_type_selection = None
        self.name_input = None
        self.recipes_selection = None
        
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
            "献立管理",
            style=Pack(padding=(0, 0, 10, 0), font_size=18, font_weight="bold")
        )
        self.content.add(title_label)
        
        # Split view for list and details
        split_container = toga.SplitContainer(style=Pack(flex=1))
        
        # Meal plans list
        list_container = toga.Box(style=Pack(direction=COLUMN, padding=5))
        list_label = toga.Label("献立一覧", style=Pack(padding=(0, 0, 5, 0), font_weight="bold"))
        self.meal_plans_list = toga.Table(
            headings=["日付", "食事", "名前"],
            style=Pack(flex=1),
        )
        
        # Buttons for list actions
        list_actions = toga.Box(style=Pack(direction=ROW, padding=5))
        add_button = toga.Button("追加")
        add_button.on_press = self.on_add_meal_plan
        delete_button = toga.Button("削除")
        delete_button.on_press = self.on_delete_meal_plan
        
        list_actions.add(add_button)
        list_actions.add(delete_button)
        
        list_container.add(list_label)
        list_container.add(self.meal_plans_list)
        list_container.add(list_actions)
        
        # Meal plan details
        details_container = toga.Box(style=Pack(direction=COLUMN, padding=5))
        details_label = toga.Label("献立詳細", style=Pack(padding=(0, 0, 5, 0), font_weight="bold"))
        
        # Form for meal plan details
        form_container = toga.Box(style=Pack(direction=COLUMN, padding=5))
        
        # Name input
        name_box = toga.Box(style=Pack(direction=ROW, padding=2))
        name_label = toga.Label("名前:", style=Pack(width=100, padding=(0, 5, 0, 0)))
        self.name_input = toga.TextInput(style=Pack(flex=1))
        name_box.add(name_label)
        name_box.add(self.name_input)
        
        # Date input
        date_box = toga.Box(style=Pack(direction=ROW, padding=2))
        date_label = toga.Label("日付:", style=Pack(width=100, padding=(0, 5, 0, 0)))
        self.date_input = toga.DateInput(style=Pack(flex=1))
        date_box.add(date_label)
        date_box.add(self.date_input)
        
        # Meal type selection
        meal_type_box = toga.Box(style=Pack(direction=ROW, padding=2))
        meal_type_label = toga.Label("食事タイプ:", style=Pack(width=100, padding=(0, 5, 0, 0)))
        self.meal_type_selection = toga.Selection(
            items=["朝食", "昼食", "夕食"],
            style=Pack(flex=1),
        )
        meal_type_box.add(meal_type_label)
        meal_type_box.add(self.meal_type_selection)
        
        # Recipes selection
        recipes_box = toga.Box(style=Pack(direction=COLUMN, padding=2))
        recipes_label = toga.Label("レシピ:", style=Pack(padding=(0, 0, 5, 0)))
        self.recipes_selection = toga.MultilineTextInput(
            readonly=True,
            style=Pack(flex=1, height=150),
        )
        recipes_actions = toga.Box(style=Pack(direction=ROW, padding=2))
        add_recipe_button = toga.Button("レシピを追加")
        add_recipe_button.on_press = self.on_add_recipe
        remove_recipe_button = toga.Button("レシピを削除")
        remove_recipe_button.on_press = self.on_remove_recipe
        recipes_actions.add(add_recipe_button)
        recipes_actions.add(remove_recipe_button)
        
        recipes_box.add(recipes_label)
        recipes_box.add(self.recipes_selection)
        recipes_box.add(recipes_actions)
        
        # Add form elements
        form_container.add(name_box)
        form_container.add(date_box)
        form_container.add(meal_type_box)
        form_container.add(recipes_box)
        
        # Buttons for details actions
        details_actions = toga.Box(style=Pack(direction=ROW, padding=5))
        save_button = toga.Button("保存")
        save_button.on_press = self.on_save_meal_plan
        cancel_button = toga.Button("キャンセル")
        cancel_button.on_press = self.on_cancel_edit
        
        details_actions.add(save_button)
        details_actions.add(cancel_button)
        
        details_container.add(details_label)
        details_container.add(form_container)
        details_container.add(details_actions)
        
        # Add containers to split view
        split_container.content = [list_container, details_container]
        
        # Add split view to main container
        self.content.add(split_container)
    
    def _register_handlers(self):
        """Register event handlers."""
        # Register handlers for meal plan view model
        self.meal_plan_vm.register_error_handler("create_meal_plan", self._on_meal_plan_error)
        self.meal_plan_vm.register_error_handler("update_meal_plan", self._on_meal_plan_error)
        self.meal_plan_vm.register_error_handler("delete_meal_plan", self._on_meal_plan_error)
        
        self.meal_plan_vm.register_success_handler("create_meal_plan", self._on_meal_plan_success)
        self.meal_plan_vm.register_success_handler("update_meal_plan", self._on_meal_plan_success)
        self.meal_plan_vm.register_success_handler("delete_meal_plan", self._on_meal_plan_deleted)
        
        # Set up table selection handler
        self.meal_plans_list.on_select = self.on_meal_plan_selected
    
    def _load_data(self):
        """Load initial data."""
        # Load meal plans
        meal_plans = self.meal_plan_vm.get_all_meal_plans()
        self._update_meal_plans_list(meal_plans)
    
    def _update_meal_plans_list(self, meal_plans):
        """Update the meal plans list."""
        # Clear the list
        self.meal_plans_list.data = []
        
        # Add meal plans to the list
        for meal_plan in meal_plans:
            date_str = meal_plan.date.strftime("%Y-%m-%d")
            meal_type_str = meal_plan.meal_type.value
            if meal_type_str == "BREAKFAST":
                meal_type_str = "朝食"
            elif meal_type_str == "LUNCH":
                meal_type_str = "昼食"
            elif meal_type_str == "DINNER":
                meal_type_str = "夕食"
            
            self.meal_plans_list.data.append(
                (date_str, meal_type_str, meal_plan.name)
            )
    
    def _on_meal_plan_error(self, error):
        """Handle meal plan error."""
        self.app.main_window.info_dialog("エラー", str(error))
    
    def _on_meal_plan_success(self, meal_plan):
        """Handle meal plan success."""
        self.app.main_window.info_dialog("成功", "献立が保存されました")
        self._load_data()
    
    def _on_meal_plan_deleted(self, result):
        """Handle meal plan deleted."""
        if result:
            self.app.main_window.info_dialog("成功", "献立が削除されました")
            self._load_data()
    
    def on_add_meal_plan(self, widget):
        """Handle add meal plan button press."""
        # Clear form fields
        self.name_input.value = ""
        self.date_input.value = None
        self.meal_type_selection.value = "朝食"
        self.recipes_selection.value = ""
    
    def on_delete_meal_plan(self, widget):
        """Handle delete meal plan button press."""
        # Get selected meal plan
        selection = self.meal_plans_list.selection
        if selection is None:
            self.app.main_window.info_dialog("エラー", "献立を選択してください")
            return
        
        # Confirm deletion
        if self.app.main_window.question_dialog("確認", "選択した献立を削除しますか？"):
            # Delete meal plan
            # Note: In a real implementation, we would need to get the meal plan ID
            # For now, this is just a placeholder
            pass
    
    def on_save_meal_plan(self, widget):
        """Handle save meal plan button press."""
        # Get form values
        name = self.name_input.value
        date_val = self.date_input.value
        meal_type = self.meal_type_selection.value
        
        # Validate form values
        if not name:
            self.app.main_window.info_dialog("エラー", "名前を入力してください")
            return
        
        if not date_val:
            self.app.main_window.info_dialog("エラー", "日付を選択してください")
            return
        
        # Convert meal type to enum value
        if meal_type == "朝食":
            meal_type = "BREAKFAST"
        elif meal_type == "昼食":
            meal_type = "LUNCH"
        elif meal_type == "夕食":
            meal_type = "DINNER"
        
        # Create meal plan data
        meal_plan_data = {
            "name": name,
            "date": date_val,
            "meal_type": meal_type,
            "recipe_ids": [],  # In a real implementation, we would get selected recipe IDs
        }
        
        # Create or update meal plan
        # Note: In a real implementation, we would check if we're editing an existing meal plan
        # For now, we'll just create a new one
        self.meal_plan_vm.create_meal_plan(meal_plan_data)
    
    def on_cancel_edit(self, widget):
        """Handle cancel edit button press."""
        # Clear form fields
        self.name_input.value = ""
        self.date_input.value = None
        self.meal_type_selection.value = "朝食"
        self.recipes_selection.value = ""
    
    def on_meal_plan_selected(self, table, row):
        """Handle meal plan selection."""
        # In a real implementation, we would load the selected meal plan details
        # For now, this is just a placeholder
        pass
    
    def on_add_recipe(self, widget):
        """Handle add recipe button press."""
        # In a real implementation, we would show a dialog to select recipes
        # For now, this is just a placeholder
        pass
    
    def on_remove_recipe(self, widget):
        """Handle remove recipe button press."""
        # In a real implementation, we would remove the selected recipe from the meal plan
        # For now, this is just a placeholder
        pass