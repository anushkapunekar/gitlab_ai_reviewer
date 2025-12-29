from fastapi import APIRouter, Request, HTTPException
from app.services.mr_service import handle_merge_request

router = APIRouter(prefix="/ci", tags=["ci"])

@router.post("/ai-review")
async def ci_ai_review(request: Request):
    payload = await request.json()

    result = handle_merge_request(payload, post_comment=False)
    review_text = result["review"]

    # 🔍 Extract verdict
    if "Verdict: FAIL" in review_text:
        raise HTTPException(
            status_code=400,
            detail="AI Review failed. Merge blocked."
        )

    return {
        "status": "PASS",
        "message": "AI Review passed. Safe to merge."
    }
