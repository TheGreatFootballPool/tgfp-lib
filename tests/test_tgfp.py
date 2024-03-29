"""Unit Test For TGFP """
import os
from typing import List

import pytest
from bson import ObjectId

from tgfp import TGFP, TGFPGame, TGFPTeam, TGFPPick, TGFPPlayer

from config import get_config, Config

config: Config = get_config()


# pylint: disable=redefined-outer-name
@pytest.fixture
def tgfp_db(mocker):
    """
    This will return the default tgfp database object loaded with the test fixture

    :return: tgfp database object
    :rtype: TGFP
    """
    mongo_uri = config.MONGO_URI
    mocker.patch("tgfp.TGFP.current_season", return_value=2019)
    return TGFP(mongo_uri)


@pytest.fixture
def tgfp_db_reg_season(tgfp_db: TGFP):
    """
    Extends the :func:`tgfp_db` database method, truncates the playoffs, returning just
    the regular season
    :param tgfp_db: test DB with all the test data loaded
    :type tgfp_db: TGFP
    :return: Test DB with playoff games removed (just regular season)
    :rtype: TGFP
    """
    games = tgfp_db.find_games(season=2019, ordered_by='week_no')
    new_games = []
    for game in games:
        if game.week_no <= 17:  # 17 weeks in the regular season
            new_games.append(game)
    # pylint: disable=protected-access
    # ^^^ I know what I'm doing here.
    tgfp_db._games = new_games
    return tgfp_db


@pytest.fixture
def tgfp_db_reg_season_a(tgfp_db_reg_season):
    """
    Extends the :func:`tgfp_db_reg_season` database method, sets one game in the final week to
    'pregame'

    :param tgfp_db_reg_season: Test DB with all the regular season games loaded
    :type tgfp_db_reg_season: TGFP
    :return: Same DB as input with one game set to 'pregame'
    :rtype: TGFP
    """
    last_game = tgfp_db_reg_season.find_games(ordered_by='week_no')[-1]
    last_game.game_status = 'pregame'
    return tgfp_db_reg_season


@pytest.fixture
def tgfp_db_reg_season_b(tgfp_db_reg_season):
    """
    Extends the :func:`tgfp_db_reg_season` database method, sets one game in the final week to
    'in progress'

    :param tgfp_db_reg_season: Test DB with all the regular season games loaded
    :type tgfp_db_reg_season: TGFP
    :return: Same DB as input with one game set to 'in progress'
    :rtype: TGFP
    """
    last_game = tgfp_db_reg_season.find_games(ordered_by='week_no')[-1]
    last_game.game_status = 'in progress'
    return tgfp_db_reg_season


@pytest.fixture
def tgfp_db_reg_season_c(tgfp_db_reg_season):
    """
    Extends the :func:`tgfp_db_reg_season` database method, sets all games in the final week to
    'pregame'

    :param tgfp_db_reg_season: Test DB with all the regular season games loaded
    :type tgfp_db_reg_season: TGFP
    :return: Same DB as input with all games in the final week to
    'pregame'
    :rtype: TGFP
    """
    for game in tgfp_db_reg_season.games():
        if game.week_no == 17:
            game.game_status = 'pregame'

    return tgfp_db_reg_season


@pytest.fixture
# regular season with all games of last week in progress
def tgfp_db_reg_season_d(tgfp_db_reg_season):
    """
    Extends the :func:`tgfp_db_reg_season` database method, sets all games in the final week to
    'in progress'

    :param tgfp_db_reg_season: Test DB with all the regular season games loaded
    :type tgfp_db_reg_season: TGFP
    :return: Same DB as input with all games in the final week to
    'in progress'
    :rtype: TGFP
    """
    for game in tgfp_db_reg_season.games():
        if game.week_no == 17:
            game.game_status = 'in progress'

    return tgfp_db_reg_season


@pytest.fixture
def tgfp_db_live():
    """ Return the live TGFP db object"""
    mongo_uri = config.MONGO_URI
    return TGFP(mongo_uri)


# pylint: disable=missing-function-docstring
def test_live_week_no(tgfp_db_live):
    assert tgfp_db_live.current_week() == 16


def test_games(tgfp_db):
    games = tgfp_db.find_games(season=2019)
    assert len(games) == 267
    assert isinstance(games[0], TGFPGame)


def test_teams(tgfp_db):
    teams = tgfp_db.teams()
    assert len(teams) == 32
    assert isinstance(teams[0], TGFPTeam)


def test_picks(tgfp_db):
    picks = tgfp_db.find_picks(season=2019)
    assert len(picks) == 441
    assert isinstance(picks[0], TGFPPick)


def test_players(tgfp_db):
    picks = tgfp_db.players()
    assert 20 < len(picks) < 100
    assert isinstance(picks[0], TGFPPlayer)


def test_current_week_last_week(tgfp_db_reg_season):
    # count the new games array to make sure we've got a good set of data
    assert len(tgfp_db_reg_season.games()) == (267 - 11)  # all playoff games plus last week
    assert tgfp_db_reg_season.current_week() == 17  # should be the last completed week + 1
    assert tgfp_db_reg_season.current_active_week() == 16


def test_current_week_one_game_in_pregame(tgfp_db_reg_season_a):
    assert tgfp_db_reg_season_a.current_week() == 17
    assert tgfp_db_reg_season_a.current_active_week() == 16


