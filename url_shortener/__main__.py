import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_responses import custom_openapi
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from url_shortener.routers import router as main_router
from url_shortener.tools.logs import configure_logger, get_uvicorn_log_config

app = FastAPI()
app.openapi = custom_openapi(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)


def main():
    load_dotenv()
    configure_logger()
    logger.info("Starting...")

    app.include_router(main_router)

    uvicorn.run(
        "url_shortener.__main__:app",
        log_config=get_uvicorn_log_config(),
        host="0.0.0.0",
    )


if __name__ == "__main__":
    main()
