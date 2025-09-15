from cachetools import TTLCache
from app.library.storage.enums import Meal, Gender


class UserContext:
    def __init__(self):
        self.cache = TTLCache(maxsize=1000, ttl=3000)

    def getMealDescription(self, userId: str) -> str:
        item = self.cache.get(userId)
        return item
    def setMealDescription(self, userId: str, description: str):
        self.cache[userId] = description
    def deleteMealDescription(self, userId: str):
        if userId in self.cache:
            del self.cache[userId]
    def getMeal(self, userId: str) -> Meal:
        item = self.cache.get(f'{userId}@meal')
        return item
    def setMeal(self, userId: str, meal: Meal):
        self.cache[f'{userId}@meal'] = meal
    def deleteMeal(self, userId: str):
        if f'{userId}@meal' in self.cache:
            del self.cache[f'{userId}@meal']
    def setPicture(self, userId: str, picture: bytearray):
        self.cache[f'{userId}@pic'] = picture
    def getPicture(self, userId: str) -> bytearray:
        return self.cache.get(f'{userId}@pic')
    def deletePicture(self, userId: str):
        if f'{userId}@pic' in self.cache:
            del self.cache[f'{userId}@pic']
    def setHeight(self, userId: str, height: float):
        self.cache[f'{userId}@height'] = height
    def getHeight(self, userId: str) -> float:
        return self.cache.get(f'{userId}@height')
    def deleteHeight(self, userId: str):
        if f'{userId}@height' in self.cache:
            del self.cache[f'{userId}@height']
    def setWeight(self, userId: str, weight: float):
        self.cache[f'{userId}@weight'] = weight
    def getWeight(self, userId: str) -> float:
        return self.cache.get(f'{userId}@weight')
    def deleteWeight(self, userId: str):
        if f'{userId}@weight' in self.cache:
            del self.cache[f'{userId}@weight']
    def setAge(self, userId: str, age: int):
        self.cache[f'{userId}@age'] = age
    def getAge(self, userId: str) -> int:
        return self.cache.get(f'{userId}@age')
    def deleteAge(self, userId: str):
        if f'{userId}@age' in self.cache:
            del self.cache[f'{userId}@age']
    def setGender(self, userId: str, gender: Gender):
        self.cache[f'{userId}@gender'] = gender
    def getGender(self, userId: str) -> Gender:
        return self.cache.get(f'{userId}@gender')
    def deleteGender(self, userId: str):
        if f'{userId}@gender' in self.cache:
            del self.cache[f'{userId}@gender']
    def getRegisterProcess(self, userId: str) -> bool:
        return self.cache.get(f'{userId}@registerProcess')
    def setRegisterProcess(self, userId: str, isProcess: bool):
        self.cache[f'{userId}@registerProcess'] = isProcess
    def deleteRegisterProcess(self, userId: str):
        if f'{userId}@registerProcess' in self.cache:
            del self.cache[f'{userId}@registerProcess']
    def getStartReport(self, userId: str) -> str:
        return self.cache.get(f'{userId}@startReport')
    def setStartReport(self, userId: str, start_date: str):
        self.cache[f'{userId}@startReport'] = start_date
    def deleteStartReport(self, userId: str):
        if f'{userId}@startReport' in self.cache:
            del self.cache[f'{userId}@startReport']