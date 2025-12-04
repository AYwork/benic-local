from fastapi import FastAPI
from kiki_local.parent.parent_agent import run_kiki_orchestrator
from pydantic import BaseModel

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

        return {"response": result.raw}

    except Exception as e:
        return {"error": str(e)}
