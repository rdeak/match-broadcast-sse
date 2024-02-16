const composeServerSideEventListener = () => {
    let eventSource = null;

    const connect = (url, onMessage) =>{
        eventSource = new EventSource(url);

        eventSource.onmessage = onMessage;

        eventSource.addEventListener("started", onMessage);
        eventSource.addEventListener("halftime", onMessage);
        eventSource.addEventListener("finished", event => {
            onMessage(event);
            eventSource.close();
        });
    }

    const disconnect = () => {
        eventSource?.close();
    }

    return {
        connect, disconnect
    }
}
const serverSideEventListener = composeServerSideEventListener()

const processMessage = (messageEvent) => {
    console.log("New event:", messageEvent.data);
    document.getElementById("events").innerHTML += messageEvent.data + "<br>";
}


export function init(url){
    const maybeConnectButton = document.querySelector("#connect");
    maybeConnectButton?.addEventListener("click", ()=>{
        document.getElementById("events").innerHTML = "";
        serverSideEventListener.connect( url, processMessage);
    });

    const maybeCloseButton = document.querySelector("#disconnect");
    maybeCloseButton?.addEventListener("click", serverSideEventListener.disconnect);

}