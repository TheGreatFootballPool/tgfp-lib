"""Unit Test TGFP Team """
from typing import List

import pytest
from tgfp import TGFP, TGFPTeam
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
    mocker.patch("tgfp.TGFP.current_season", return_value=2022)
    return TGFP(config.MONGO_URI)


# pylint: disable=missing-function-docstring
def test_team(tgfp_db):
    teams: List[TGFPTeam] = tgfp_db.find_teams(tgfp_nfl_team_id='s:20~l:28~t:2')
    team: TGFPTeam = teams[0]
    assert team.long_name == 'Bills'
    assert team.discord_emoji == "<:buf:1023040265998577724>"
    teams = tgfp_db.teams()
    assert len(teams) == 32
    team_1: TGFPTeam
    team_1 = teams[0]
    team_data = team_1.mongo_data()
    assert '_id' not in team_data
    assert 'short_name' in team_data
    assert 'discord_emoji' in team_data
