from unittest.mock import Mock

from i3ipc.aio import Con

import i3_live_tree.tree_serializer  # noqa: F401


class MockConSerializer(Mock, Con):
    """Mock a generic i3ipc.aio.Con for serialization purposes

    This Mock is meant to ease testing of i3ipc.aio.Con serialization methods,
    which are mokey patched in i3_live_tree.tree_serializer.
    In order to achieve this, the mock inherits all the method implementations
    of i3ipc.aio.Con, most importantly the serialization ones. However,
    whatever is needed for serialization, both properties and methods, is
    mocked and can be injected in the constructor, in order to ease the
    creation of mock instances.
    """

    def __init__(self, *args, name=None, layout=None, focused=False,
                 nodes=iter(()), **kwargs):
        Mock.__init__(self, *args, **kwargs)

        self.focused = focused
        self.layout = layout
        self.name = name
        self.nodes = nodes
