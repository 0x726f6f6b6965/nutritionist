from os import environ
from urllib.parse import parse_qs
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    Configuration, 
    ApiClient, 
    MessagingApi, 
    ReplyMessageRequest, 
    TextMessage,
    MessagingApiBlob,
    FlexMessage,
    FlexBubble,
)
from linebot.v3.webhooks import (
    MessageEvent, 
    PostbackEvent,
    TextMessageContent, 
    ImageMessageContent,
)
from app.library.storage.cache import UserContext
from app.library.storage.enums import Meal, Gender
from app.library.storage.psql import engine
from app.library.storage.operation import UserObject, DietHistory
from app.library.storage.models import User, History
from app.library.msg import GetCheckMsg, GetUploadMsg, GetSetMealMsg, GetMonthMsg, GetAIMealResponseMsg
from datetime import datetime, timedelta, time
from dateutil.relativedelta import relativedelta
from app.library.gpt import NutritionAPI
from app.library.gpt.models import Food, UserProfile
import json


configuration = Configuration(access_token=environ.get('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(environ.get('CHANNEL_SECRET'))
nutrition_api = NutritionAPI(api_key=environ.get('OPENAI_API_KEY'))
cache = UserContext()
user_table = UserObject(engine)
history_table = DietHistory(engine)

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        # here only handle meal description.
        line_bot_api = MessagingApi(api_client)
        context = event.message.text
        user = event.source.user_id
        user_info = getUserInfo(user)
        # the first use.
        # add simple user information first.
        if user_info is None:
            addUserProcess(line_bot_api, user, event)
            return
        meal = cache.getMeal(user)
        if meal is None:
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token, messages=[TextMessage(text="請點擊下方選單開始上傳餐點")]))
            return
        cache.setMealDescription(user, context)
        msg = GetCheckMsg(
            "上傳餐點", 
            [("餐點", meal.getChinese()), ("名稱", context)],
            ("action=check_descript&data=y","action=check_descript&data=n"))
        bubble_container = FlexBubble()
        bubble_container = bubble_container.from_dict(msg)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token, messages=[FlexMessage(
                    alt_text="upload img",
                    contents=bubble_container)]
            ))
        return

@handler.add(MessageEvent, message=ImageMessageContent)
def handle_imgae(event):
    with ApiClient(configuration) as api_client:
        # here only handle food image
        # and will reponse the ai analysis.
        now = datetime.now()
        line_bot_api = MessagingApi(api_client)
        user = event.source.user_id
        user_info = getUserInfo(user)
        if user_info is None:
            addUserProcess(line_bot_api, user, event)
            return
        meal = cache.getMeal(user)
        description = cache.getMealDescription(user)
        if meal is None or description is None:
            bubble_container = FlexBubble()
            bubble_container = bubble_container.from_dict(GetSetMealMsg())
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token, messages=[FlexMessage(
                        alt_text="set description",
                        contents=bubble_container)]
                ))
            return
        api_instance = MessagingApiBlob(api_client)
        img = api_instance.get_message_content(event.message.id)
        cache.setPicture(user, img)
        if cache.getPicture(user) is None:
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token, messages=[TextMessage(text="please send picture again")]))
            return
        photo = cache.getPicture(user)
        user_profile = UserProfile(user_info)
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        start = datetime.combine(today, time.min)
        end = datetime.combine(tomorrow, time.min)
        histories = history_table.GetHistory(user, start, end)
        if len(histories) > 0:
            user_profile.add_history(histories)
        resp = nutrition_api.get_meal_info(Food(description, meal, photo), user_profile)
        if resp is None:
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token, messages=[TextMessage(text="ai response error")]))
            return
        if resp["is_food"] == False:
            line_bot_api.reply_message_with_http_info( 
              ReplyMessageRequest( 
                reply_token=event.reply_token, messages=[TextMessage(text="這似乎不是餐點的照片，請重新上傳")]))
            return
        data = History(
            line_id = user,
            meal = meal.value,
            description = description,
            photo = photo,
            calories_kcal = resp["dishes"][0]["est_nutrition"]["calories_kcal"],
            protein_g = resp["dishes"][0]["est_nutrition"]["protein_g"],
            carbs_g = resp["dishes"][0]["est_nutrition"]["carbs_g"],
            fat_g = resp["dishes"][0]["est_nutrition"]["fat_g"],
            sodium_mg = resp["dishes"][0]["est_nutrition"]["sodium_mg"],
            ai_description = resp["explanations_zh"],
            ai_suggest = resp["personalized_advice"]
        )
        history_table.AddHistory(data)
        cache.deleteMeal(user)
        cache.deleteMealDescription(user)
        cache.deletePicture(user)
        cost_time = (datetime.now() - now).total_seconds()
        # @TODO: remove cost_time
        resp = GetAIMealResponseMsg(data, cost_time)
        bubble_container = FlexBubble()
        bubble_container = bubble_container.from_dict(resp)
        line_bot_api.reply_message_with_http_info(
        ReplyMessageRequest(
            reply_token=event.reply_token, messages=[FlexMessage(
                alt_text="ai meal response",
                contents=bubble_container)]
        ))
        

