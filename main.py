from fastapi import FastAPI
from microServicePaymentAPI.app.controllers.paymentController import router as restaurantController
app = FastAPI()

app.include_router(restaurantController, prefix="/api/restaurant")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)