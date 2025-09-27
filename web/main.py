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
import httpx
import uvicorn
from fastapi import FastAPI, Response
from opentelemetry.propagate import inject
from utils import PrometheusMiddleware, metrics, setting_otlp
import os
import logging

# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

APP_NAME = os.environ.get("APP_NAME", "app")
EXPOSE_PORT = os.environ.get("EXPOSE_PORT", 8000)
OTLP_GRPC_ENDPOINT = os.environ.get("OTLP_GRPC_ENDPOINT", "tempo:4317")


from worker import create_task, terminate_task

app = FastAPI()

# Setting metrics middleware
app.add_middleware(PrometheusMiddleware, app_name=APP_NAME)
app.add_route("/metrics", metrics)

# Setting OpenTelemetry exporter
setting_otlp(app, APP_NAME, OTLP_GRPC_ENDPOINT)

class EndpointFilter(logging.Filter):
    # Uvicorn endpoint access log filter
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("GET /metrics") == -1


# Filter out /endpoint
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())

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
    logging.info("health 2")
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
    logging.info("submit_task")
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
    
if __name__ == "__main__":
    # update uvicorn access logger format
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"][
        "fmt"
    ] = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
    uvicorn.run("main:app", host="0.0.0.0", port=EXPOSE_PORT, reload=True, log_config=log_config)