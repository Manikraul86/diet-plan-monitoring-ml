from fastapi import FastAPI
from pydantic import BaseModel,Field
from typing import Annotated
from typing import List,Optional
import pandas as pd
import os
from model import recommend,output_recommended_recipes

# Get the absolute path to the Data directory
data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data', 'dataset.csv')
recipe_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data', 'recipe.csv')
dataset=pd.read_csv(data_path,compression='gzip')

app = FastAPI()


class params(BaseModel):
    n_neighbors:int=5
    return_distance:bool=False

class PredictionIn(BaseModel):
    nutrition_input:Annotated[List[float], Field(min_length=9, max_length=9)]
    ingredients:list[str]=[]
    params:Optional[params]


class Recipe(BaseModel):
    Name:str
    CookTime:int
    PrepTime:int
    TotalTime:int
    RecipeIngredientParts:list[str]
    Calories:float
    FatContent:float
    SaturatedFatContent:float
    CholesterolContent:float
    SodiumContent:float
    CarbohydrateContent:float
    FiberContent:float
    SugarContent:float
    ProteinContent:float
    RecipeInstructions:list[str]

class PredictionOut(BaseModel):
    output: Optional[List[Recipe]] = None


@app.get("/")
def home():
    return {"health_check": "OK"}


@app.post("/predict/",response_model=PredictionOut)
def update_item(prediction_input:PredictionIn):
    recommendation_dataframe=recommend(dataset,prediction_input.nutrition_input,prediction_input.ingredients,prediction_input.params.dict())
    output=output_recommended_recipes(recommendation_dataframe)
    if output is None:
        return {"output":None}
    else:
        return {"output":output}

