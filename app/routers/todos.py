from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app import models, schemas
from app.database import SessionLocal

router = APIRouter(prefix="/todos", tags=["todos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.TodoResponse)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    db_todo = models.Todo(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@router.get("/", response_model=List[schemas.TodoResponse])
def read_todos(
        sort_by: Optional[str] = Query(None, regex="^(title|status|created_at)$"),
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    query = db.query(models.Todo)

    if sort_by:
        if sort_by == "title":
            query = query.order_by(models.Todo.title)
        elif sort_by == "status":
            query = query.order_by(models.Todo.status)
        elif sort_by == "created_at":
            query = query.order_by(models.Todo.created_at)

    return query.offset(skip).limit(limit).all()


@router.get("/top/{n}", response_model=List[schemas.TodoResponse])
def get_top_priority(n: int, db: Session = Depends(get_db)):
    return db.query(models.Todo).order_by(models.Todo.priority.desc()).limit(n).all()


@router.get("/search/", response_model=List[schemas.TodoResponse])
def search_todos(q: str, db: Session = Depends(get_db)):
    todos = db.query(models.Todo).all()
    return [todo for todo in todos if q.lower() in todo.title.lower() or q.lower() in todo.description.lower()]


@router.get("/{todo_id}", response_model=schemas.TodoResponse)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Task not found")
    return todo


@router.put("/{todo_id}", response_model=schemas.TodoResponse)
def update_todo(todo_id: int, todo_update: schemas.TodoUpdate, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = todo_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(todo, field, value)

    db.commit()
    db.refresh(todo)
    return todo


@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(todo)
    db.commit()
    return {"message": "Task deleted successfully"}