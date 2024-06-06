import pytest
from fastapi.testclient import TestClient
from ..main import app
import json
from ..schemas.conversations import AddConversationModel

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def sample_conversation1():
    return AddConversationModel(id="test_id", prompt="say test")

@pytest.fixture
def sample_conversation2():
    return AddConversationModel(id="new_test_id", prompt="say test")

def test_get_conversations(client):
    response = client.get("/conversations/")
    assert response.status_code == 200
    assert "conversations" in response.json()
    assert isinstance(response.json()["conversations"], dict)

    for conversation in response.json()["conversations"].values():
        assert isinstance(conversation, dict)
        assert "prompts" in conversation.keys()
        assert isinstance(conversation["prompts"], list)
        assert "responses" in conversation.keys()
        assert isinstance(conversation["responses"], list)

def test_get_conversation(client):
    response = client.get("/conversations/test_id")
    assert response.status_code == 200
    assert "prompts" in response.json()
    assert "responses" in response.json()
    assert response.json()["prompts"][0] == "test_prompt_1"
    assert response.json()["responses"][0] == "test_response_1"


def test_add_conversation_existing_id(client, sample_conversation1):
    conversations = client.get("/conversations/").json()["conversations"]
    before_prompt_len = len(conversations["test_id"]["prompts"])
    before_response_len = len(conversations["test_id"]["responses"])

    response = client.post("/conversations/", json=sample_conversation1.model_dump())
    assert response.status_code == 200

    conversations = client.get("/conversations/").json()["conversations"]
    assert len(conversations["test_id"]["prompts"]) == before_prompt_len + 1
    assert len(conversations["test_id"]["responses"]) == before_response_len + 1
    assert conversations["test_id"]["prompts"][-1] == "say test"

    with open("db.json") as f:
        db = json.load(f)
        conversations = db["conversations"]
        del conversations["test_id"]["prompts"][-1]
        del conversations["test_id"]["responses"][-1]
        db["conversations"] = conversations
    
    with open("db.json", "w") as f:
        json.dump(db, f)


def test_add_conversation_new_id(client, sample_conversation2):
    conversations = client.get("/conversations/").json()["conversations"]
    before_len = len(conversations.keys())

    response = client.post("/conversations/", json=sample_conversation2.model_dump())
    assert response.status_code == 200
    assert "prompts" in response.json()
    assert "responses" in response.json()
    assert response.json()["prompts"][0] == "say test"

    conversations = client.get("/conversations/").json()["conversations"]
    assert len(conversations.keys()) == before_len + 1

    with open("db.json") as f:
        db = json.load(f)
        conversations = db["conversations"]
        del conversations["new_test_id"]
        db["conversations"] = conversations
    
    with open("db.json", "w") as f:
        json.dump(db, f)