"""
In this file we will have reusable functions to interact with the data
in the database. CRUD comes from: Create, Read, Update, and Delete.

NOTE: Although in this example we are only creating and reading.

Links:
    https://fastapi.tiangolo.com/tutorial/sql-databases/#crud-utils
"""

from datetime import datetime
from sqlalchemy.orm import Session

import schemas
import models


def get_tournament_by_id(db_session: Session, tournament_id: int) -> models.Tournament | None:
    return db_session.query(models.Tournament).filter(
        models.Tournament.id == tournament_id
    ).first()


def get_player_by_email(db_session: Session, email: str) -> models.Player | None:
    return db_session.query(models.Player).filter(
        models.Player.email == email
    ).first()


def get_player_by_id(db_session: Session, player_id: int) -> models.Player | None:
    return db_session.query(models.Player).filter(
        models.Player.id == player_id
    ).first()


def get_player_tournaments(db_session: Session, player_db: models.Player, tournament_id: int) -> models.Player | None:
    tournament = get_tournament_by_id(db_session, tournament_id)
    for player in tournament.players_enrolled:
        if player.id == player_db.id:
            return player


def get_tournament_by_name(db_session: Session, tournament_name: str) -> models.Tournament | None:
    return db_session.query(models.Tournament).filter(
        models.Tournament.name == tournament_name
    ).first()


def create_player(
        db_session: Session,
        player: schemas.PlayerRegister,
) -> models.Player:
    fake_hashed_password = player.password + '-hashedpw'
    db_player = models.Player(
        full_name=player.full_name,
        email=player.email,
        hashed_password=fake_hashed_password,
        phone_number=player.phone_number,
        level=player.level,
    )
    db_session.add(db_player)
    db_session.commit()
    db_session.refresh(db_player)  # to get autoincrement id
    return db_player


def update_player_tournament(
        db_session: Session,
        db_player: models.Player,
        tournament_id: int,
):
    db_player.tournament.append(get_tournament_by_id(
        db_session, tournament_id))  # type: ignore
    db_session.commit()


def create_tournament(
        db_session: Session,
        tournament: schemas.TournamentRegister,
) -> models.Tournament:
    db_tournament = models.Tournament(
        name=tournament.name,
        start_date=datetime.strptime(tournament.start_date, '%d/%m/%Y').date(),
        end_date=datetime.strptime(tournament.end_date, '%d/%m/%Y').date(),
    )
    db_session.add(db_tournament)
    db_session.commit()
    db_session.refresh(db_tournament)
    return db_tournament
