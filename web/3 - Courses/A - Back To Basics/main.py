from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get('/')
async def index():
    return {
        'msg': "Hello world"
    }

if __name__ == '__main__':
    uvicorn.run(app)
