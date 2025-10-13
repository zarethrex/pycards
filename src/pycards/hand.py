"""Class defining a hand of cards."""

import random as rdm
from typing import Self

import pydantic

from .card import Card, Deck

__all__ = ["Hand"]


class Hand(pydantic.BaseModel):
    """Class representing cards in hand."""

    deck: Deck
    cards: list[Card]

    @classmethod
    @pydantic.validate_call
    def draw_hand(cls, *, deck: Deck, n_cards: pydantic.PositiveInt) -> Self:
        """Initialise a hand by drawing cards.

        Parameters
        ----------
        deck : Deck
            deck to draw from.
        n_cards : int
            number of cards to draw.

        Returns
        -------
        Hand
            hand of cards.
        """
        _deck: Deck = deck
        _cards: list[Card] = [deck.draw() for _ in range(n_cards)]
        return cls(deck=_deck, cards=_cards)

    def __add__(self, other: Self) -> Self:
        if self.deck != other.deck:
            raise ValueError("Hands must be drawn from the same deck.")
        return self.__class__(deck=self.deck, cards=self.cards + other.cards)

    def discard(
        self,
        n_cards: pydantic.PositiveInt,
        *,
        to_deck: Deck | None = None,
        random: bool = False,
    ) -> None:
        """Discard cards from the hand.

        Parameters
        ----------
        n_cards : int
            number of cards to discard.
        to_deck : Deck, optional
            discard to a deck, default is None.
        random : bool, optional
            discard randomly as opposed to from top, default is False.

        Returns
        -------
        Card
            discarded card
        """
        _target_deck: Deck = to_deck or self.deck
        for _ in range(n_cards):
            _draw_index: int = 0 if not random else rdm.randint(0, len(self.cards) - 1)
            _target_deck += self.cards[_draw_index]
            self.cards.pop(_draw_index)

