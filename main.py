from fastapi import FastAPI

app=FastAPI(title="Rolio backend")

@app.get("/")
def root():
    return "bidhan"