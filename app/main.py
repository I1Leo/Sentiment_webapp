from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from loguru import logger

from app.api import api_router
from app.config import settings, setup_app_logging

# setup logging as early as possible
setup_app_logging(config=settings)


app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

root_router = APIRouter()


@root_router.get("/")
def index(request: Request) -> HTMLResponse:
    """Basic HTML response with a form to submit text."""
    body = (
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Welcome to the Sentiment model API</h1>"
        "<div style='padding-bottom: 15px'>"
        "Check the docs: <a href='/docs'>here</a>"
        "</div>"
        "<div>"
        "<form id='inputForm'>"
        "<label for='inputText' style='padding-right: 5px;'>Enter text:</label>"
        "<input style='width: 200px; padding: 5px' type='text' id='inputText' name='inputText' required>"
        "<button style='padding: 5px' type='submit'>Submit</button>"
        "</form>"
        "<div id='result'></div>"
        "</div>"
        "<script>"
        "document.getElementById('inputForm').onsubmit = async function(event) {"
        "  event.preventDefault();"
        "  try {"
        "    const text = document.getElementById('inputText').value;"
        "    const response = await fetch('/api/v1/predict', {"
        "      method: 'POST',"
        "      headers: { 'Content-Type': 'application/json' },"
        "      body: JSON.stringify({ texts: [text] })"
        "    });"
        "    if (!response.ok) {"
        "      throw new Error('Network response was not ok');"
        "    }"
        "    const result = await response.json();"
        "    document.getElementById('result').innerText = JSON.stringify(result['predictions'][0]);"
        "  } catch (error) {"
        "    console.error('Error:', error);"
        "    document.getElementById('result').innerText = 'Error: ' + error.message;"
        "  }"
        "};"
        "</script>"
        "</body>"
        "</html>"
    )

    return HTMLResponse(content=body)


app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


if __name__ == "__main__":
    # Use this for debugging purposes only
    logger.warning("Running in development mode. Do not run like this in production.")
    import uvicorn

    uvicorn.run(app, host="localhost", port=8001, log_level="debug")
