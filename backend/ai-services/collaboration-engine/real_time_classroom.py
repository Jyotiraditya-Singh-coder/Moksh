import asyncio
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer, MediaRelay
import json

# WebRTC signaling (simplified)
class WebRTCManager:
    def __init__(self):
        self.pcs = set()

    async def offer(self, sdp, type):
        pc = RTCPeerConnection()
        self.pcs.add(pc)

        @pc.on("iceconnectionstatechange")
        async def on_iceconnectionstatechange():
            if pc.iceConnectionState == "failed":
                await pc.close()
                self.pcs.discard(pc)

        await pc.setRemoteDescription(RTCSessionDescription(sdp, type))
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)
        return {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}

# For signaling, we use socket.io (handled in main app)