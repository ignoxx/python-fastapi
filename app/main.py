from fastapi import FastAPI

from app.routers import cart, item

app = FastAPI()


app.include_router(cart.router)
app.include_router(item.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
