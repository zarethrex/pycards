"""Pycards Card definitions."""

import contextlib
import itertools
import uuid
from typing import Annotated, Literal

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self  # noqa: UP035

import pydantic

CardNumber = Annotated[int, pydantic.Field(ge=2, le=10)] | Literal["A", "K", "Q", "J"]
CardSuit = Literal["H", "S", "D", "C"]

DEFAULT_SCORING: dict[CardNumber, int] = {"A": 1, "K": 10, "Q": 10, "J": 10} | {
    n: n for n in range(2, 11)
}

__all__ = ["Card", "Deck"]


class Card(pydantic.BaseModel):
    """Class representing a single playing card."""

    model_config = pydantic.ConfigDict(frozen=True, extra="forbid", strict=True)
    suit: Literal["H", "D", "C", "S"]
    rank: CardNumber

    def __str__(self) -> str:
        """Return string representation of card."""
        return f"{self.suit}{self.rank}"

    def __eq__(self, other: object) -> bool:
        """Compare two cards."""
        if not isinstance(other, Card):
            _out_msg: str = (
                "Unsupported operands for == "
                f"({self.__class__.__name__}, {type(other)})"
            )
            raise TypeError(_out_msg)
        return self.suit == other.suit and self.rank == other.rank

    def __hash__(self) -> int:
        """Hash for this card."""
        return hash((self.suit, self.rank))

    def score(
        self,
        *,
        ace_high: bool = False,
        score_dict: dict[CardNumber, int] = DEFAULT_SCORING,
    ) -> int:
        """Return the score for this card.

        Parameters
        ----------
        ace_high : bool, optional
            whether Ace should rank high, default False.
        score_dict : dict[str | int, int], optional
            the score mapping.

        Returns
        -------
        int
            the score for this card.
        """
        if ace_high and self.rank == "A":
            return 11
        return score_dict[self.rank]


@pydantic.validate_call
def build_deck(n_packs: pydantic.NonNegativeInt) -> list[Card]:
    """Build a deck of cards.

    Parameters
    ----------
    n_packs : int
        number of standard 52 card packs.

    Returns
    -------
    list[Card]
        deck of cards
    """
    if not n_packs:
        return []
    return n_packs * [
        Card(suit=suit, rank=number)
        for suit, number in itertools.product(
            ("H", "D", "S", "C"), DEFAULT_SCORING.keys()
        )
    ]


class Deck(pydantic.BaseModel):
    """Class representing a deck of cards."""

    name: str = pydantic.Field(f"{uuid.uuid4()}")
    cards: list[Card]
    drawn: list[Card]

    @classmethod
    @pydantic.validate_call
    def build(
        cls, name: str | None = None, *, n_packs: pydantic.NonNegativeInt = 1
    ) -> Self:
        """Create a new deck.

        By default this will create a single deck of 52 cards.

        Parameters
        ----------
        name : str
            name for this deck
        n_packs: bool, optional
            number of packs of 52 cards to use to form deck.
        """
        return cls(name=name or f"{uuid.uuid4()}", cards=build_deck(n_packs), drawn=[])

    def __str__(self) -> str:
        """Return string representation of deck."""
        _cards_in_deck = [str(card) for card in self.cards if card not in self.drawn]
        return f"{self.name}{_cards_in_deck}"

    @pydantic.validate_call
    def draw(self, *, from_bottom: bool = False, replace: bool = False) -> Card:
        """Draw cards from this deck.

        Parameters
        ----------
        from_bottom : bool, optional
            whether to draw cards from the bottom rather than the top, default False.
        replace : bool, optional
            whether to replace the cards to the used area of the deck
            or discard permanently, default is False.

        Returns
        -------
        Card
            the drawn card.
        """
        for i in range(len(self.cards)):
            _front = self.cards[i]
            _back = self.cards[-i]

            if from_bottom and _front not in self.drawn:
                _card = self.cards.pop(i)
                if replace:
                    self.drawn.append(_card)
                return _card
            if not from_bottom and _back not in self.drawn:
                _card = self.cards.pop(-i)
                if replace:
                    self.drawn.append(_card)
                return _card
        raise ValueError("No cards remaining.")

    def __add__(self, other: Self | Card) -> Self:
        if isinstance(other, Deck):
            return self.__class__(
                name=self.name,
                cards=self.cards + other.cards,
                drawn=[card for card in self.drawn if card in other.drawn],
            )
        _cards = list(self.cards)
        _drawn = list(self.drawn)

        with contextlib.suppress(ValueError):
            _drawn.remove(other)

        if other not in _cards:
            _cards.append(other)

        return self.__class__(name=self.name, cards=_cards, drawn=_drawn)

    def __iadd__(self, other: Self | Card) -> Self:
        if isinstance(other, Deck):
            return self.__class__(
                name=self.name,
                cards=self.cards + other.cards,
                drawn=[card for card in self.drawn if card in other.drawn],
            )

        with contextlib.suppress(ValueError):
            self.drawn.remove(other)

        if other not in self.cards:
            self.cards.append(other)
        return self

    @property
    def ncards_deck(self) -> int:
        """Return number of cards remaining in the deck."""
        return len(self.cards) - len(self.drawn)

    @property
    def ncards_draw(self) -> int:
        """Return number of cards drawn from deck."""
        return len(self.drawn)
