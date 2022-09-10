""" Test module for testing clans """
from tgfp import TGFP, TGFPClan, TGFPPlayer


def test_clan():
    """ First test class"""
    tgfp = TGFP()
    clans = tgfp.clans()
    for clan in clans:
        assert clan


def test_add_member():
    """ Test adding a clan to the DB """
    tgfp = TGFP()
    dons_clan: TGFPClan = tgfp.find_clan(clan_name="Team Don")
    assert dons_clan
    assert isinstance(dons_clan, TGFPClan)
    player: TGFPPlayer = dons_clan.add_member("Will Kahl")
    assert player.first_name == "Will"
    dons_clan.save()
    player_2: TGFPPlayer = dons_clan.add_member("Will Kahl")
    assert player_2 is None
