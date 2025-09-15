import base64
from openai import OpenAI
from app.library.gpt.prompt import agent_prompt
from app.library.gpt.models import UserProfile, Food
from typing import Dict
import json

class NutritionAPI:
    def __init__(self, api_key, model="gpt-4.1-mini", max_tokens=1200,temperature=0.2, presence_penalty=0):
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.presence_penalty = presence_penalty
        self.client = OpenAI(api_key=api_key)

    def get_meal_info(self, food_item: Food, user_profile: UserProfile) -> Dict:
        image = food_item.getImage()
        img = base64.b64encode(image).decode("utf-8")
        user_ctx = user_profile.to_text()
        resp = self.client.responses.create(
            model=self.model,
            temperature=self.temperature,
            max_output_tokens=self.max_tokens,
            input=[
                {
                    "role": "system",
                    "content": [
                        {"type": "input_text", "text": agent_prompt},
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": f"這是{food_item.getName()}, 請分析這張照片（繁體中文輸出）。"},
                        {"type": "input_text", "text": user_ctx },
                        {"type": "input_image", "image_url": f"data:image/jpeg;base64,{img}"},
                    ],
                },
            ],
        )
        result = json.loads(resp.output_text)
        return result