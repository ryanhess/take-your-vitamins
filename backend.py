from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.post("/")
async def make_viamin_schedule(suppliment_data: dict):
    print(suppliment_data)
    raise HTTPException(status_code=500, detail="test error response")