@handler.add(PostbackEvent)
def handle_postback(event):
    with ApiClient(configuration) as api_client:
        # here will handle multiple situation.
        # 1. set which meal that user want to analysis
        # 2. check the meal description is correct or not
        # 3. send meal option message to user
        # 4. check basic user information for the first tiem
        # 5. get daily report
        # 6. get a meal report with specific time range
        # 7. get a calendar to select for meal report
        line_bot_api = MessagingApi(api_client)
        user = event.source.user_id
        postback_data = event.postback.data
        q = parse_qs(postback_data)
        act_list = q["action"]
        if len(act_list) == 0:
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token, messages=[TextMessage(text="unknown action")]))
            return
        action = act_list[0]
        user_info = getUserInfo(user)
        if user_info is None and action != "check_basic_info":
            addUserProcess(line_bot_api, user, event)
            return
        match action:
            case "set_meal":
                meal = Meal(int(q["data"][0]))
                cache.setMeal(user, meal)
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token, messages=[TextMessage(text=f'請輸入{meal.getChinese()}餐點名稱')]))
                return
            case "check_descript":
                if q["data"][0] == "y":
                    meal = cache.getMeal(user)
                    des = cache.getMealDescription(user)
                    msg = GetUploadMsg([("餐點", meal.getChinese()), ("名稱", des)])
                    bubble_container = FlexBubble()
                    bubble_container = bubble_container.from_dict(msg)
                    line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token, messages=[FlexMessage(
                            alt_text="upload img",
                            contents=bubble_container)]
                    ))
                else:
                    cache.deleteMeal(user)
                    cache.deleteMealDescription(user)
                    bubble_container = FlexBubble()
                    bubble_container = bubble_container.from_dict(GetSetMealMsg())
                    line_bot_api.reply_message_with_http_info(
                        ReplyMessageRequest(
                            reply_token=event.reply_token, messages=[FlexMessage(
                                alt_text="set description",
                                contents=bubble_container)]
                        ))
                return
            case "set_description":
                bubble_container = FlexBubble()
                bubble_container = bubble_container.from_dict(GetSetMealMsg())
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token, messages=[FlexMessage(
                            alt_text="set description",
                            contents=bubble_container)]
                    ))
                return
            case "check_basic_info":
                if q["data"][0] == "y":
                    userInfo = User(
                      line_id = user,
                      height = cache.getHeight(user),
                      weight = cache.getWeight(user),
                      age = cache.getAge(user),
                      gender = cache.getGender(user).value
                    )
                    user_table.AddUser(userInfo)
                    removeRegisterProcess(user)
                    line_bot_api.reply_message_with_http_info(
                        ReplyMessageRequest(
                            reply_token=event.reply_token,
                            messages=[TextMessage(text="註冊成功! 歡迎使用營養師機器人")]))
                else:
                    removeRegisterProcess(user)
                    addUserProcess(line_bot_api, user, event)
                return
            case "daily_report":
                today = datetime.now().date()
                tomorrow = today + timedelta(days=1)
                start = datetime.combine(today, time.min)
                end = datetime.combine(tomorrow, time.min)
                data = history_table.GetHistory(user, start, end)
                # @TODO: format message with ai response
                resp = json.dumps(data, default=str)
                line_bot_api.reply_message_with_http_info( 
                  ReplyMessageRequest( 
                    reply_token=event.reply_token, messages=[TextMessage(text=resp)]))
                return
            case "join_us":
                # @TODO: Rename 
                today = datetime.now().date()
                bubble_container = FlexBubble()
                bubble_container = bubble_container.from_dict(GetMonthMsg(today, today, "set_report_start"))
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token, messages=[FlexMessage(
                            alt_text="set report start",
                            contents=bubble_container)]
                    ))
                return
            case "get_month":
                today = datetime.now().date()
                data_list = q["data"]
                give = datetime.strptime(f'{data_list[0]}-01', "%Y-%m-%d")
                # date_str = data_list[0].split("-")
                act = data_list[1]
                if act not in ["set_report_start", "set_report_end"]:
                    line_bot_api.reply_message_with_http_info(
                        ReplyMessageRequest(
                            reply_token=event.reply_token, messages=[TextMessage(text="unknown action")]))
                    return
                alt_text = ""
                if act == "set_report_start":
                    alt_text = "set report start"
                else:
                    alt_text = "set report end"
                start_date_str = cache.getStartReport(user)
                if start_date_str is None:
                    start_date = today
                else:
                    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
                bubble_container = FlexBubble()
                bubble_container = bubble_container.from_dict(GetMonthMsg(give.date(), start_date, act))
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token, messages=[FlexMessage(
                            alt_text=alt_text,
                            contents=bubble_container)]
                    ))
                return
            case "set_report_start":
                today = datetime.now().date()
                data_list = q["data"]
                date_str = data_list[0]
                cache.setStartReport(user, date_str)
                start_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                bubble_container = FlexBubble()
                bubble_container = bubble_container.from_dict(GetMonthMsg(start_date, start_date, "set_report_end"))
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token, messages=[FlexMessage(
                            alt_text="set report end",
                            contents=bubble_container)]
                    ))
                return
            case "set_report_end":
                data_list = q["data"]
                date_str = data_list[0]
                start_date_str = cache.getStartReport(user)
                if start_date_str is None:
                    today = datetime.now().date()
                    bubble_container = FlexBubble()
                    bubble_container = bubble_container.from_dict(GetMonthMsg(today, today, "set_report_start"))
                    line_bot_api.reply_message_with_http_info(
                        ReplyMessageRequest(
                            reply_token=event.reply_token, messages=[FlexMessage(
                                alt_text="set report start",
                                contents=bubble_container)]
                        ))
                    return
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
                end_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                if end_date < start_date:
                    line_bot_api.reply_message_with_http_info(
                        ReplyMessageRequest(
                            reply_token=event.reply_token, messages=[TextMessage(text="結束日期不可小於開始日期，請重新設定")]))
                    return
                start = datetime.combine(start_date, time.min)
                end = datetime.combine(end_date, time.min)
                data = history_table.GetHistory(user, start, end)
                cache.deleteStartReport(user)
                # @TODO: format message with ai response
                resp = json.dumps(data, default=str)
                line_bot_api.reply_message_with_http_info( 
                  ReplyMessageRequest( 
                    reply_token=event.reply_token, messages=[TextMessage(text=resp)]))
                return
            case _:
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token, messages=[TextMessage(text="unknown action")]))
                return
                
