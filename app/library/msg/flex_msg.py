from typing import Dict, List, Tuple
from datetime import datetime, date, timedelta
from app.library.storage.models import History

def GetCheckMsg(title: str, vars: List[Tuple[str, str]], actions: Tuple[str, str] ) -> Dict:
    check_msg = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": "https://developers-resource.landpress.line.me/fx/img/01_1_cafe.png",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "action": {
                "type": "uri",
                "uri": "https://line.me/"
            }
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": f'{title}',
                    "weight": "bold",
                    "size": "xl"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": []
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "height": "sm",
                    "action": {
                        "type": "postback",
                        "label": "正確",
                        "data": f'{actions[0]}'
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "postback",
                        "label": "錯誤",
                        "data": f'{actions[1]}'
                    }
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "margin": "sm"
                }
            ],
            "flex": 0
        }
    }

    for var in vars:
        item = {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
                {
                    "type": "text",
                    "text": f'{var[0]}',
                    "color": "#aaaaaa",
                    "size": "sm",
                    "flex": 1
                },
                {
                    "type": "text",
                    "text": f'{var[1]}',
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5
                }
            ]
        }
        check_msg['body']['contents'][1]['contents'].append(item)
    return check_msg

def GetUploadMsg(vars: List[Tuple[str, str]]) -> Dict:
    upload_img = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": "https://developers-resource.landpress.line.me/fx/img/01_1_cafe.png",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "action": {
                "type": "uri",
                "uri": "https://line.me/"
            }
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "上傳餐點",
                    "weight": "bold",
                    "size": "xl"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": []
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": "開啟相機",
                        "uri": "https://line.me/R/nv/camera/"
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": "選擇圖片",
                        "uri": "https://line.me/R/nv/cameraRoll/single"
                    }
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "margin": "sm"
                }
            ],
            "flex": 0
        }
    }
    for var in vars:
        item = {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
                {
                    "type": "text",
                    "text": f'{var[0]}',
                    "color": "#aaaaaa",
                    "size": "sm",
                    "flex": 1
                },
                {
                    "type": "text",
                    "text": f'{var[1]}',
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5
                }
            ]
        }
        upload_img['body']['contents'][1]['contents'].append(item)
    return upload_img

def GetSetMealMsg():
    meals = [("早餐","1"), ("午餐","2"), ("晚餐","3"), ("點心","4")]
    set_description = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "設定餐點",
                    "weight": "bold",
                    "size": "xl"
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [],
            "flex": 0
        }
    }
    for meal in meals:
        item = {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
                "type": "postback",
                "label": f'{meal[0]}',
                "data": f'action=set_meal&data={meal[1]}',
            }
        }
        set_description['footer']['contents'].append(item)
    return set_description

