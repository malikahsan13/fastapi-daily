from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()


@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    try:
        # Make a GET request to the JSONPlaceholder API
        response = requests.get(
            f"https://jsonplaceholder.typicode.com/posts/{post_id}")

        # check if the request was successful
        if response.status_code == 200:

            return response.json()
        else:
            raise HTTPException(
                status_code=response.status_code, detail="API Call failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