def getUserInfo(userId: str) -> User:
    result = user_table.GetUserInfo(userId)
    if len(result) == 0:
        return None
    return result[0]

def addUserProcess(line_bot_api: MessagingApi, userId: str, event):
    if cache.getRegisterProcess(userId) is None:
        cache.setRegisterProcess(userId, True)
        line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token, 
                    messages=[TextMessage(text="歡迎使用營養師機器人，請依序輸入您的身高(公分)、體重(公斤)、年齡、性別(男/女)以完成註冊\n\n請輸入身高(公分) ex. 175.5")]))
        return
    else:
        if cache.getHeight(userId) is None:
            try:
                height = float(event.message.text)
                cache.setHeight(userId, height)
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token, 
                        messages=[TextMessage(text="請輸入體重(公斤) ex. 70.5")]))
                return
            except:
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token, 
                        messages=[TextMessage(text="身高格式錯誤，請重新輸入 ex. 175.5")]))
                return
        if cache.getWeight(userId) is None:
            try:
                weight = float(event.message.text)
                cache.setWeight(userId, weight)
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token, 
                        messages=[TextMessage(text="請輸入年齡 ex. 25")]))
                return
            except:
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token, 
                        messages=[TextMessage(text="體重格式錯誤，請重新輸入 ex. 70.5")]))
                return
        if cache.getAge(userId) is None:
            try:
                age = int(event.message.text)
                cache.setAge(userId, age)
                # @TODO: use flex message
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token, 
                        messages=[TextMessage(text="請輸入性別(男/女)")]))
                return
            except:
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token, 
                        messages=[TextMessage(text="年齡格式錯誤，請重新輸入 ex. 25")]))
                return
        if cache.getGender(userId) is None:
            # @TODO: use flex message
            if event.message.text.strip() == "男":
                cache.setGender(userId, Gender.MALE)
            elif event.message.text.strip() == "女":
                cache.setGender(userId, Gender.FEMALE)
            else:
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text="性別格式錯誤，請重新輸入(男/女)")]))
                return
            msg = GetCheckMsg(
                "基本資料", 
                [
                    ("性別", cache.getGender(userId).getChinese()), 
                    ("身高", str(cache.getHeight(userId)) + " 公分"), 
                    ("體重", str(cache.getWeight(userId)) + " 公斤"), 
                    ("年齡", str(cache.getAge(userId)) + " 歲")
                ],
                ("action=check_basic_info&data=y","action=check_basic_info&data=n"))
            bubble_container = FlexBubble()
            bubble_container = bubble_container.from_dict(msg)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token, messages=[FlexMessage(
                        alt_text="basic info",
                        contents=bubble_container)]
                ))
    return

def removeRegisterProcess(userId: str):
    cache.deleteRegisterProcess(userId)
    cache.deleteHeight(userId)
    cache.deleteWeight(userId)
    cache.deleteAge(userId)
    cache.deleteGender(userId)
    return
