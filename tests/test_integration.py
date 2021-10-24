import json
import sys
from contextlib import contextmanager
from io import StringIO
from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock

from i3_live_tree.i3_event_handlers import (WINDOW_EVENT_CHANGE, on_tick_event,
                                            on_window_event)

from .mocks import MockCon, MockI3


@contextmanager
def record_stdout():
    mock_stdout = StringIO()
    try:
        sys.stdout = mock_stdout
        yield mock_stdout
    finally:
        sys.stdout = sys.__stdout__


class EventIntegrationTest(IsolatedAsyncioTestCase):
    def setUp(self):
        self.i3 = MockI3(tree=None)

    async def test_window_event_ignored(self):
        # Given
        self.i3.tree = MockCon(name='python')
        event = Mock(**{
            'change': 'title',
            'container': self.i3.tree
        })

        # When
        with record_stdout() as stdout:
            await on_window_event(self.i3, event)

        # Then
        self.assertEqual('', stdout.getvalue().strip())

    async def test_no_workspace(self):
        # Given
        self.i3.tree = MockCon(name='splith', nodes=iter((
            Mock(**{
                'workspace.return_value': None
            })
        ,)))
        event = Mock(**{
            'change': 'title',
            'container': self.i3.tree
        })


        # When
        with record_stdout() as stdout:
            await on_window_event(self.i3, event)

        # Then
        self.assertEqual('', stdout.getvalue().strip())



#     async def test_window_event_change(self):
#         for change in WINDOW_EVENT_CHANGE:
#             with self.subTest():
#                 # Given
#                 self.window.reset_mock()
#                 event = Mock(**{
#                     'change': change,
#                     'container': self.window
#                 })

#                 # When
#                 await on_window_event(self.i3, event)

#                 # Then
#                 self.window.workspace().__str__.assert_called_once()


# class TickHandlerTest(IsolatedAsyncioTestCase):
#     def setUp(self):
#         self.window = MockConNavigation()
#         self.i3 = MockI3(tree=self.window)

#     async def test_malformed_payload(self):
#         # Given
#         event = Mock(**{
#             'payload': 'This [is not} json'
#         })


#         # When
#         await on_tick_event(self.i3, event)

#         # Then
#         self.window.workspace().__str__.assert_not_called()

#     async def test_invalid_payload(self):
#         # Given
#         event = Mock(**{
#             'payload': json.dumps({
#                 'bad_key': 'bad_value'
#             })
#         })

#         # When
#         await on_tick_event(self.i3, event)

#         # Then
#         self.window.workspace().__str__.assert_not_called()

#     async def test_alien_tick_event(self):
#         # Given
#         event = Mock(**{
#             'payload': json.dumps({
#                 'is_alien': True
#             })
#         })

#         # When
#         await on_tick_event(self.i3, event)

#         # Then
#         self.window.workspace().__str__.assert_not_called()

#     async def test_own_tick_event(self):
#         # Given
#         event = Mock(**{
#             'payload': json.dumps({
#                 'is_live_tree': True
#             })
#         })

#         # When
#         await on_tick_event(self.i3, event)

#         # Then
#         self.window.workspace().__str__.assert_called_once()
