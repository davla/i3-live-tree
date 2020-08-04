from unittest import TestCase

from i3_live_tree.tree_serializer import FOCUSED_COLOR, RESET

from .mocks import MockConSerializer


class SingleNodeSerializerTest(TestCase):
    def test_one_node(self):
        # Given
        node = MockConSerializer(name='Code', focused=False)

        # When
        actual = str(node)

        # Then
        self.assertEqual('Code', actual)

    def test_one_node_focused(self):
        # Given
        node = MockConSerializer(name='python', focused=True)

        # When
        actual = str(node)

        # Then
        self.assertEqual(f'{FOCUSED_COLOR}python{RESET}', actual)


class DepthTwoNodeSerializerTest(TestCase):
    def test_node_with_children(self):
        # Given
        node = MockConSerializer(layout='splith', nodes=iter((
            MockConSerializer(name='python'),
        )))

        # When
        actual = str(node)

        # Then
        self.assertEqual('splith\n  python', actual)

    def test_node_with_children_focused(self):
        # Given
        node = MockConSerializer(layout='splith', nodes=iter((
            MockConSerializer(name='python', focused=True),
        )))

        # When
        actual = str(node)

        # Then
        self.assertEqual(f'splith\n  {FOCUSED_COLOR}python{RESET}', actual)

    def test_node_focused_with_children(self):
        # Given
        node = MockConSerializer(layout='splith', focused=True, nodes=iter((
            MockConSerializer(name='python'),
        )))

        # When
        actual = str(node)

        # Then
        self.assertEqual(f'{FOCUSED_COLOR}splith{RESET}\n  python', actual)

    def test_node_with_two_children(self):
        # Given
        node = MockConSerializer(layout='tabbed', nodes=iter((
            MockConSerializer(name='Firefox'),
            MockConSerializer(name='Thunar', focused=True)
        )))

        # When
        actual = str(node)

        # Then
        self.assertEqual(f'tabbed\n  Firefox\n  {FOCUSED_COLOR}Thunar{RESET}',
                         actual)


class DepthThreeNodeSerializerTest(TestCase):
    def test_node_with_grandchildren(self):
        # Given
        node = MockConSerializer(layout='splith', nodes=iter((
            MockConSerializer(layout='splitv', nodes=iter((
                MockConSerializer(name='Firefox'),
            ))),
        )))

        # When
        actual = str(node)

        # Then
        self.assertEqual('splith\n  splitv\n    Firefox', actual)

    def test_node_depth_first(self):
        # Given
        node = MockConSerializer(layout='splith', nodes=iter((
            MockConSerializer(layout='stacked', focused=True, nodes=iter((
                MockConSerializer(name='exa'),
                MockConSerializer(name='wd')
            ))),
            MockConSerializer(name='python')
        )))

        # When
        actual = str(node)

        # Then
        self.assertEqual(f'splith\n  {FOCUSED_COLOR}stacked{RESET}\n    exa'
                         '\n    wd\n  python', actual)
