from fastapi import APIRouter, Request

router = APIRouter(prefix="/webhooks", tags=["gitlab"])

@router.post("/gitlab")
async def gitlab_webhook(request: Request):
    payload = await request.json()

    event_type = payload.get("object_kind")

    if event_type == "merge_request":
        print("✅ Merge Request event received")
    else:
        print("ℹ️ Non-MR event received:", event_type)

    return {"status": "received", "event": event_type}
