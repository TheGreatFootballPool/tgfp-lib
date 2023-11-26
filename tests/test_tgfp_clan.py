""" Test module for testing clans """
from tgfp import TGFP, TGFPClan, TGFPPlayer
from config import get_config, Config

config: Config = get_config()


def test_clan():
    """ First test class"""
    tgfp = TGFP(config.MONGO_URI)
    clans = tgfp.clans()
    for clan in clans:
        assert clan


def test_add_member():
    """ Test adding a clan to the DB """
    tgfp = TGFP(config.MONGO_URI)
    johns_clan: TGFPClan = tgfp.find_clan(clan_name="Team John")
    johns_clan.delete_all_members()
    assert johns_clan
    assert isinstance(johns_clan, TGFPClan)
    player: TGFPPlayer = johns_clan.add_member(752964049959911514)
    assert player.first_name == "Teresa"
    player_2: TGFPPlayer = johns_clan.add_member(752964049959911514)
    assert player_2 is None
    johns_clan.delete_all_members()


def test_find_clan_by_discord_id():
    """ Test searching by discord ID"""
    tgfp = TGFP(config.MONGO_URI)
    johns_clan: TGFPClan = tgfp.find_clan(discord_role_id=1016665854538154076)
    assert johns_clan.clan_name == "Team John"


def test_delete_member():
    """ Test the 'delete all members' functionality """
    tgfp = TGFP(config.MONGO_URI)
    johns_clan: TGFPClan = tgfp.find_clan(clan_name="Team John")
    player: TGFPPlayer = johns_clan.add_member(752964049959911514)
    assert player.first_name == "Teresa"
    player_2: TGFPPlayer = johns_clan.add_member(752964049959911514)
    assert len(johns_clan.members) > 0
    assert player_2 is None
    johns_clan.delete_all_members()
    assert len(johns_clan.members) == 0
