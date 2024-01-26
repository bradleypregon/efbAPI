from fastapi import FastAPI
# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
import uvicorn
import efbUI
# import ssl

# https://medium.com/@mariovanrooij/adding-https-to-fastapi-ad5e0f9e084e
# openssl req -x509 -out localhost.crt -keyout localhost.key -newkey rsa:2048 -nodes -sha256 -subj '/CN=localhost' -days 364
# key = "ssl/localhost.key"
# cert = "ssl/localhost.crt"
app = FastAPI()

#app.add_middleware(HTTPSRedirectMiddleware)

@app.get("/")
def getBlank():
  return {"Hello": "World"}

@app.get("/latest/{simbriefID}")
def fetchRoute(simbriefID):
  return efbUI.main(simbriefID)

if __name__ == "__main__":
  # config = uvicorn.Config(app, port=8005, host="0.0.0.0", ssl_keyfile=key, ssl_certfile=cert)
  config = uvicorn.Config(app, port=8005, host="0.0.0.0", proxy_headers=True)
  server = uvicorn.Server(config)
  server.run()
