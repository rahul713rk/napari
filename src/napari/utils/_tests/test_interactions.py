import sys

import pytest

from napari.utils.interactions import Shortcut


@pytest.mark.parametrize(
    ('shortcut', 'reason'),
    [
        ('Atl-A', 'Alt misspelled'),
        ('Ctrl-AA', 'AA makes no sense'),
        ('BB', 'BB makes no sense'),
    ],
)
def test_shortcut_invalid(shortcut, reason):
    with pytest.warns(UserWarning, match='does not seem to be a valid'):
        Shortcut(shortcut)  # Should be Control-A


def test_minus_shortcut():
    """
    Misc tests minus is properly handled as it is the delimiter
    """
    assert str(Shortcut('-')) == '-'
    assert str(Shortcut('Control--')).endswith('-')
    assert str(Shortcut('Shift--')).endswith('-')


def test_shortcut_qt():
    assert Shortcut('Control-A').qt == 'Ctrl+A'


@pytest.mark.skipif(
    sys.platform != 'darwin', reason='Parsing macos specific keys'
)
@pytest.mark.parametrize(
    ('expected', 'shortcut'),
    [
        ('␣', 'Space'),
        ('⌥', 'Alt'),
        ('⌥-', 'Alt--'),
        ('⌘', 'Meta'),
        ('⌘-', 'Meta--'),
        ('⌘⌥', 'Meta-Alt'),
        ('⌥⌘P', 'Meta-Alt-P'),
    ],
)
def test_partial_shortcuts(shortcut, expected):
    assert str(Shortcut(shortcut)) == expected
