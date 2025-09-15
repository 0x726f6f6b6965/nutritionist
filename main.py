from app import api
import uvicorn
# from sqlalchemy import create_engine
# from app.library.storage.operation.history import DietHistory
# from app.library.storage.models import History
# from datetime import datetime, time

# for debug
if __name__ == '__main__':
    # engine = create_engine("postgresql://postgres:docker@127.0.0.1:5432/postgres", echo=True)
    # aa = datetime.now().date()

    # c = DietHistory(engine)
    # a = c.GetDailyHistory(1)
    # print(a)
    # c.AddHistory(History(user_id=1, meal=1, ai_cal=100))
    # aa = c.GetDailyHistory(1)
    # print(aa)
    uvicorn.run(api, host="0.0.0.0", port=8080)