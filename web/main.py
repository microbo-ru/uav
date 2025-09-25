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
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from worker import create_task, terminate_task

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

@app.post("/task", status_code=201, responses={
    201: {
        "content": {
            "application/json": {
                "example": {"id": "08234f72-29c9-4527-861c-b3d29aabf0e4"}
            }},
        "description": "Return task id"
    },
})
def submit_task(
    xslx_file: UploadFile = File(..., description="*.xlsx file with data"),
):
    logger.info("Root endpoint accessed.")
    file_location = f"./tmp/{xslx_file.filename}"
    with open(file_location, "wb") as f:
        f.write(xslx_file.file.read())

    task = create_task.delay(file_location)

    return JSONResponse({"id": task.id, "status": task.status}, status_code=201)

@app.get("/task/{id}/status", responses={
    200: {
        "content": {
            "application/json": {
                "example": {
                    "id": "cc6b3345-4207-4ebc-94a2-0c8f03d08bb3",
                    "status": "FAILURE"
                    }
            }},
        "description": "Return task id and current status"
    },
    404: {
        "description": "Task with provided id not found"
    }
})
def get_task_status(id):
    try:
        task_result = AsyncResult(id)

        result = {
            "id": id,
            "status": task_result.status,
            "result": task_result.result
        }
        return JSONResponse(result)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=404, content={"message": "Not Found"})