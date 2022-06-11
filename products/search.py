from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod
# from .models import Label as LabelModel , Category as CategoryModel

from enum import Enum
from pydantic import BaseModel
from enum import Enum
from django.db import models as django_models

class BaseSearchModelData(BaseModel):
    key: str
    value_type: type  

    @property
    def model(self):

      class Model(BaseModel):
        
        key = self.key 
        value:self.value_type

      return Model

# The search Words I can search with 
class SearchWord(Enum):
    Name = BaseSearchModelData(key="name", value_type=str)
    Describtion = BaseSearchModelData(key="describtion", value_type=str)
    MinPrice = BaseSearchModelData(key="min_price", value_type=float)
    MaxPrice = BaseSearchModelData(key="max_price", value_type=float)
    Price = BaseSearchModelData(key="price", value_type=float)
    # Label = BaseSearchModelData(key="label", value_type=LabelModel)
    # Labels = BaseSearchModelData(key="labels", value_type=list[LabelModel])
    # Category = BaseSearchModelData(key="category", value_type=CategoryModel)
    # Categories = BaseSearchModelData(key="categories ", value_type=list[CategoryModel])


    @classmethod
    def models(cls)->tuple[str]:
      """Return tuple of models that you can search on it"""
      return [ cls._member_map_[key].value for key in cls._member_map_ ]





name = SearchWord.Name.value.model(value="Name")

print(name)
# TODO validate the SearchQueryData

"""Search Levels
- Validate the data 
- Create Search Object 
- register Search Object in Search Manager 
- run them in Search Manager 
"""


# Key must be allowed
@dataclass
class SearchQueryData:
    """Store the Key , Value for Search if it Valid"""

    key: SearchWord
    value: str | float | int | django_models.QuerySet

    def valid_value(self) -> bool:
        """Validate the Value return True or False"""
        value = self.value
        if value is not None and value != "":
            return True
        return False

    def valid_key(self) -> bool:
        """Validate the Key return True Or False"""
        if self.key in SearchWord._member_map_ or self.key in SearchWord._member_names_:
            return True
        return False


    # Run all Validate functions to ensure the Data is Right 
    def is_valid(self) -> bool:
        """validate if the object can be search based on it return True OR False"""
        return all([self.valid_key(), self.valid_value()])


    def __str__(self) -> str:
        return f"(key={self.key},value={self.value})"





class BaseSearch(ABC):

    def __init__(self,data:SearchQueryData) -> None:
        self.data = data 

    @abstractmethod
    def search(self,query_set:django_models.QuerySet) -> django_models.QuerySet:
        """Search the Model and Return QuerySet"""
        pass


class SearchManager:
    search_queries: list[BaseSearch] = []

    def register(self,search_object:BaseSearch):
        pass 

if __name__ == "__main__":
    sq = SearchQueryData(SearchWord.Name, "value")
    print(sq)
    print(sq.valid_key())
    print(sq.valid_value())
