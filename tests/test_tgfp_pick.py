"""Unit Test  for TGFPPick class"""
import pytest
from pytest import FixtureRequest
from bson import ObjectId


# pylint: disable=redefined-outer-name
from tgfp import TGFP, TGFPPick

from config import get_config, Config

config: Config = get_config()


@pytest.fixture
def tgfp_db(mocker) -> TGFP:
    """
    This will return the default tgfp database object loaded with the test fixture

    :return: tgfp database object
    :rtype: TGFP
    """
    mocker.patch("tgfp.TGFP.current_season", return_value=2022)
    return TGFP(config.MONGO_URI)


# pylint: disable=missing-function-docstring
@pytest.fixture
def pick(tgfp_db, request: FixtureRequest) -> TGFPPick:
    pick: TGFPPick = tgfp_db.find_picks()[0]

    def reset_db():
        pick.load_record()
        pick.save()

    request.addfinalizer(reset_db)
    return pick


def test_pick(pick: TGFPPick):
    assert len(pick.pick_detail) == 16


def test_pick_init():
    new_pick = TGFPPick(TGFP(config.MONGO_URI), data=None)
    assert hasattr(new_pick, 'week_no') is False


def test_winner_for_game_id(pick):
    game_id = ObjectId('6314a964f0d6ff0b1736f8c5')
    winner_id = ObjectId('59ac8d50ee45e20848e11a6f')
    bogus_game_id = ObjectId('5d827532dd2d55018d8d756b')
    assert pick.winner_for_game_id(game_id) == winner_id
    assert pick.winner_for_game_id(bogus_game_id) is None


def test_save(pick):
    assert pick.wins == 8
    pick.wins = 4
    pick.save()
    new_pick: TGFPPick = TGFP(config.MONGO_URI).find_picks(season=2022)[0]
    assert new_pick.id == pick.id
    assert new_pick.wins == 4


def test_load_record(pick):
    assert pick.wins == 8
    pick.wins = 3
    assert pick.wins == 3
    pick.load_record()
    assert pick.wins == 8


def test_games(pick):
    assert len(pick.games) > 15
