from fastapi import APIRouter
import json
from ..schemas.conversations import AddConversationModel, ConversationModel, ConversationsModel
from ..utils.ai import get_ai_response

router = APIRouter()


@router.post("/conversations/")
async def add_conversation(conversation: AddConversationModel) -> ConversationModel:
    response = await get_ai_response(conversation.prompt)

    with open('db.json', 'r') as f:
        db = json.load(f)
        conversations = db["conversations"]
    
    if conversation.id in conversations.keys():
        conversations[conversation.id]["prompts"].append(conversation.prompt)
        conversations[conversation.id]["responses"].append(response)
    else:
        conversations[conversation.id] = {"prompts": [conversation.prompt], "responses": [response]}
    
    db["conversations"] = conversations
    with open('db.json', 'w') as f:
        json.dump(db, f, indent=4)
    
    return conversations[conversation.id]


@router.get("/conversations/")
async def get_conversations() -> ConversationsModel:
    with open('db.json', 'r') as f:
        conversations = json.load(f)["conversations"]
    
    return {"conversations": conversations}


@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str) -> ConversationModel:
    with open('db.json', 'r') as f:
        conversations = json.load(f)["conversations"]
    
    return conversations[conversation_id]