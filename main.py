from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class WebhookRequest(BaseModel):
    responseId: str
    session: str
    queryResult: dict

def handle_order_add(session_id: str, parameters: dict):
    # Your logic for handling order.add intent
    # Extract parameters from the parameters dictionary as needed
    return {"fulfillmentText": "Order added successfully"}

def handle_order_remove(session_id: str, parameters: dict):
    # Your logic for handling order.remove intent
    # Extract parameters from the parameters dictionary as needed
    return {"fulfillmentText": "Order removed successfully"}

@app.post("/webhook")
async def webhook_handler(request: WebhookRequest):
    payload = request.queryResult['queryResult']['intent']['displayName']
    session_id = request.session.split('/')[-1]  # Extracting session ID
    intent_name = request.queryResult['intent']['displayName']

    if intent_name == 'order.add':
        response = handle_order_add(session_id, request.queryResult.get('parameters', {}))
    elif intent_name == 'order.remove':
        response = handle_order_remove(session_id, request.queryResult.get('parameters', {}))
    else:
        raise HTTPException(status_code=400, detail=f"Intent {intent_name} not supported")

    return response
