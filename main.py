from fastapi.responses import JSONResponse
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

import psycopg
from database import get_db
from schemas import IssueCreate, IssueResponse, IssueListResponse
from models import Issue

app = FastAPI()

@app.exception_handler(psycopg.Error)
async def database_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "A database error occurred"}
    )

@app.get("/issues", response_model=IssueListResponse)
def get_issues(db: Session = Depends(get_db)):
    statement = select(Issue)
    issues = db.scalars(statement).all()
    return {"issues": issues}
    
@app.post("/issues", status_code=201, response_model=IssueResponse)
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
    
@app.patch("/issues/{issue_id}")
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

@app.get("/issues/{issue_id}", response_model=IssueResponse)
def get_issue(issue_id: int, db: Session = Depends(get_db)):
    issue = db.get(Issue, issue_id)
    if issue is None:
        raise HTTPException(
            status_code=404,
            detail=f"No issue found with ID #{issue_id}"
        )
    return issue

@app.delete("/issues/{issue_id}")
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