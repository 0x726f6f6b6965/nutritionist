from app.library.storage.enums import Meal
class Food:
    def __init__(self, name: str, meal: Meal, image: bytes):
        self.name = name
        self.image = image
        self.meal = meal
    def __repr__(self):
        return f"<Food(name={self.name!r}, meal={self.meal!r}, image_length={len(self.image) if self.image else 0})>"
    def getImage(self):
        return self.image
    def getName(self):
        return self.name
    def getMeal(self):
        return self.meal.getChinese()