"""
Recipe view for the meal planner application.
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from meals.viewmodels.recipe import RecipeViewModel


class RecipeView:
    """Recipe view for the meal planner application."""
    
    def __init__(self, app):
        """Initialize the recipe view."""
        self.app = app
        self.content = None
        self.recipe_vm = RecipeViewModel()
        
        # UI components
        self.recipes_list = None
        self.recipe_details = None
        self.name_input = None
        self.description_input = None
        self.preparation_time_input = None
        self.category_selection = None
        self.cooking_instructions_input = None
        self.ingredients_table = None
        
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
            "レシピ管理",
            style=Pack(padding=(0, 0, 10, 0), font_size=18, font_weight="bold")
        )
        self.content.add(title_label)
        
        # Split view for list and details
        split_container = toga.SplitContainer(style=Pack(flex=1))
        
        # Recipes list
        list_container = toga.Box(style=Pack(direction=COLUMN, padding=5))
        list_label = toga.Label("レシピ一覧", style=Pack(padding=(0, 0, 5, 0), font_weight="bold"))
        self.recipes_list = toga.Table(
            headings=["名前", "カテゴリ", "調理時間"],
            style=Pack(flex=1),
        )
        
        # Search box
        search_box = toga.Box(style=Pack(direction=ROW, padding=5))
        search_label = toga.Label("検索:", style=Pack(width=50, padding=(0, 5, 0, 0)))
        search_input = toga.TextInput(style=Pack(flex=1))
        search_button = toga.Button("検索", on_press=self.on_search)
        search_box.add(search_label)
        search_box.add(search_input)
        search_box.add(search_button)
        
        # Buttons for list actions
        list_actions = toga.Box(style=Pack(direction=ROW, padding=5))
        add_button = toga.Button("追加", on_press=self.on_add_recipe)
        delete_button = toga.Button("削除", on_press=self.on_delete_recipe)
        
        list_actions.add(add_button)
        list_actions.add(delete_button)
        
        list_container.add(list_label)
        list_container.add(search_box)
        list_container.add(self.recipes_list)
        list_container.add(list_actions)
        
        # Recipe details
        details_container = toga.ScrollContainer(style=Pack(flex=1))
        details_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
        details_label = toga.Label("レシピ詳細", style=Pack(padding=(0, 0, 5, 0), font_weight="bold"))
        
        # Form for recipe details
        form_container = toga.Box(style=Pack(direction=COLUMN, padding=5))
        
        # Name input
        name_box = toga.Box(style=Pack(direction=ROW, padding=2))
        name_label = toga.Label("名前:", style=Pack(width=100, padding=(0, 5, 0, 0)))
        self.name_input = toga.TextInput(style=Pack(flex=1))
        name_box.add(name_label)
        name_box.add(self.name_input)
        
        # Category selection
        category_box = toga.Box(style=Pack(direction=ROW, padding=2))
        category_label = toga.Label("カテゴリ:", style=Pack(width=100, padding=(0, 5, 0, 0)))
        self.category_selection = toga.Selection(
            items=["主菜", "副菜", "スープ", "サラダ", "デザート", "飲み物", "その他"],
            style=Pack(flex=1),
        )
        category_box.add(category_label)
        category_box.add(self.category_selection)
        
        # Preparation time input
        time_box = toga.Box(style=Pack(direction=ROW, padding=2))
        time_label = toga.Label("調理時間(分):", style=Pack(width=100, padding=(0, 5, 0, 0)))
        self.preparation_time_input = toga.NumberInput(
            min_value=1,
            max_value=999,
            step=1,
            style=Pack(width=100),
        )
        time_box.add(time_label)
        time_box.add(self.preparation_time_input)
        
        # Description input
        description_box = toga.Box(style=Pack(direction=COLUMN, padding=2))
        description_label = toga.Label("説明:", style=Pack(padding=(0, 0, 5, 0)))
        self.description_input = toga.MultilineTextInput(
            style=Pack(flex=1, height=80),
        )
        description_box.add(description_label)
        description_box.add(self.description_input)
        
        # Cooking instructions input
        instructions_box = toga.Box(style=Pack(direction=COLUMN, padding=2))
        instructions_label = toga.Label("調理手順:", style=Pack(padding=(0, 0, 5, 0)))
        self.cooking_instructions_input = toga.MultilineTextInput(
            style=Pack(flex=1, height=150),
        )
        instructions_box.add(instructions_label)
        instructions_box.add(self.cooking_instructions_input)
        
        # Ingredients table
        ingredients_box = toga.Box(style=Pack(direction=COLUMN, padding=2))
        ingredients_label = toga.Label("材料:", style=Pack(padding=(0, 0, 5, 0)))
        self.ingredients_table = toga.Table(
            headings=["材料名", "分量", "単位", "カテゴリ"],
            style=Pack(flex=1, height=150),
        )
        
        # Buttons for ingredients actions
        ingredients_actions = toga.Box(style=Pack(direction=ROW, padding=2))
        add_ingredient_button = toga.Button("材料を追加", on_press=self.on_add_ingredient)
        edit_ingredient_button = toga.Button("材料を編集", on_press=self.on_edit_ingredient)
        remove_ingredient_button = toga.Button("材料を削除", on_press=self.on_remove_ingredient)
        
        ingredients_actions.add(add_ingredient_button)
        ingredients_actions.add(edit_ingredient_button)
        ingredients_actions.add(remove_ingredient_button)
        
        ingredients_box.add(ingredients_label)
        ingredients_box.add(self.ingredients_table)
        ingredients_box.add(ingredients_actions)
        
        # Add form elements
        form_container.add(name_box)
        form_container.add(category_box)
        form_container.add(time_box)
        form_container.add(description_box)
        form_container.add(instructions_box)
        form_container.add(ingredients_box)
        
        # Buttons for details actions
        details_actions = toga.Box(style=Pack(direction=ROW, padding=5))
        save_button = toga.Button("保存", on_press=self.on_save_recipe)
        cancel_button = toga.Button("キャンセル", on_press=self.on_cancel_edit)
        
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
        # Register handlers for recipe view model
        self.recipe_vm.register_error_handler("create_recipe", self._on_recipe_error)
        self.recipe_vm.register_error_handler("update_recipe", self._on_recipe_error)
        self.recipe_vm.register_error_handler("delete_recipe", self._on_recipe_error)
        
        self.recipe_vm.register_success_handler("create_recipe", self._on_recipe_success)
        self.recipe_vm.register_success_handler("update_recipe", self._on_recipe_success)
        self.recipe_vm.register_success_handler("delete_recipe", self._on_recipe_deleted)
        
        # Set up table selection handler
        self.recipes_list.on_select = self.on_recipe_selected
    
    def _load_data(self):
        """Load initial data."""
        # Load recipes
        recipes = self.recipe_vm.get_all_recipes()
        self._update_recipes_list(recipes)
    
    def _update_recipes_list(self, recipes):
        """Update the recipes list."""
        # Clear the list
        self.recipes_list.data = []
        
        # Add recipes to the list
        for recipe in recipes:
            category_str = recipe.category.value if recipe.category else ""
            if category_str == "MAIN_DISH":
                category_str = "主菜"
            elif category_str == "SIDE_DISH":
                category_str = "副菜"
            elif category_str == "SOUP":
                category_str = "スープ"
            elif category_str == "SALAD":
                category_str = "サラダ"
            elif category_str == "DESSERT":
                category_str = "デザート"
            elif category_str == "DRINK":
                category_str = "飲み物"
            elif category_str == "OTHER":
                category_str = "その他"
            
            preparation_time = f"{recipe.preparation_time}分" if recipe.preparation_time else ""
            
            self.recipes_list.data.append(
                (recipe.name, category_str, preparation_time)
            )
    
    def _on_recipe_error(self, error):
        """Handle recipe error."""
        self.app.main_window.info_dialog("エラー", str(error))
    
    def _on_recipe_success(self, recipe):
        """Handle recipe success."""
        self.app.main_window.info_dialog("成功", "レシピが保存されました")
        self._load_data()
    
    def _on_recipe_deleted(self, result):
        """Handle recipe deleted."""
        if result:
            self.app.main_window.info_dialog("成功", "レシピが削除されました")
            self._load_data()
    
    def on_search(self, widget):
        """Handle search button press."""
        # In a real implementation, we would search for recipes
        # For now, this is just a placeholder
        pass
    
    def on_add_recipe(self, widget):
        """Handle add recipe button press."""
        # Clear form fields
        self.name_input.value = ""
        self.description_input.value = ""
        self.preparation_time_input.value = 30
        self.category_selection.value = "主菜"
        self.cooking_instructions_input.value = ""
        self.ingredients_table.data = []
    
    def on_delete_recipe(self, widget):
        """Handle delete recipe button press."""
        # Get selected recipe
        selection = self.recipes_list.selection
        if selection is None:
            self.app.main_window.info_dialog("エラー", "レシピを選択してください")
            return
        
        # Confirm deletion
        if self.app.main_window.question_dialog("確認", "選択したレシピを削除しますか？"):
            # Delete recipe
            # Note: In a real implementation, we would need to get the recipe ID
            # For now, this is just a placeholder
            pass
    
    def on_save_recipe(self, widget):
        """Handle save recipe button press."""
        # Get form values
        name = self.name_input.value
        description = self.description_input.value
        preparation_time = self.preparation_time_input.value
        category = self.category_selection.value
        cooking_instructions = self.cooking_instructions_input.value
        
        # Validate form values
        if not name:
            self.app.main_window.info_dialog("エラー", "名前を入力してください")
            return
        
        # Convert category to enum value
        if category == "主菜":
            category = "MAIN_DISH"
        elif category == "副菜":
            category = "SIDE_DISH"
        elif category == "スープ":
            category = "SOUP"
        elif category == "サラダ":
            category = "SALAD"
        elif category == "デザート":
            category = "DESSERT"
        elif category == "飲み物":
            category = "DRINK"
        elif category == "その他":
            category = "OTHER"
        
        # Create recipe data
        recipe_data = {
            "name": name,
            "description": description,
            "preparation_time": preparation_time,
            "category": category,
            "cooking_instructions": cooking_instructions,
        }
        
        # Get ingredients data
        # In a real implementation, we would get the ingredients from the table
        ingredients_data = []
        
        # Create or update recipe
        # Note: In a real implementation, we would check if we're editing an existing recipe
        # For now, we'll just create a new one
        self.recipe_vm.create_recipe(recipe_data, ingredients_data)
    
    def on_cancel_edit(self, widget):
        """Handle cancel edit button press."""
        # Clear form fields
        self.name_input.value = ""
        self.description_input.value = ""
        self.preparation_time_input.value = 30
        self.category_selection.value = "主菜"
        self.cooking_instructions_input.value = ""
        self.ingredients_table.data = []
    
    def on_recipe_selected(self, table, row):
        """Handle recipe selection."""
        # In a real implementation, we would load the selected recipe details
        # For now, this is just a placeholder
        pass
    
    def on_add_ingredient(self, widget):
        """Handle add ingredient button press."""
        # In a real implementation, we would show a dialog to add an ingredient
        # For now, this is just a placeholder
        pass
    
    def on_edit_ingredient(self, widget):
        """Handle edit ingredient button press."""
        # In a real implementation, we would show a dialog to edit the selected ingredient
        # For now, this is just a placeholder
        pass
    
    def on_remove_ingredient(self, widget):
        """Handle remove ingredient button press."""
        # In a real implementation, we would remove the selected ingredient
        # For now, this is just a placeholder
        pass