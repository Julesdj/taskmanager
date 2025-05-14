from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(title="Task manager APi")
    return app


app = create_app()
