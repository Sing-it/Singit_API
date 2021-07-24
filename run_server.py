import uvicorn
from app.core.config import settings


def main():

    HOST: str = settings.SERVER_HOST
    PORT: int = settings.SERVER_PORT
    MODE: bool = (
        settings.MODE  # True: on development(reload True), False: on Production(reload False)
    )

    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=MODE)


if __name__ == "__main__":
    main()
