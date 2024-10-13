from fastapi import FastAPI
from app.controllers.paymentController import router as paymentController
app = FastAPI()

app.include_router(paymentController, prefix="/api/payment")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)