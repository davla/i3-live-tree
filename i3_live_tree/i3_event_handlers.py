"""Handle events from i3ipc

This module defines handlers for i3ipc WINDOW and TICK events which redraw the
focused workspace. It also defines the payload for the TICK event.
"""
import json
from json.decoder import JSONDecodeError
from typing import Type, TypeVar

from i3ipc import TickEvent, WindowEvent
from i3ipc.aio import Con, Connection

import i3_live_tree.tree_serializer  # noqa: F401

"""List the window events that actually change the tree"""
WINDOW_EVENT_CHANGE = ('close', 'floating', 'focus', 'fullscreen_mode', 'move',
                       'new',)


TickPayloadClass = TypeVar('TickPayloadClass', bound='TickPayload')
TickPayloadType = Type[TickPayloadClass]


class TickPayload:
    """The payload of a TICK event"""
    is_live_tree: bool

    def __init__(self, is_live_tree: bool):
        self.is_live_tree = is_live_tree

    @classmethod
    def parse(cls: TickPayloadType, input: dict) -> TickPayloadType:
        """Create a TickPayload from a dict"""
        return cls(**input)


def print_active_workspace(tree: Con) -> None:
    """Draw the currently active workspace"""
    workspace = tree.find_focused().workspace()
    if workspace:
        print(str(workspace))


async def on_window_event(i3: Connection, event: WindowEvent) -> None:
    """Draw the event's window workspace

    This function redraws the workspace containing the window that triggered
    the event. Only events that actually affect the layout serialization are
    considered.
    """
    if event.change in WINDOW_EVENT_CHANGE:
        print_active_workspace(await i3.get_tree())


async def on_tick_event(i3: Connection, event: TickEvent) -> None:
    """Draw the workspace containing the focused window

    This function redraws the workspace containing the focused window. However,
    this only occurs if the event payload conforms to a specific schema.
    """
    try:
        payload = json.loads(event.payload, object_hook=TickPayload.parse)
        if payload.is_live_tree:
            print_active_workspace(await i3.get_tree())
    except (JSONDecodeError, TypeError):
        pass
