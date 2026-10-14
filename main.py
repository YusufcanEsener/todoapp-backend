from fastapi import FastAPI, HTTPException,status
from pydantic import BaseModel,Field

app=FastAPI(title="Pydantic Doğrulama")

fake_todos=[]

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=50, description="Todo başlığı")
    description: str | None = Field(default="None", max_length=200, description="İsteğe bağlı detay")
    is_completed: bool = Field(default=False)
    
@app.post("/todos",status_code=status.HTTP_201_CREATED,tags=["Todos"])
def create_todo(todo_in:TodoCreate):
    new_id=len(fake_todos)+1
    new_todo={
        "id":new_id,
        "title":todo_in.title,
        "description":todo_in.description,
        "is_completed":todo_in.is_completed
    }
    fake_todos.append(new_todo)
    return new_todo

@app.get("/todos/{todo_id}",tags=["Todos"])
def get_single_todo(todo_id:int):
    for todo in fake_todos:
        if todo["id"]==todo_id:
            return {"data":todo}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{todo_id} numaralı Todo kaydı bulunamadı."
    )
