from app.library.storage.models import User, History
from app.library.storage.enums import Meal, Gender
import json

class UserProfile:
    def __init__(self, info: User):
        self.user_id = info.line_id
        self.height = info.height
        self.weight = info.weight
        self.age = info.age
        self.gender = info.gender
        self.history = {}
    def add_history(self, infos: list[History]):
        for info in infos:
            data = {
                "calories_kcal": info.calories_kcal,
                "protein_g": info.protein_g,
                "carbs_g": info.carbs_g,
                "fat_g": info.fat_g,
                "sodium_mg": info.sodium_mg,
                "description": info.ai_description,
                "personalized_advice": info.ai_suggest,
            }
            m = Meal(info.meal)
            self.history[m.getChinese()] = data
    def to_text(self) -> str:
        g = Gender(self.gender)
        data = {
            "user_profile": {
                "user_id": self.user_id,
                "height_cm": float(self.height),
                "weight_kg": float(self.weight),
                "age": self.age,
                "gender": g.getChinese(),
            },
            "nutrient_intake": self.history
        }
        return json.dumps(data, ensure_ascii=False)