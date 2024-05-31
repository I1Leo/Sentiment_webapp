from typing import Any, List

from fastapi import APIRouter
from pydantic import BaseModel
from sentiment_model.predict import predict

api_router = APIRouter()


class PredictionRequest(BaseModel):
    texts: List[str]


class PredictionResponse(BaseModel):
    predictions: List[str]


@api_router.post("/predict", response_model=PredictionResponse)
async def get_predictions(request: PredictionRequest) -> Any:
    texts = request.texts
    preds = predict(texts)
    return PredictionResponse(predictions=preds)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(api_router, host="localhost", port=8001)
