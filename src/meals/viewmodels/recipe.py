"""
Recipe ViewModel for the meal planner application.
"""

from typing import Dict, List, Optional

from meals.models.enums import RecipeCategory
from meals.repositories.recipe import RecipeRepository
from meals.schemas.recipe import IngredientCreate, IngredientRead, RecipeCreate, RecipeRead, RecipeUpdate
from meals.utils.exceptions import DatabaseException, ValidationException
from meals.viewmodels.base import BaseViewModel


class RecipeViewModel(BaseViewModel):
    """ViewModel for Recipe model."""
    
    def __init__(self):
        """Initialize the ViewModel."""
        super().__init__()
        self.recipe_repo = RecipeRepository()
    
    def create_recipe(self, recipe_data: Dict, ingredients_data: List[Dict]) -> Optional[RecipeRead]:
        """Create a new recipe with ingredients."""
        try:
            # Validate required fields for recipe
            self.validate_required_fields(recipe_data, ["name"])
            
            # Validate required fields for each ingredient
            for i, ingredient_data in enumerate(ingredients_data):
                try:
                    self.validate_required_fields(
                        ingredient_data, ["name", "quantity", "unit"]
                    )
                except ValidationException as e:
                    raise ValidationException(f"Ingredient {i+1}: {str(e)}")
            
            # Create recipe schema
            recipe_create = RecipeCreate(**recipe_data)
            
            # Create ingredient schemas
            ingredient_creates = [IngredientCreate(**data) for data in ingredients_data]
            
            # Create recipe with ingredients
            recipe = self.recipe_repo.create_with_ingredients(
                recipe_create.model_dump(exclude={"ingredients"}),
                [ing.model_dump() for ing in ingredient_creates],
            )
            
            # Get the created recipe with ingredients
            result = self.recipe_repo.get_with_ingredients(recipe.id)
            
            # Convert to schema
            recipe_read = RecipeRead.model_validate(result)
            
            # Handle success
            self._handle_success("create_recipe", recipe_read)
            
            return recipe_read
        except (ValidationException, DatabaseException) as e:
            self._handle_error("create_recipe", e)
            return None
    
    def update_recipe(
        self, recipe_id: int, recipe_data: Dict, ingredients_data: Optional[List[Dict]] = None
    ) -> Optional[RecipeRead]:
        """Update a recipe with ingredients."""
        try:
            # Check if recipe exists
            recipe = self.recipe_repo.get_by_id(recipe_id)
            if not recipe:
                raise ValidationException(f"Recipe with ID {recipe_id} not found")
            
            # Validate ingredients if provided
            if ingredients_data is not None:
                for i, ingredient_data in enumerate(ingredients_data):
                    try:
                        self.validate_required_fields(
                            ingredient_data, ["name", "quantity", "unit"]
                        )
                    except ValidationException as e:
                        raise ValidationException(f"Ingredient {i+1}: {str(e)}")
            
            # Create update schema
            recipe_update = RecipeUpdate(**recipe_data)
            
            # Update recipe with ingredients
            if ingredients_data is not None:
                ingredient_creates = [IngredientCreate(**data) for data in ingredients_data]
                updated_recipe = self.recipe_repo.update_with_ingredients(
                    recipe_id,
                    recipe_update.model_dump(exclude_none=True, exclude={"ingredients"}),
                    [ing.model_dump() for ing in ingredient_creates],
                )
            else:
                updated_recipe = self.recipe_repo.update(
                    recipe_id, recipe_update.model_dump(exclude_none=True, exclude={"ingredients"})
                )
            
            # Get the updated recipe with ingredients
            result = self.recipe_repo.get_with_ingredients(recipe_id)
            
            # Convert to schema
            recipe_read = RecipeRead.model_validate(result)
            
            # Handle success
            self._handle_success("update_recipe", recipe_read)
            
            return recipe_read
        except (ValidationException, DatabaseException) as e:
            self._handle_error("update_recipe", e)
            return None
    
    def delete_recipe(self, recipe_id: int) -> bool:
        """Delete a recipe."""
        try:
            # Check if recipe exists
            recipe = self.recipe_repo.get_by_id(recipe_id)
            if not recipe:
                raise ValidationException(f"Recipe with ID {recipe_id} not found")
            
            # Delete recipe
            result = self.recipe_repo.delete(recipe_id)
            
            # Handle success
            self._handle_success("delete_recipe", result)
            
            return result
        except (ValidationException, DatabaseException) as e:
            self._handle_error("delete_recipe", e)
            return False
    
    def get_recipe(self, recipe_id: int) -> Optional[RecipeRead]:
        """Get a recipe by ID."""
        try:
            # Get recipe with ingredients
            recipe = self.recipe_repo.get_with_ingredients(recipe_id)
            if not recipe:
                return None
            
            # Convert to schema
            recipe_read = RecipeRead.model_validate(recipe)
            
            return recipe_read
        except DatabaseException as e:
            self._handle_error("get_recipe", e)
            return None
    
    def get_all_recipes(self) -> List[RecipeRead]:
        """Get all recipes."""
        try:
            # Get all recipes with ingredients
            recipes = self.recipe_repo.get_all_with_ingredients()
            
            # Convert to schemas
            recipe_reads = [RecipeRead.model_validate(r) for r in recipes]
            
            return recipe_reads
        except DatabaseException as e:
            self._handle_error("get_all_recipes", e)
            return []
    
    def get_recipes_by_category(self, category: RecipeCategory) -> List[RecipeRead]:
        """Get recipes by category."""
        try:
            # Get recipes by category
            recipes = self.recipe_repo.get_by_category(category)
            
            # Convert to schemas
            recipe_reads = [RecipeRead.model_validate(r) for r in recipes]
            
            return recipe_reads
        except DatabaseException as e:
            self._handle_error("get_recipes_by_category", e)
            return []
    
    def search_recipes(self, query: str) -> List[RecipeRead]:
        """Search recipes by name or ingredients."""
        try:
            # Search recipes
            recipes = self.recipe_repo.search(query)
            
            # Convert to schemas
            recipe_reads = [RecipeRead.model_validate(r) for r in recipes]
            
            return recipe_reads
        except DatabaseException as e:
            self._handle_error("search_recipes", e)
            return []
    
    def add_ingredient(self, recipe_id: int, ingredient_data: Dict) -> Optional[IngredientRead]:
        """Add an ingredient to a recipe."""
        try:
            # Check if recipe exists
            recipe = self.recipe_repo.get_by_id(recipe_id)
            if not recipe:
                raise ValidationException(f"Recipe with ID {recipe_id} not found")
            
            # Validate required fields
            self.validate_required_fields(ingredient_data, ["name", "quantity", "unit"])
            
            # Create ingredient schema
            ingredient_create = IngredientCreate(**ingredient_data)
            
            # Add ingredient to recipe
            ingredient = self.recipe_repo.add_ingredient(recipe_id, ingredient_create.model_dump())
            
            # Convert to schema
            ingredient_read = IngredientRead.model_validate(ingredient)
            
            # Handle success
            self._handle_success("add_ingredient", ingredient_read)
            
            return ingredient_read
        except (ValidationException, DatabaseException) as e:
            self._handle_error("add_ingredient", e)
            return None
    
    def update_ingredient(self, ingredient_id: int, ingredient_data: Dict) -> Optional[IngredientRead]:
        """Update an ingredient."""
        try:
            # Update ingredient
            ingredient = self.recipe_repo.update_ingredient(ingredient_id, ingredient_data)
            if not ingredient:
                raise ValidationException(f"Ingredient with ID {ingredient_id} not found")
            
            # Convert to schema
            ingredient_read = IngredientRead.model_validate(ingredient)
            
            # Handle success
            self._handle_success("update_ingredient", ingredient_read)
            
            return ingredient_read
        except (ValidationException, DatabaseException) as e:
            self._handle_error("update_ingredient", e)
            return None
    
    def remove_ingredient(self, ingredient_id: int) -> bool:
        """Remove an ingredient from a recipe."""
        try:
            # Remove ingredient
            result = self.recipe_repo.remove_ingredient(ingredient_id)
            if not result:
                raise ValidationException(f"Ingredient with ID {ingredient_id} not found")
            
            # Handle success
            self._handle_success("remove_ingredient", result)
            
            return result
        except (ValidationException, DatabaseException) as e:
            self._handle_error("remove_ingredient", e)
            return False