def test_current_week_one_in_progress(tgfp_db_reg_season_b):
    assert tgfp_db_reg_season_b.current_week() == 17
    assert tgfp_db_reg_season_b.current_active_week() == 16


def test_current_week_all_games_pregame(tgfp_db_reg_season_c):
    assert tgfp_db_reg_season_c.current_week() == 17
    assert tgfp_db_reg_season_c.current_active_week() == 16


def test_current_week_all_games_in_progress(tgfp_db_reg_season_d):
    assert tgfp_db_reg_season_d.current_week() == 17
    assert tgfp_db_reg_season_d.current_active_week() == 16


def test_home_page_text(tgfp_db):
    assert '<br><br><font class="date" style="font-weight:bold">Welcome</font>' \
           in tgfp_db.home_page_text()


def test_find_players(tgfp_db):
    """
    Here's the API for find_players:
    ordered_by=None,
    reverse_order=False

    I should test all these conditions
    """
    # should find all players
    assert 20 < len(tgfp_db.find_players()) < 100
    found_players = tgfp_db.find_players(player_id=ObjectId('59a97660ee45e20848e119aa'))
    assert len(found_players) == 1
    assert found_players[0].email == 'john.sturgeon@gmail.com'
    found_players = tgfp_db.find_players(player_email='wkahl22@gmail.com')
    assert len(found_players) == 1
    assert found_players[0].id == ObjectId('59ab2fb5ee45e20848e119d6')
    found_players = tgfp_db.find_players(discord_id=609144199618494483)
    assert len(found_players) == 1
    assert found_players[0].email == 'jamesvanboxtel@gmail.com'
    found_players = tgfp_db.find_players(player_active=False)
    assert 0 < len(found_players) < 10
    found_players = tgfp_db.find_players(ordered_by='total_points')
    assert 20 < len(found_players) < 100
    assert found_players[0].total_points() == 0  # last place
    assert found_players[-1].total_points() == 195  # first place
    found_players = tgfp_db.find_players(ordered_by='total_points', reverse_order=True)
    assert 20 < len(found_players) < 100
    assert found_players[0].total_points() == 195  # first place
    assert found_players[-1].total_points() == 0  # last place


def test_find_teams(tgfp_db):
    assert len(tgfp_db.find_teams()) == 32
    found_teams = tgfp_db.find_teams(team_id=ObjectId('59ac8d10ee45e20848e11a69'))
    assert len(found_teams) == 1
    assert found_teams[0].long_name == '49ers'
    found_teams = tgfp_db.find_teams(tgfp_nfl_team_id='s:20~l:28~t:3')
    assert len(found_teams) == 1
    assert found_teams[0].long_name == 'Bears'


def test_find_picks(tgfp_db):
    assert len(tgfp_db.find_picks()) == 441
    # noinspection SpellCheckingInspection
    found_picks = tgfp_db.find_picks(pick_id=ObjectId('5b8feea5bf75f56e643f991a'))
    assert len(found_picks) == 1
    assert found_picks[0].player_id == ObjectId('59a97660ee45e20848e119aa')
    found_picks = tgfp_db.find_picks(week_no=1)
    assert len(found_picks) == 22
    found_picks = tgfp_db.find_picks(season=2020)
    assert len(found_picks) == 420
    found_picks = tgfp_db.find_picks(season=2000)
    assert len(found_picks) == 0
    found_picks = tgfp_db.find_picks(season=2019)
    assert len(found_picks) == 441
    found_picks = tgfp_db.find_picks(player_id=ObjectId('59a97660ee45e20848e119aa'))
    assert len(found_picks) == 21


def test_find_games(tgfp_db):
    assert len(tgfp_db.find_games()) == 267
    found_games = tgfp_db.find_games(game_id=ObjectId('5d6fcc5fd4fa6803c650581b'))
    assert len(found_games) == 1
    assert found_games[0].tgfp_nfl_game_id == 'nfl.g.20190908030'
    found_games = tgfp_db.find_games(tgfp_nfl_game_id='nfl.g.20190908020')
    assert found_games[0].home_team_score == 16
    assert len(found_games) == 1
    found_games = tgfp_db.find_games(week_no=15)
    assert len(found_games) == 16
    assert found_games[0].favorite_team_id == ObjectId('59ac8f79ee45e20848e11a95')
    found_games = tgfp_db.find_games(season=2019)
    assert len(found_games) == 267
    found_games = tgfp_db.find_games(season=2018)
    assert len(found_games) == 254
    found_games = tgfp_db.find_games(season=2020)
    assert len(found_games) == 268
    found_games = tgfp_db.find_games(season=2021)
    assert len(found_games) == 289
    found_games = tgfp_db.find_games(season=2000)
    assert len(found_games) == 0
    found_games = tgfp_db.find_games(season=2019, week_no=15)
    assert len(found_games) == 16
    found_games = tgfp_db.find_games(season=2000, week_no=15)
    assert len(found_games) == 0
    found_games = tgfp_db.find_games(home_team_id=ObjectId("59ac8f24ee45e20848e11a80"))
    assert len(found_games) == 8
    found_games = tgfp_db.find_games(ordered_by='start_time')
    assert found_games[0].tgfp_nfl_game_id == 'nfl.g.20190905003'


def test_seasons(tgfp_db):
    seasons: List[int] = tgfp_db.seasons
    assert seasons[0] == 2018
    assert tgfp_db.current_season() == seasons[1]
