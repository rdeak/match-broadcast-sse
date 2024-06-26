from asyncio import CancelledError

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles

from .watch_for_events import watch_for_events

app = FastAPI()


def stream_events():
    try:
        print("Client connected")
        yield from watch_for_events()
    except CancelledError:
        print("Client disconnected.")


@app.get("/match-events")
async def get_events():
    return StreamingResponse(stream_events(), media_type="text/event-stream")


app.mount("/", StaticFiles(directory="static", html=True), name="static")
