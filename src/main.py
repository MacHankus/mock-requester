import uvicorn
from art import text2art
from loguru import logger

from app import APP_FROZEN
from app import app
from definitions import PROJECT_NAME
from settings import settings

if __name__ == "__main__":
    logger.info("\n" + text2art(PROJECT_NAME))
    logger.info(PROJECT_NAME)
    uvicorn.run(
        app if APP_FROZEN else "app:app",
        host="0.0.0.0",
        port=int(settings.API_PORT),
        reload=not APP_FROZEN,
        access_log=False,
    )
