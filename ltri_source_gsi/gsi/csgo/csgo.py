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

PREFIX = "com.lambentri.edge.la4.extservices.gsi.csgo"
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
        # yield session.publish(
        #     f"{SRC_PREFIX}ltri-csgo-gsi-de",
        #     []],
        #     id="ltri-csgo-gsi-de",
        #     options=options)
        yield session.publish(f"{SRC_PREFIX}ltri-csgo-gsi-health",
                              wamp_component.state.player.state.health_as_color() * LEDS_IN_ARRAY_DEFAULT,
                              id="ltri-csgo-gsi-health", options=options)
        yield session.publish(f"{SRC_PREFIX}ltri-csgo-gsi-health-inv",
                              wamp_component.state.player.state.health_as_color_inv() * LEDS_IN_ARRAY_DEFAULT,
                              id="ltri-csgo-gsi-health-inv", options=options)
        yield session.publish(f"{SRC_PREFIX}ltri-csgo-gsi-armor",
                              wamp_component.state.player.state.armor_as_color() * LEDS_IN_ARRAY_DEFAULT,
                              id="ltri-csgo-gsi-armor", options=options)
        yield session.publish(f"{SRC_PREFIX}ltri-csgo-gsi-armor-inv",
                              wamp_component.state.player.state.armor_as_color_inv() * LEDS_IN_ARRAY_DEFAULT,
                              id="ltri-csgo-gsi-armor-inv", options=options)
        yield session.publish(f"{SRC_PREFIX}ltri-csgo-gsi-money",
                              wamp_component.state.player.state.money_as_color() * LEDS_IN_ARRAY_DEFAULT,
                              id="ltri-csgo-gsi-money", options=options)
        yield session.publish(f"{SRC_PREFIX}ltri-csgo-gsi-money-inv",
                              wamp_component.state.player.state.money_as_color_inv() * LEDS_IN_ARRAY_DEFAULT,
                              id="ltri-csgo-gsi-money-inv", options=options)
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
            "cs-gsi-de": Machine(
                name="CSGO-GSI",
                iname="DE_",
                id="ltri-csgo-gsi-de",
                desc="Machine State for CSGO Defusal games"
            ),
            "cs-gsi-cs": Machine(
                name="CSGO-GSI",
                iname="CS_",
                id="ltri-csgo-gsi-cs",
                desc="Machine State for CSGO Hostage Rescue games"
            ),
            "cs-gsi-ar": Machine(
                name="CSGO-GSI",
                iname="AR_",
                id="ltri-csgo-gsi-ar",
                desc="Machine State for CSGO Arms Race games"
            ),
            "cs-gsi-dz": Machine(
                name="CSGO-GSI",
                iname="DZ_",
                id="ltri-csgo-gsi-dz",
                desc="Machine State for CSGO Danger Zone games"
            ),
            # these work
            "cs-gsi-health": Machine(
                name="CSGO-GSI",
                iname="HEALTH",
                id="ltri-csgo-gsi-health",
                desc="Machine State for CSGO Health"
            ),
            "cs-gsi-health-inv": Machine(
                name="CSGO-GSI",
                iname="HEALTH_INV",
                id="ltri-csgo-gsi-armor-inv",
                desc="Machine State for CSGO Health (inverted)"
            ),
            "cs-gsi-armor": Machine(
                name="CSGO-GSI",
                iname="ARMOR",
                id="ltri-csgo-gsi-armor",
                desc="Machine State for CSGO Health"
            ),
            "cs-gsi-armor-inv": Machine(
                name="CSGO-GSI",
                iname="ARMOR_INV",
                id="ltri-csgo-gsi-armor-inv",
                desc="Machine State for CSGO Health (inverted)"
            ),
            "cs-gsi-money": Machine(
                name="CSGO-GSI",
                iname="MONEY",
                id="ltri-csgo-gsi-money",
                desc="Machine State for CSGO Money"
            ),
            "cs-gsi-money-inv": Machine(
                name="CSGO-GSI",
                iname="MONEY_INV",
                id="ltri-csgo-gsi-money-inv",
                desc="Machine State for CSGO Money (inverted)"
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
    print("h")
    content = json.loads(request.content.read())
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

    reactor.listenTCP(8015, Site(webapp.resource()))
    run([wamp_component])
