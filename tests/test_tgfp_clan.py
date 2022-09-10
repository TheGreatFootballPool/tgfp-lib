""" Test module for testing clans """
from tgfp import TGFP, TGFPClan


def test_clan():
    """ First test class"""
    tgfp = TGFP()
    clans = tgfp.clans()
    for clan in clans:
        assert clan


def test_add_clan():
    """ Test adding a clan to the DB """
    tgfp = TGFP()
    new_clan: TGFPClan = TGFPClan(tgfp=tgfp)
    new_clan.clan_name = "Team Don"
    new_clan.captain_name = "Don Kassner"
    new_clan.save()
