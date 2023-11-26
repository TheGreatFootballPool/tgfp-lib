"""Unit Test wrapper for discord_bot_tester.py"""
from datetime import datetime
import pytest

# pylint: disable=redefined-outer-name
from tgfp import TGFP, TGFPGame, TGFPTeam
from config import get_config, Config

config: Config = get_config()


@pytest.fixture
def tgfp_db(mocker):
    """
    This will return the default tgfp database object loaded with the test fixture

    :return: tgfp database object
    :rtype: TGFP
    """
    mocker.patch("tgfp.TGFP.current_season", return_value=2022)
    return TGFP(config.MONGO_URI)


# pylint: disable=missing-function-docstring
@pytest.fixture
def game(tgfp_db: TGFP) -> TGFPGame:
    return tgfp_db.find_games(season=2022)[0]


@pytest.fixture
def west_coast_game(tgfp_db: TGFP) -> TGFPGame:
    return tgfp_db.find_games(tgfp_nfl_game_id='s:20~l:28~e:401437653')[0]


def test_tgfpgame(game: TGFPGame):
    assert isinstance(game, TGFPGame)


def test_game_mongo_data(game):
    game_data = game.mongo_data()
    assert '_id' not in game_data
    assert 'game_status' in game_data


def test_game_save(game: TGFPGame):
    assert game.game_status == 'STATUS_FINAL'
    game.game_status = 'STATUS_IN_PROGRESS'
    new_tgfp = TGFP(config.MONGO_URI)
    new_game = new_tgfp.find_games(season=2022)[0]
    assert new_game.game_status == 'STATUS_FINAL'
    game.save()
    newer_tgfp = TGFP(config.MONGO_URI)
    newer_game = newer_tgfp.find_games(season=2022)[0]
    assert newer_game.game_status == 'STATUS_IN_PROGRESS'
    newer_game.game_status = 'STATUS_FINAL'
    newer_game.save()


# noinspection DuplicatedCode
def test_winner_id_of_game(game: TGFPGame):
    home_team_id = game.home_team_id
    road_team_id = game.road_team_id
    assert game.winner_id_of_game == road_team_id
    game.home_team_score = 100
    assert game.winner_id_of_game == home_team_id
    game.road_team_score = 100
    assert game.winner_id_of_game is None
    game.road_team_score = 4
    assert game.winner_id_of_game == home_team_id
    game.game_status = 'STATUS_IN_PROGRESS'
    assert game.winner_id_of_game is None


# noinspection DuplicatedCode
def test_leader_id_of_game(game: TGFPGame):
    home_team_id = game.home_team_id
    road_team_id = game.road_team_id
    assert game.leader_id_of_game == road_team_id
    game.home_team_score = 100
    assert game.leader_id_of_game == home_team_id
    game.road_team_score = 100
    assert game.leader_id_of_game is None
    game.road_team_score = 4
    assert game.leader_id_of_game == home_team_id
    game.game_status = 'STATUS_IN_PROGRESS'
    assert game.leader_id_of_game == home_team_id


# noinspection DuplicatedCode
def test_loser_id_of_game(game: TGFPGame):
    home_team_id = game.home_team_id
    road_team_id = game.road_team_id
    assert game.loser_id_of_game == home_team_id
    game.home_team_score = 100
    assert game.loser_id_of_game == road_team_id
    game.road_team_score = 100
    assert game.loser_id_of_game is None
    game.road_team_score = 4
    assert game.loser_id_of_game == road_team_id
    game.game_status = 'STATUS_IN_PROGRESS'
    assert game.loser_id_of_game is None


def test_winning_team(game: TGFPGame):
    winning_team: TGFPTeam = game.winning_team
    assert winning_team.full_name == "Buffalo Bills"
    game.road_team_score = 10
    game.home_team_score = 10
    assert game.winning_team is None


def test_losing_team(game: TGFPGame):
    losing_team: TGFPTeam = game.losing_team
    assert losing_team.full_name == "Los Angeles Rams"
    game.road_team_score = 10
    game.home_team_score = 10
    assert game.losing_team is None


def test_winning_team_score(game: TGFPGame):
    assert game.winning_team_score == 31
    game.road_team_score = 5
    assert game.winning_team_score == 10


def test_losing_team_score(game: TGFPGame):
    assert game.losing_team_score == 10
    game.road_team_score = 5
    assert game.losing_team_score == 5


def test_underdog_team_id(game: TGFPGame):
    assert game.underdog_team_id == game.home_team_id


def test_pacific_start_time(west_coast_game: TGFPGame):
    pacific_start_time: datetime = west_coast_game.pacific_start_time
    assert pacific_start_time.hour == 13
    assert pacific_start_time.minute == 25
