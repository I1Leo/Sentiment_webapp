from fastapi.testclient import TestClient


def test_make_prediction(client: TestClient) -> None:
    
    test_texts = [
            "my ass still knee-deep in Assassins Creed Odyssey with no way out anytime soon lmao.",
            "FIX IT JESUS ! Please FIX IT ! What In the world is going on here.",
            "Anyone that plays a bad luck albatross deck in hearthstone is a literal cop. Fucking fun police."
    ]
    
    payload = {
        "texts": test_texts
    }

    response = client.post(
        "http://localhost:8001/api/v1/predict",
        json=payload,
    )

    assert response.status_code == 200
    prediction_data = response.json()
    assert prediction_data['predictions'][0] == "Positive"
    assert prediction_data['predictions'][1] == "Negative"
    assert prediction_data['predictions'][2] == "Neutral"
