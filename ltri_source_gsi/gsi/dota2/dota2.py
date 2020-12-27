import json
import os

from autobahn.twisted.component import Component, run
from autobahn.wamp import RegisterOptions, PublishOptions
from klein import Klein
from pydantic.json import pydantic_encoder
from twisted.internet.defer import inlineCallbacks
from twisted.web.http import Request
from typing import Optional

from common.compat import Machine, MachineDict
from models import GameState

# this is mostly working, just needs cleanup

PREFIX = "com.lambentri.edge.la4.extservices.gsi.dota"
SRC_PREFIX = "com.lambentri.edge.la4.machine.link.src."

LEDS_IN_ARRAY_DEFAULT = int(os.environ.get("LA4_GSI_LEDS", 256))

##
wamp_component = Component(
    transports=os.environ.get("LA4_XBAR_ROUTER", "ws://127.0.0.1:8083/ws"),
    realm=os.environ.get("LA4_XBAR_REALM", "realm1"),
)
wamp_component.state: Optional[GameState] = None
wamp_component.count = 0


@inlineCallbacks
def publish_gsi(session):
    if wamp_component.state:
        options = PublishOptions(retain=True)
        yield session.publish(f"{SRC_PREFIX}ltri-dota-gsi-health",
                              wamp_component.state.hero.health_as_color() * LEDS_IN_ARRAY_DEFAULT,
                              id="ltri-dota-gsi-health", options=options)
        yield session.publish(f"{SRC_PREFIX}ltri-dota-gsi-health-inv",
                              wamp_component.state.hero.health_as_color_inv() * LEDS_IN_ARRAY_DEFAULT,
                              id="ltri-dota-gsi-health-inv", options=options)
        yield session.publish(f"{SRC_PREFIX}ltri-dota-gsi-mana",
                              wamp_component.state.hero.mana_as_color() * LEDS_IN_ARRAY_DEFAULT,
                              id="ltri-dota-gsi-mana", options=options)
        yield session.publish(f"{SRC_PREFIX}ltri-dota-gsi-mana-inv",
                              wamp_component.state.hero.mana_as_color_inv() * LEDS_IN_ARRAY_DEFAULT,
                              id="ltri-dota-gsi-mana-inv", options=options)
        yield session.publish(f"{SRC_PREFIX}ltri-dota-gsi-money",
                              wamp_component.state.player.money_as_color() * LEDS_IN_ARRAY_DEFAULT,
                              id="ltri-dota-gsi-money", options=options)
        yield session.publish(f"{SRC_PREFIX}ltri-dota-gsi-money-inv",
                              wamp_component.state.player.money_as_color_inv() * LEDS_IN_ARRAY_DEFAULT,
                              id="ltri-dota-gsi-money-inv", options=options)
    yield None


@wamp_component.on_join
@inlineCallbacks
def joined(session, details):
    print("session ready")
    wamp_component.loop_gsi_publish = task.LoopingCall(publish_gsi, session=session)
    wamp_component.loop_gsi_publish.start(.05)


@wamp_component.register("com.lambentri.edge.la4.machine.list", options=RegisterOptions(invoke="roundrobin"))
def list_active_machine_instances():
    """List all available machines"""
    schema = MachineDict(
        machines=
        {
            # these don't quite work yet

            # these work
            "dota-gsi-health": Machine(
                name="dota-GSI",
                iname="HEALTH",
                id="ltri-dota-gsi-health",
                desc="Machine State for DOTA Health"
            ),
            "dota-gsi-health-inv": Machine(
                name="dota-GSI",
                iname="HEALTH_INV",
                id="ltri-dota-gsi-health-inv",
                desc="Machine State for DOTA Health (inverted)"
            ),
            "dota-gsi-mana": Machine(
                name="dota-GSI",
                iname="MANA",
                id="ltri-dota-gsi-mana",
                desc="Machine State for DOTA Mana"
            ),
            "dota-gsi-mana-inv": Machine(
                name="dota-GSI",
                iname="MANA_INV",
                id="ltri-dota-gsi-mana-inv",
                desc="Machine State for DOTA Mana (inverted)"
            ),
            "dota-gsi-money": Machine(
                name="dota-GSI",
                iname="MONEY",
                id="ltri-dota-gsi-money",
                desc="Machine State for DOTA Money"
            ),
            "dota-gsi-money-inv": Machine(
                name="dota-GSI",
                iname="MONEY_INV",
                id="ltri-dota-gsi-money-inv",
                desc="Machine State for DOTA Money (inverted)"
            ),
        },
        speed_enum={"FHUNDREDTHS": .05}
    )
    # lol
    serialized = json.loads(json.dumps(schema, indent=4, default=pydantic_encoder))
    return serialized


webapp = Klein()


@webapp.route('/', methods=['POST'])
def index(request: Request):
    # print("h")
    content = json.loads(request.content.read())
    # print(json.dumps(content, indent=3))
    try:
        new_state = GameState(**content)

    except Exception as e:
        print(content)
        print(e)
        return "wew"

    # check for diffs
    # print(json.dumps(content, indent=3))
    # new_state
    wamp_component.state = new_state

    return "ok"


if __name__ == "__main__":
    from twisted.web.server import Site
    from twisted.internet import reactor, task

    import sys
    print(sys.path)

    reactor.listenTCP(8016, Site(webapp.resource()))
    run([wamp_component])