def GetMonthMsg(input_date: date, start_date: date, act: str) -> Dict:
    today = datetime.now().date()
    year = input_date.year
    month = input_date.month
    if act == "set_report_start":
        header = "設定開始日期"
    else:
        header = "設定結束日期"
    month_msg = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "text",
                    "text": f'{header}',
                    "weight": "bold",
                    "size": "xl",
                    "align": "center",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": f'{year} 年 {month} 月',
                    "weight": "bold",
                    "size": "xl",
                    "align": "center",
                    "margin": "md"
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "text",
                            "text": "Su",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 1,
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": "Mo",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 1,
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": "Tu",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 1,
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": "We",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 1,
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": "Th",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 1,
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": "Fr",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 1,
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": "Sa",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 1,
                            "align": "center"
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "md",
                    "contents": [],
                },
            ]
        },
        "footer": {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [],
            "flex": 1
        }
    }
    first_day_of_month = date(year, month, 1)
    # caculate the first day of next month
    if month == 12:
        first_day_of_next_month = date(year + 1, 1, 1)
    else:
        first_day_of_next_month = date(year, month + 1, 1)
    # get the number of days in the month
    num_days_by_datetime = (first_day_of_next_month - first_day_of_month).days
    idx = 0
    layer = 4
    for i in range(first_day_of_month.weekday()+1):
        idx += 1
        month_msg['body']['contents'][layer]['contents'].append({
            "type": "text",
            "text": " ",
            "size": "sm",
            "flex": 1,
            "align": "center"
        })
    for i in range(num_days_by_datetime):
        if idx > 6:
            idx = 0
            layer += 1
            month_msg['body']['contents'].append({
                "type": "box",
                "layout": "horizontal",
                "margin": "md",
                "contents": [],
            })
        if (date(year, month, i+1) == today and today == start_date) or (date(year, month, i+1) == start_date and today != start_date):
            month_msg['body']['contents'][layer]['contents'].append({
                "type": "box",
                "layout": "vertical",
                "flex": 1,
                "alignItems": "center",
                "justifyContent": "center",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "height": "30px",
                        "width": "30px",
                        "cornerRadius": "100px",
                        "backgroundColor": "#00B900",
                        "alignItems": "center",
                        "justifyContent": "center",
                        "contents": [
                            {
                                "type": "text",
                                "text": f'{i+1}',
                                "size": "sm",
                                "color": "#ffffff",
                                "align": "center",
                                "gravity": "center",
                                "weight": "bold",
                                "action": {
                                    "type": "postback",
                                    "label": "set date",
                                    "data": f'action={act}&data={year}-{month}-{i+1}',
                                }
                            }
                        ]
                    }
                ]
            })
        elif (date(year, month, i+1) > today) or (today - date(year, month, i+1) > timedelta(days=90)):
            month_msg['body']['contents'][layer]['contents'].append({
                "type": "text",
                "text": f'{i+1}',
                "size": "sm",
                "flex": 1,
                "align": "center",
                "gravity": "center",
                "color": "#C6C6C6"
            })
        else:
            month_msg['body']['contents'][layer]['contents'].append({
                "type": "text",
                "text": f'{i+1}',
                "size": "sm",
                "flex": 1,
                "align": "center",
                "gravity": "center",
                "action": {
                    "type": "postback",
                    "label": "set date",
                    "data": f'action={act}&data={year}-{month}-{i+1}',
                }
            })
        idx += 1
    for idx in range(idx, 7):
        month_msg['body']['contents'][layer]['contents'].append({
            "type": "text",
            "text": " ",
            "size": "sm",
            "flex": 1,
            "align": "center"
        })
    if today - input_date <= timedelta(days=90):
        month_msg['footer']['contents'].append({
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
                "type": "postback",
                "label": "上個月",
                "data": f'action=get_month&data={year if month > 1 else year - 1}-{month - 1 if month > 1 else 12}&data={act}',
            }
        })
    else:
        month_msg['footer']['contents'].append({
            "type": "text",
            "text": " ",
            "size": "sm",
            "flex": 1,
            "align": "center"
        })
    if today.month != input_date.month:
        month_msg['footer']['contents'].append({
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
                "type": "postback",
                "label": "下個月",
                "data": f'action=get_month&data={year if month < 12 else year + 1}-{month + 1 if month < 12 else 1}&data={act}',
            }
        })
    else:
        month_msg['footer']['contents'].append({
            "type": "text",
            "text": " ",
            "size": "sm",
            "flex": 1,
            "align": "center"
        })
    return month_msg

def GetAIMealResponseMsg(response: History, cost) -> Dict:
    ai_response = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "營養評估與建議",
                    "weight": "bold",
                    "color": "#1DB446",
                    "size": "sm"
                },
                {
                    "type": "text",
                    "text": f"{response.description}",
                    "weight": "bold",
                    "size": "lg",
                    "margin": "md",
                    "wrap": True
                },
                {
                    "type": "separator",
                    "margin": "xxl"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "xxl",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "卡路里(kcal)",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": f"{response.calories_kcal if response.calories_kcal else 0}",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "蛋白質(g)",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": f"{response.protein_g if response.protein_g else 0}",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "碳水化合物(g)",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": f"{response.carbs_g if response.carbs_g else 0}",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "脂肪(g)",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": f"{response.fat_g if response.fat_g else 0}",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "鈉(mg)",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": f"{response.sodium_mg if response.sodium_mg else 0}",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        },
                        {
                            "type": "separator",
                            "margin": "xxl"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "簡單描述",
                                            "size": "md",
                                            "flex": 0,
                                            "margin": "none",
                                            "weight": "bold",
                                            "color": "#1DB446"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": f"{response.ai_description if response.ai_description else '無'}",
                                            "margin": "md",
                                            "size": "sm",
                                            "wrap": True
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "type": "separator",
                            "margin": "xxl"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "建議",
                                            "size": "md",
                                            "flex": 0,
                                            "margin": "none",
                                            "weight": "bold",
                                            "color": "#1DB446"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": f"{response.ai_suggest if response.ai_suggest else '無'}",
                                            "margin": "md",
                                            "size": "sm",
                                            "wrap": True
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "separator",
                    "margin": "xxl"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": "分析時間(s)",
                            "size": "xs",
                            "color": "#aaaaaa",
                            "flex": 0
                        },
                        {
                            "type": "text",
                            "text": f"{cost} s",
                            "color": "#aaaaaa",
                            "size": "xs",
                            "align": "end"
                        }
                    ]
                }
            ]
        },
        "styles": {
            "footer": {
                "separator": True
            }
        }
    }
    return ai_response
