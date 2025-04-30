from typing import List
import pandas as pd
from pydantic import BaseModel, Field

class FoodItem(BaseModel):
  name: str = Field(description='Name of the food item')
  quantity: int = Field(description='Quantity of the food item')
  price: float = Field(description='Price of the food item')
  currency: str = Field(description='Currency of the price')

def to_dataframe(food_items: List[FoodItem]) -> pd.DataFrame:
  df = pd.DataFrame(
    {
      "Quantity": [item.quantity for item in food_items],
      "Food Item": [item.name for item in food_items],
      "Currency": [item.currency for item in food_items],
      "Price": ["{:.2f}".format(item.price) for item in food_items],
    }
  )
  return df