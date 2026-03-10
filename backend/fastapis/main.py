############# basic fast api set up

from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#####################################################


# http://127.0.0.1:8000/api/yusuff
@app.get("/yusuff")
def read_root():
    return {"message": "FastAPI working"}