from fastapi import FastAPI
from app.database import engine, Base
from app.routers import todos

app = FastAPI(title="Todo App")

@app.on_event("startup")
def init_db():
    Base.metadata.create_all(bind=engine)

app.include_router(todos.router)

@app.get("/")
def root():
    return {"message": "Todo App API"}