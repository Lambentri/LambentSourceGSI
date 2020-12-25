# from dataclasses import dataclass
from enum import Enum

from pydantic.dataclasses import dataclass
from typing import Any, Dict


class TeamEnum(Enum):
    CT = "CT"
    T = "T"


class PhaseEnum(Enum):
    LIVE = "live"
    FREEZE = "freezetime"
    OVER = "over"


class ModeEnum(Enum):
    DEATHMATCH = "deathmatch"
    CASUAL = "casual"


class BombEnum(Enum):
    PLANTED = "planted"
    EXPLODED = "exploded"
    DEFUSED = "defused"


class WinCondition(Enum):
    T_WIN_BOMB = "t_win_bomb"
    CT_WIN_DEFUSE = "ct_win_defuse"
    CT_WIN_TIME = "ct_win_time"

    T_WIN_ELIM = "t_win_elimination"
    CT_WIN_ELIM = "ct_win_elimination"

    CT_WIN_RESCUE = "ct_win_rescue"


class WeaponState(Enum):
    ACTIVE = 'active'
    HOLSTERED = 'holstered'
    RELOADING = 'reloading'


class WeaponType(Enum):
    KNIFE = "Knife"
    PISTOL = "Pistol"
    C4 = "C4"
    MACHINE = "Machine Gun"
    GRENADE = "Grenade"
    SHOTGUN = "Shotgun"
    SMG = "Submachine Gun"
    RIFLE = "Rifle"
    STACKABLE = "StackableItem"
    SNIPER = "SniperRifle"


@dataclass
class TeamVals:
    score: int
    consecutive_round_losses: int
    timeouts_remaining: int
    matches_won_this_series: int


@dataclass
class MatchStats:
    kills: int
    assists: int
    deaths: int
    mvps: int
    score: int


@dataclass
class MatchState:
    health: int
    armor: int
    helmet: bool
    flashed: int
    smoked: int
    burning: int
    money: int
    round_kills: int
    round_killhs: int
    equip_value: int
    defusekit: int = None

    def health_as_color(self):
        bg_value = (self.health / 100) * 255.
        return [255, int(bg_value), int(bg_value)]

    def health_as_color_inv(self):
        r_value = (100 - self.health) / 100 * 255.
        return [int(r_value), 0, 0]

    # health but blue for now
    def armor_as_color(self):
        rg_value = (self.armor / 100) * 255.
        return [int(rg_value), 255, int(rg_value)]

    def armor_as_color_inv(self):
        b_value = (100 - self.armor) / 100 * 255.
        return [0, 0, int(b_value)]

    # health but green for now
    def money_as_color(self):
        rb_value = (self.money / 16000) * 255.
        return [int(rb_value), 255, int(rb_value)]

    def money_as_color_inv(self):
        g_value = (16000 - self.money) / 16000 * 255.
        return [0, int(g_value), 0]


@dataclass
class Weapon:
    name: str
    paintkit: str
    type: WeaponType
    state: WeaponState
    ammo_clip: int = None
    ammo_clip_max: int = None
    ammo_reserve: int = None


@dataclass
class Player:
    steamid: str
    name: str
    activity: str
    team: TeamEnum = None
    activity: str = None
    match_stats: MatchStats = None
    state: MatchState = None
    weapons: Dict[str, Weapon] = None
    observer_slot: int = None


@dataclass
class Provider:
    name: str
    appid: int
    version: int
    steamid: str
    timestamp: int


@dataclass
class Map:
    mode: ModeEnum
    name: str
    phase: PhaseEnum
    round: int
    team_ct: TeamVals
    team_t: TeamVals
    num_matches_to_win_series: int
    current_spectators: int
    souvenirs_total: int

    round_wins: Dict[str, WinCondition] = None


@dataclass
class DefaultAuth:
    token: str


@dataclass
class Round:
    phase: PhaseEnum
    bomb: BombEnum = None
    win_team: TeamEnum = None


@dataclass
class Previously:
    player: Player


@dataclass
class GameState:
    # map_round_wins = MapHistory()
    player: Player
    provider: Provider
    map: Map = None
    player_id: Any = None
    round: Round = None
    auth: DefaultAuth = None
    previously: Dict = None  # this is unpred
    added: Dict = None

    # spectator only
    # allgrenades = Grenades()
    # allplayers_id = List(Players())
    # allplayers_match_stats = List(PlayerMatchStats())
    # allplayers_position = List(PlayerPosition())
    # allplayers_stats = List(PlayerState())
    # allplayers_weapons = List(PlayerWeapons())
    # bomb = Bomb()
    # phase_countdowns = PhaseCountdowns()
    # player_position = PlayerPosition()
