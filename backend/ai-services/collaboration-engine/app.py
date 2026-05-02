from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import List
import socketio
from group_formation import form_study_groups
from emotion_detector import detect_emotion
import logging

app = FastAPI()
sio = socketio.AsyncServer(async_mode='asgi')
socket_app = socketio.ASGIApp(sio, app)

class GroupRequest(BaseModel):
    student_ids: List[str]
    skill_vectors: List[List[float]]

class EmotionRequest(BaseModel):
    audio_base64: str

@app.post("/form-groups")
async def form_groups(req: GroupRequest):
    students = [{"id": sid, "skills": vec} for sid, vec in zip(req.student_ids, req.skill_vectors)]
    groups = form_study_groups(students)
    return {"groups": groups}

@app.post("/detect-emotion")
async def detect_emotion_endpoint(req: EmotionRequest):
    emotion = detect_emotion(req.audio_base64)
    return {"emotion": emotion}

# WebSocket for real-time collaboration (whiteboard sync)
active_rooms = {}

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def join_room(sid, data):
    room = data['room']
    sio.enter_room(sid, room)
    active_rooms[room] = active_rooms.get(room, set())
    active_rooms[room].add(sid)
    await sio.emit('user_joined', {'sid': sid}, room=room)

@sio.event
async def whiteboard_update(sid, data):
    room = data['room']
    await sio.emit('whiteboard_update', data['canvas_data'], room=room, skip_sid=sid)

@sio.event
async def disconnect(sid):
    for room, members in active_rooms.items():
        if sid in members:
            members.remove(sid)
            await sio.emit('user_left', {'sid': sid}, room=room)
    print(f"Client disconnected: {sid}")

app.mount("/", socket_app)