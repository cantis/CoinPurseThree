from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Character(BaseModel):
    id: int
    name: str
    level: int

characters = []

@router.get("/characters")
def get_characters():
    return characters

@router.get("/characters/{character_id}")
def get_character(character_id: int):
    for character in characters:
        if character["id"] == character_id:
            return character
    return {"message": "Character not found"}

@router.post("/characters")
def create_character(character: dict):
    characters.append(character)
    return {"message": "Character created successfully"}

@router.put("/characters/{character_id}")
def update_character(character_id: int, updated_character: dict):
    for character in characters:
        if character["id"] == character_id:
            character.update(updated_character)
            return {"message": "Character updated successfully"}
    return {"message": "Character not found"}

@router.delete("/characters/{character_id}")
def delete_character(character_id: int):
    for character in characters:
        if character["id"] == character_id:
            characters.remove(character)
            return {"message": "Character deleted successfully"}
    return {"message": "Character not found"}
