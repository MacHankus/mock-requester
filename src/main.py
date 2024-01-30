import uvicorn
from loguru import logger

from app import APP_FROZEN
from app import app
from definitions import PROJECT_NAME
from settings import settings

if __name__ == "__main__":
    logger.info(PROJECT_NAME)
    uvicorn.run(
        app if APP_FROZEN else "app:app",
        host="0.0.0.0",
        port=int(settings.API_PORT),
        reload=not APP_FROZEN,
        access_log=False,
    )
