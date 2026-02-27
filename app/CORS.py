from fastapi import FastAPI

# import the CORS Middleware class from fastapi.middleware.cors

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "https://example.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origin=origins,
    allow_credentials=True,   # it should include credentials such as cookie or authorization header
    allow_methods=["GET","POST","PUT","DELETE"],
    allow_headers=["Authorization", "Content-Type"]
)

#allow_methods=[*]
#allow_headers=[*]