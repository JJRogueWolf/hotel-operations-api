from fastapi.responses import JSONResponse
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi.security import OAuth2PasswordRequestForm
from auth import authenticate_user, create_access_token, get_current_user
import logging

from database import get_db
from models import Issue
from schemas import IssueCreate, IssueResponse, IssueListResponse

app = FastAPI()

logger = logging.getLogger(__name__)

@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request, exc):
    logger.exception("Database operation failed", exc_info= exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "A database error occurred"}
    )
    
@app.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not authenticate_user(
        form_data.username,
        form_data.password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(form_data.username)

    return {
        "access_token": token,
        "token_type": "bearer",
    }

@app.get("/issues", response_model=IssueListResponse, dependencies=[Depends(get_current_user)],)
def get_issues(db: Session = Depends(get_db)):
    statement = select(Issue)
    issues = db.scalars(statement).all()
    return {"issues": issues}
    
@app.post("/issues", status_code=201, response_model=IssueResponse, dependencies=[Depends(get_current_user)],)
def create_issue(issue: IssueCreate, db: Session = Depends(get_db)):
    new_issue = Issue(
        room=issue.room,
        description=issue.description,
        status="Open"
    )
    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)
    
    return new_issue
    
@app.patch("/issues/{issue_id}", dependencies=[Depends(get_current_user)],)
def close_issue(issue_id: int, db: Session = Depends(get_db)):
    issue = db.get(Issue, issue_id)
    if issue is None:
        raise HTTPException(
            status_code=404,
            detail=f"No issue found with ID #{issue_id}"
        )
    issue.status = "Closed"
    db.commit()
    
    return {"message": f"Issue ID #{issue_id} is now closed"}

@app.get("/issues/{issue_id}", response_model=IssueResponse, dependencies=[Depends(get_current_user)],)
def get_issue(issue_id: int, db: Session = Depends(get_db)):
    issue = db.get(Issue, issue_id)
    if issue is None:
        raise HTTPException(
            status_code=404,
            detail=f"No issue found with ID #{issue_id}"
        )
    return issue

@app.delete("/issues/{issue_id}", dependencies=[Depends(get_current_user)],)
def delete_issue(issue_id: int, db: Session = Depends(get_db)):
    issue = db.get(Issue, issue_id)
    if issue is None:
        raise HTTPException(
            status_code=404,
            detail=f"No issue found with ID #{issue_id}!"
        )
    db.delete(issue)
    db.commit()
    return {"message": f"Issue ID #{issue_id} has been deleted!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}