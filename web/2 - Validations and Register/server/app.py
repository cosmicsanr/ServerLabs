from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://127.0.0.1:5000",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:5500"
]

# https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/register')
async def register(player: str):
    return "XPTO"

################################


def main():
    import uvicorn
    from docopt import docopt
    help_doc = """
A web accessible FastAPI server that allow players to register/enroll for tournaments

Usage:
    app.py [-c | -c -d] [-p PORT] [-h HOST_IP]

Options:
    -p PORT, --port=PORT        Listen on this port [default: 8000]
    -c, --create-ddl            Create the models in the database
    -d --populate-db            Populate the DB with dummy for testing purposes
    -h HOST_IP, --host=HOST_IP  Listen on this IP address [default: 127.0.0.1]
    """

    args = docopt(help_doc)
    create_ddl = args['--create-ddl']
    populate_db = args['--populate-db']
    if create_ddl:
        print("Will create ddl")
        if populate_db:
            print("Will also populate the DB")

    uvicorn.run('app:app',
                port=int(args['--port']),
                host=args['--host'],
                reload=True,

                )


if __name__ == '__main__':
    main()
