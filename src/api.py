from fastapi import FastAPI
import uvicorn
import SBCleaner
app = FastAPI()

@app.get("/")
def getBlank():
  return {"Hello": "World"}

@app.get("/latest/{sbID}")
def fetchRoute(sbID):
  return SBCleaner.main(sbID)

if __name__ == "__main__":
  config = uvicorn.Config(app, port=65010, host="0.0.0.0")
  server = uvicorn.Server(config)
  server.run()
