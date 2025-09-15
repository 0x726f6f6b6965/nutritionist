from enum import Enum

class Meal(Enum):
    BREAKFAST = 1
    LUNCH = 2
    DINNER = 3
    DESSERT = 4

    def getChinese(self):
        match self:
            case Meal.BREAKFAST:
                return "早餐"
            case Meal.LUNCH:
                return "午餐"
            case Meal.DINNER:
                return "晚餐"
            case Meal.DESSERT:
                return "點心"
            case _:
                return "未知"

class Gender(Enum):
    MALE = 1
    FEMALE = 2

    def getChinese(self):
        match self:
            case Gender.MALE:
                return "男"
            case Gender.FEMALE:
                return "女"
            case _:
                return "未知"