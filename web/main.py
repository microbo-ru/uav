from celery.result import AsyncResult
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse
from typing import Any, Callable, Set, TypeVar
from fastapi.openapi.utils import generate_operation_id
from fastapi.routing import APIRoute
from pathlib import Path

# from worker import create_task, terminate_task

app = FastAPI()

@app.get('/health', responses={
    200: {
        "content": {
            "application/json": {
                "example": {}
            }},
        "description": "Return health check"
    }
})
def health():
    return JSONResponse({}, status_code=200)