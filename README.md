# pycards    
[![MIT Licence](https://badges.frapsoft.com/os/mit/mit.png?v=103)](https://opensource.org/licenses/mit-license.php)

A module consisting of objects to represent a standard pack of 52 playing cards.

## The Basics

The best way to show the capability of the module is to demonstrate it through examples. The `Deck` object by default initialises the standard 52 card deck including shuffling.

```python
from pycards import Deck

my_deck = Deck()

my_deck.shuffle() # For those few who require an extra reshuffle ;
```

From the deck we can either draw individual cards:

```python
# Draw cards from the top of the deck as opposed to randomly
# This is default behaviour.
# Also return the card to the deck when finished and reshuffle

my_card = my_deck.draw(from_top=True, replace=True)
print(my_card)
my_deck.reshuffle()
```
or deal a number of cards to a number of players utilising the `Hand` class:

```python
cards_per_player  = 7
number_of_players = 3

hands = my_deck.deal(cards_per_player, number_of_players)
```
here `hands` would be a list of objects of type `Hand`.

## More Advanced Methods

### Combining Hands

We can add hands together. The cards from hand are combined with another to form a new hand.
```python
from pycards import Deck

my_deck = Deck()

hand_a = my_deck.draw_hand(cards_per_player) # Only want a single hand
hand_b = my_deck.draw_hand(cards_per_player)

new_hand = hand_a + hand_b
```

### Scoring Cards

In games where rank of a card leads to scoring you can use the `score` function of the `Card` class:

```python
from pycards import Deck

my_deck = Deck()

card = my_deck.draw()

# Score using Ace-High
# (i.e. Ace = 11 as opposed to the default of 1)

print(card.score(ace_high=True)
```
in addition you can create your own scoring dictionary which will be used instead:

```python
new_scores = {'A' : 5, 'K' : 2, ...}

card.score(score_dict=new_scores)
```

### Discarding Cards

In a game where cards are discarded you will need to create an empty discard pile to which the cards are sent:

```python
from pycards import Deck

my_deck = Deck()
discard_pile = Deck(empty=True)

hand = my_deck.draw_hand(6)

# Discard the top card back to the parent deck
hand.discard(1)

# Discard a card at random to the discard pile
hand.discard(1, to_deck=discard_pile, random=True)
```

## Testing
| Branch | Test Status |
|--------|-------------|
| main | [![CI](https://github.com/zarethrex/pycards/actions/workflows/test_build.yml/badge.svg?branch=main)](https://github.com/zarethrex/pycards/actions/workflows/test_build.yml)|