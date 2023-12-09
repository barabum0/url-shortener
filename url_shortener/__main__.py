import uvicorn
from fastapi import FastAPI
from url_shortener.routers import router as main_router


def main():
    app = FastAPI()
    app.include_router(main_router)

    uvicorn.run(app)


if __name__ == "__main__":
    main()
