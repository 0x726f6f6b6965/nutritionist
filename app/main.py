from fastapi import FastAPI, Request, HTTPException
from linebot.v3.exceptions import InvalidSignatureError
from app.controller import handler
import logging
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

api = FastAPI()

@api.get("/")
async def root():
    return {"message": "Hello World"}

@api.post("/callback")
async def callback(request: Request):
        logger.info(f"Incoming Request: {request.method} {request.url}")
        logger.info(f"Incoming Request Headers: {dict(request.headers)}")
        signature = request.headers.get("X-Line-Signature", "")
        logger.info(f"Incoming Request Signature: {signature}")
        body = await request.body()
        try:
            handler.handle(body.decode("utf-8"), signature)
        except InvalidSignatureError:
            raise HTTPException(status_code=400, detail="Invalid signature")
        except  Exception as e:
            logging.error("Error: " + str(e))
            raise HTTPException(status_code=500, detail="Internal server error")
        return 'OK'
