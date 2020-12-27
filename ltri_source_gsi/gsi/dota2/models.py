from enum import Enum
from typing import Dict, Any, Optional

from pydantic import Field, BaseModel
from pydantic.dataclasses import dataclass
from common.models import DefaultAuth, Provider

GOLD = [255, 128, 0]


class Team(Enum):
    radiant = "radiant"
    dire = "dire"


class GameStateEnum(Enum):
    DOTA_GAMERULES_STATE_INIT = "DOTA_GAMERULES_STATE_INIT"
    DOTA_GAMERULES_STATE_WAIT_FOR_PLAYERS_TO_LOAD = "DOTA_GAMERULES_STATE_WAIT_FOR_PLAYERS_TO_LOAD"
    DOTA_GAMERULES_STATE_HERO_SELECTION = "DOTA_GAMERULES_STATE_HERO_SELECTION"
    DOTA_GAMERULES_STATE_STRATEGY_TIME = "DOTA_GAMERULES_STATE_STRATEGY_TIME"
    DOTA_GAMERULES_STATE_PRE_GAME = "DOTA_GAMERULES_STATE_PRE_GAME"
    DOTA_GAMERULES_STATE_GAME_IN_PROGRESS = "DOTA_GAMERULES_STATE_GAME_IN_PROGRESS"
    DOTA_GAMERULES_STATE_POST_GAME = "DOTA_GAMERULES_STATE_POST_GAME"
    DOTA_GAMERULES_STATE_DISCONNECT = "DOTA_GAMERULES_STATE_DISCONNECT"
    DOTA_GAMERULES_STATE_TEAM_SHOWCASE = "DOTA_GAMERULES_STATE_TEAM_SHOWCASE"
    DOTA_GAMERULES_STATE_CUSTOM_GAME_SETUP = "DOTA_GAMERULES_STATE_CUSTOM_GAME_SETUP"
    DOTA_GAMERULES_STATE_WAIT_FOR_MAP_TO_LOAD = "DOTA_GAMERULES_STATE_WAIT_FOR_MAP_TO_LOAD"
    DOTA_GAMERULES_STATE_LAST = "DOTA_GAMERULES_STATE_LAST"


@dataclass
class Building:
    health: int
    max_health: int


@dataclass
class BuildingHolder:
    radiant: Dict[str, Building]
    # dire: Dict[str, Building] = Field(default_factory=lambda x: {})


@dataclass
class Player:
    steamid: str
    name: str
    activity: str  # enum
    kills: int
    deaths: int
    assists: int
    last_hits: int
    denies: int
    kill_streak: int
    commands_issued: int
    kill_list: Dict[str, int]  # figure out
    team_name: Team
    gold: int
    gold_reliable: int
    gold_unreliable: int
    gold_from_hero_kills: int
    gold_from_creep_kills: int
    gold_from_income: int
    gold_from_shared: int
    gpm: int
    xpm: int

    # gold maxes at 16k for now
    def money_as_color(self):
        rb_value = (self.gold / 16000) * 255.
        return [255, 255, int(rb_value)]

    def money_as_color_inv(self):
        rg_value = (16000 - self.gold) / 16000 * 255.
        return [int(rg_value), int(rg_value), 0]


@dataclass
class Map:
    name: str
    matchid: str
    game_time: int
    clock_time: int
    daytime: bool
    nightstalker_night: bool
    game_state: GameStateEnum
    paused: bool
    win_team: str
    customgamename: str
    ward_purchase_cooldown: int


# @dataclass
class Hero(BaseModel):

    id: int
    name: str

    xpos: Optional[int]
    ypos: Optional[int]
    level: Optional[int]
    alive: Optional[bool]

    respawn_seconds: int
    buyback_cost: int
    buyback_cooldown: int

    health: int
    max_health: int
    health_percent: int

    mana: int
    max_mana: int
    mana_percent: int

    silenced: bool
    stunned: bool
    disarmed: bool
    magicimmune: bool
    hexed: bool
    muted: bool
    smoked: bool
    has_debuff: bool

    talent_1: bool
    talent_2: bool
    talent_3: bool
    talent_4: bool
    talent_5: bool
    talent_6: bool
    talent_7: bool
    talent_8: bool

    break_: bool = Field(False, alias="break")

    def health_as_color(self):
        if not self.alive:
            return GOLD
        bg_value = (self.health / self.max_health) * 255.
        return [255, int(bg_value), int(bg_value)]

    def health_as_color_inv(self):
        if not self.alive:
            return GOLD
        r_value = (self.max_health - self.health) / self.max_health * 255.
        return [int(r_value), 0, 0]

    # mana
    def mana_as_color(self):
        if not self.alive:
            return GOLD
        rg_value = (self.mana / self.max_mana) * 255.
        return [int(255 - rg_value / 2), int(255 - rg_value / 2), 255]

    def mana_as_color_inv(self):
        if not self.alive:
            return GOLD
        b_value = (self.max_mana - self.mana) / self.max_mana * 255.
        return [0, 0, int(b_value)]


@dataclass
class Ability:
    name: str
    level: int
    can_cast: bool
    passive: bool
    ability_active: bool
    cooldown: int
    ultimate: bool


@dataclass
class Item:
    name: str
    purchaser: Optional[int] = None
    passive: Optional[bool] = None
    can_cast: Optional[bool] = None
    cooldown: Optional[int] = None
    charges: Optional[int] = None


@dataclass
class GameState:
    auth: DefaultAuth
    provider: Provider
    player: Player
    draft: Dict[str, Any]

    map: Optional[Map] = Field(default_factory=dict)
    hero: Optional[Hero] = Field(default_factory=dict)
    buildings: Optional[BuildingHolder] = Field(default_factory=dict)
    abilities: Optional[Dict[str, Ability]] = Field(default_factory=dict)
    items: Optional[Dict[str, Item]] = Field(default_factory=dict)
    wearables: Optional[Dict[str, int]] = Field(default_factory=dict)
    previously: Optional[Dict[str, Any]] = Field(default_factory=dict)
