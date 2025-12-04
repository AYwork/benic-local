import re

from fastapi import FastAPI
from pydantic import BaseModel

from kiki_core.parent.parent_agent import run_kiki_orchestrator

app = FastAPI(
    title="kiki API",
    description="CrewAI (Parent) on Azure App Service",
    version="0.1.0",
    openapi_version="3.0.2"
)


class UserRequest(BaseModel):
    query: str


@app.get("/")
def root():
    return {"message": "kiki parent agent is running"}


@app.post("/ask")
def ask_kiki(req: UserRequest):
    """
    Copilot Studio から叩かれるエンドポイント
    """
    try:
        # 親エージェントを起動
        result = run_kiki_orchestrator(req.query)

        raw_text = result.raw
        match = re.search(r"<RESULT>(.*?)</RESULT>", raw_text, re.DOTALL)
        if match:
            final_response = match.group(1).strip()
        else:
            final_response = raw_text

        return {"response": final_response}

    except Exception as e:
        return {"error": str(e)}
