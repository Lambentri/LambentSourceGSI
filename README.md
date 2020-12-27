 
# Lambent Source GSI (LSG)

[![Gitter](https://badges.gitter.im/Lambentri/community.svg)](https://gitter.im/Lambentri/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

A LambentAether4 machine producer that integrates with source engine Game State Integration

## CSGO

### Setup

Copy the [example GSI document](ltri_source_gsi/gsi/csgo/game_state_integration.cfg) into the `$CSGO_ROOT/csgo/cfg/gamestate_integration_ltri.cfg`

#### GSI Docs

https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Game_State_Integration


### Features

The entirety of the GSI payload is mapped into dataclasses

LSG currently implements basic features reacting on changes in:
- Health
- Armor
- Money

*TODO* Features:
- support for lights following ticking in DE_ modes.


## DOTA 2 (Conceptual Still)

### Setup

Copy the [example GSI document](ltri_source_gsi/gsi/dota2/game_state_integration.cfg) into the `$DOTA_ROOT/game/dota/cfg/gamestate_integration/gamestate_integration_ltri.cfg`

#### On Docs

No docs? will likely reveng another library to create the pydantic models

Copy example GSI document into the `$CSGO_ROOT/csgo/cfg/gamestate_integration_ltri.cfg`

### Features

LSG currently implements basic features reacting on changes in:

- Health
- Mana
- Gold

*TODO* Features:
- more complex game state following

## Running

After copying the config into the game cfg folder, run the relevant server as so: 

### CSGO 

`docker run --rm --network host --name ltri-gsi-csgo -P -e LA4_XBAR_ROUTER=ws://192.168.1.1:8083/ws ltri-gsi-csgo`

### DOTA2

`docker run --rm -d --network host --name ltri-gsi-dota2 -P -e LA4_XBAR_ROUTER=ws://192.168.1.1:8083/ws ltri-gsi-dota2`