from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Player(BaseModel):
    name: str
    is_active: bool

class Character(BaseModel):
    player: int
    charcter_name: str
    character_class: str
    is_active: bool

class Transaction(BaseModel):
    player: int
    item: int
    price: int
    is_sale: bool

# In memory data store for now...
players = []
characters = []
transactions = []

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get('/player/')
async def list_players():
    '''Get a list of players'''
    return players

@app.get('/player/{id}')
async def get_player_by_id(id:int):
    '''Get a player by id'''
    return {'Player Id': id}

@app.post('/player/')
async def create_player(player: Player):
    '''Add a new player'''
    players.append(player)
    return {'Player Name:': player.name}

@app.put('/player/')
async def update_player(player: Player):
    '''Update a player'''
    return {'Player Name:': player.name}

@app.delete('/player/{id}')
async def delete_player(id:int):
    '''Delete a player'''
    return {'Player Id': id}

@app.get('/character/')
async def list_characters():
    '''Get a list of characters'''
    return characters

@app.get('/character/{id}')
async def get_character_by_id(id:int):
    '''Get a character by id'''
    return {'Character Id': id}

@app.post('/character/')
async def create_character(character: Character):
    '''Add a new character'''
    characters.append(character)

@app.put('/character/')
async def update_character(character: Character):
    '''Update a character'''
    return {'Character Name:': character.charcter_name}

@app.delete('/character/{id}')
async def delete_character(id:int):
    '''Delete a character'''
    return {'Character Id': id}

@app.get('/buy/')
async def buy():
    '''Remove money from player, optional: record item in inventory'''
    return {'message': 'buy'}

@app.get('/sell/')
async def sell():
    '''Add money to player, optional: remove item from inventory'''
    return {'message': 'sell'}