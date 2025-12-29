from fastapi import APIRouter, Request
from app.services.mr_service import handle_merge_request

router = APIRouter(prefix="/webhooks", tags=["gitlab"])

@router.post("/gitlab")
async def gitlab_webhook(request: Request):
    payload = await request.json()

    if payload.get("object_kind") == "merge_request":
        handle_merge_request(payload, post_comment=True)
        return {"status": "processed"}

    return {"status": "ignored"}
