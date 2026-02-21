from fastapi import FastAPI

app = FastAPI()

# Simple GET route
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# GET route with parameter
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

# POST route
@app.post("/items/")
def create_item(name: str, price: float):
    return {"name": name, "price": price}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
