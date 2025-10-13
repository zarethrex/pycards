"""Methods for commencing gameplay."""

import pydantic

from .card import Deck
from .hand import Hand


@pydantic.validate_call
def deal_cards(
    deck: Deck, *, n_cards: pydantic.PositiveInt, n_players: pydantic.PositiveInt
) -> tuple[Hand, ...]:
    """Deal hands to players from a deck.

    Parameters
    ----------
    deck : Deck
        deck to deal from
    n_cards : int
        number of cards to draw
    n_players : int
        number of players to draw for

    Returns
    -------
    tuple[Hand, ...]
        drawn hands
    """
    return tuple(Hand.draw_hand(deck=deck, n_cards=n_cards) for _ in range(n_players))
