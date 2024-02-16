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

        # EventSource will reconnect automatically if we close the stream
        while True:
            None
    except CancelledError:
        print("Client disconnected.")


@app.get("/events")
async def get_events():
    return StreamingResponse(stream_events(), media_type="text/event-stream")


app.mount("/", StaticFiles(directory="static", html=True), name="static")
