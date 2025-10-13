"""Test common scenarios for PyCards."""

import pycards
import random

from hypothesis import strategies, given, settings
from pycards.card import Deck, CardNumber, DEFAULT_SCORING

import logging

logger = logging.getLogger("PyCardsTesting")
logging.basicConfig()
logger.setLevel("DEBUG")

STANDARD_DECK_SIZE: int = 52


@settings(max_examples=20)
@given(n_cards=strategies.integers(min_value=1, max_value=30))
def test_draw(n_cards: int) -> None:
    _deck = Deck.build("deck")
    _ = pycards.deal_cards(deck=_deck, n_cards=n_cards, n_players=1)
    logger.debug(
        "TestDraw: Deck: %s, Expected: %s\n", len(_deck.cards), STANDARD_DECK_SIZE - n_cards
    )
    assert _deck.ncards_deck == STANDARD_DECK_SIZE - n_cards


@settings(max_examples=20)
@given(
    n_cards=strategies.integers(min_value=1, max_value=10),
    is_random=strategies.booleans(),
    new_deck=strategies.booleans(),
)
def test_discard(n_cards: int, new_deck: bool, is_random: bool):
    deck_orig = Deck.build("deck")
    _hand, *_ = pycards.deal_cards(deck=deck_orig, n_cards=20, n_players=1)

    if new_deck:
        discard_pile = Deck.build("discard", n_packs=0)
        assert not discard_pile.cards
        _hand.discard(n_cards=n_cards, to_deck=discard_pile, random=is_random)
        assert len(discard_pile.cards) == n_cards
        logger.debug(
            "TestDiscard: Deck: %s, Expected: %s\n",
            discard_pile.ncards_deck,
            n_cards,
        )
        assert discard_pile.ncards_deck == n_cards
    else:
        _hand.discard(n_cards=n_cards, random=is_random)
        logger.debug(
            "TestDiscard: Deck: %s, Expected: %s\n",
            deck_orig.ncards_deck,
            STANDARD_DECK_SIZE - 20 + n_cards,
        )
        print(len(deck_orig.cards))
        assert deck_orig.ncards_deck == STANDARD_DECK_SIZE - 20 + n_cards
    logger.debug(
        "TestDiscard: Hand: %s, Expected: %s\n", len(_hand.cards), 20 - n_cards
    )
    assert len(_hand.cards) == 20 - n_cards


@settings(max_examples=20)
@given(
    new_dict=strategies.booleans(),
    ace_high=strategies.booleans(),
    n_cards=strategies.integers(min_value=1, max_value=10),
)
def test_score(new_dict: bool, ace_high: bool, n_cards: int) -> None:
    my_deck = Deck.build("deck")
    if new_dict:
        dict_score: dict[CardNumber, int] = {}
        for key in DEFAULT_SCORING:
            dict_score[key] = random.randint(0, 30)
        for _ in range(n_cards):
            card = my_deck.draw()
            if not card:
                continue
            card.score(score_dict=dict_score)
    else:
        for _ in range(n_cards):
            card = my_deck.draw()
            if not card:
                continue
            card.score(ace_high=ace_high)
