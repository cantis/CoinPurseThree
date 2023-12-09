from sqlalchemy.orm import Session
from . import models, schemas

def create_player(db: Session, player: schemas.PlayerCreate):
    db_player = models.Player(name=player.name, score=player.score)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

def update_player(db: Session, player: schemas.PlayerUpdate):
    db_player = db.query(models.Player).filter(models.Player.id == player.id).first()
    if db_player:
        db_player.name = player.name
        db_player.score = player.score
        db.commit()
        db.refresh(db_player)
    return db_player

def delete_player(db: Session, player_id: int):
    db_player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if db_player:
        db.delete(db_player)
        db.commit()
    return db_player
