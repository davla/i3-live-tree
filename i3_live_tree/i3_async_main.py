"""Handle i3 IPC events asynchronously

This module subscribes to some i3ipc events using asyncio
"""

import asyncio

from i3ipc import Event
from i3ipc.aio import Connection

from .i3_event_handlers import on_tick_event, on_window_event


async def i3_live_tree_main():
    """Subscribe to i3 events and awaiting the async loop"""
    i3 = await Connection().connect()
    i3.on(Event.WINDOW, on_window_event)
    i3.on(Event.TICK, on_tick_event)
    await i3.main()


def main():
    """Entry point for the module"""

    # Creating the asyncio loop with the main i3 loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(i3_live_tree_main())
    loop.close()
