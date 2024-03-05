from fastapi import FastAPI
import uvicorn
import efbUI
app = FastAPI()

@app.get("/")
def getBlank():
  return {"Hello": "World"}

@app.get("/latest/{simbriefID}")
def fetchRoute(simbriefID):
  return efbUI.main(simbriefID)

if __name__ == "__main__":
  config = uvicorn.Config(app, port=8005, host="0.0.0.0", proxy_headers=True)
  server = uvicorn.Server(config)
  server.run()
