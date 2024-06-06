from pydantic import BaseModel

class AddConversationModel(BaseModel):
    id: str
    prompt: str

class ConversationModel(BaseModel):
    prompts: list[str]
    responses: list[str]

class ConversationsModel(BaseModel):
    conversations: dict[str, ConversationModel]