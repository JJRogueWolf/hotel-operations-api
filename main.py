from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException
import psycopg
from database import get_db_connection
from schemas import IssueCreate, IssueResponse, IssueListResponse

app = FastAPI()

@app.exception_handler(psycopg.Error)
async def database_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "A database error occurred"}
    )

@app.get("/issues", response_model=IssueListResponse)
def get_issues():
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM issues")
        issues = cursor.fetchall()
    return {"issues": issues}
    
@app.post("/issues", status_code=201, response_model=IssueResponse)
def create_issue(issue: IssueCreate):
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO issues (room, description, status) 
            VALUES (%s, %s, %s) 
            RETURNING id, room, description, status
            """,
            (issue.room, issue.description, "Open"))
        new_issue = cursor.fetchone()
        connection.commit()
    
    return new_issue
    
@app.patch("/issues/{issue_id}")
def close_issue(issue_id: int):
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE issues SET status = 'Closed' WHERE id = %s", (issue_id,))
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail=f"No issue found with ID #{issue_id}"
            )
        connection.commit()
    
    return {"message": f"Issue ID #{issue_id} is now closed"}

@app.get("/issues/{issue_id}", response_model=IssueResponse)
def get_issue(issue_id: int):
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM issues WHERE id = %s", (issue_id,))
        issue = cursor.fetchone()
        if issue is None:
            raise HTTPException(
                status_code=404,
                detail=f"No issue found with ID #{issue_id}"
            )
    return issue

@app.delete("/issues/{issue_id}")
def delete_issue(issue_id: int):
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM issues WHERE id = %s", (issue_id,))
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail=f"No issue found with ID #{issue_id}!"
            )
        connection.commit()
    return {"message": f"Issue ID #{issue_id} has been deleted!"}