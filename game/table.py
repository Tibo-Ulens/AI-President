from __future__ import annotations

from random import shuffle
from typing import TYPE_CHECKING, List, Optional, Tuple

from game.deck import Deck

if TYPE_CHECKING:
    from game.agent import Agent
    from game.card import Card
    from game.president import President


class Table:
    def __init__(self, game: President):
        self.game = game
        self.current: int = 0
        self.deck = Deck()
        self.played_cards: List[Tuple[List[Card], Agent]] = []
        self.discard_pile: List[List[Card]] = []

    def reset(self) -> None:
        """
        Reset the table:
        - reset played_cards
        - reset discard_pile
        """
        self.played_cards.clear()
        self.discard_pile.clear()

    def new_trick(self) -> None:
        """
        Move the cards from the played_cards to the discard_pile.
        """
        self.discard_pile += self.played_cards
        self.played_cards.clear()

    def try_move(self, agent: Agent, cards: List[Card]) -> Tuple[int, bool]:
        """
        Take a move from an agent, execute the move on the table and give a reward to the agent.
        Validate if the move is valid first.

        TODO: discuss this.
        TODO: move rewards to settings file.
        Reward scheme:
        - Invalid move: -10
        - else return game specific reward

        return the reward and if the move is final.
        """
        # A pass is a valid move.
        if len(cards) != 0:
            # WARNING: when playing with 2 decks of cards this is not sufficient.
            if not all(card in agent.player.hand for card in cards):
                return -10, False

        return self.game.on_move(agent, cards)

    def do_move(self, agent: Agent, cards: List[Card]) -> None:
        # The move is valid, the cards can be moved from the players hand to the table. If the play was not a pass.
        if cards:
            [agent.player.hand.remove(card) for card in cards]
            self.played_cards.append((cards, agent))

    def last_move(self) -> Optional[Tuple[List[Card], Agent]]:
        """
        Get the last move
        """
        return self.played_cards[-1] if len(self.played_cards) > 0 else None

    def divide(self, nr_players: int) -> List[List[Card]]:
        """
        Shuffle and Divide all cards in as there are players, indicated by nr_players
        """
        shuffle(self.deck.card_stack)
        result = [[] for _ in range(nr_players)]
        for i in range(len(self.deck.card_stack)):
            result[i % nr_players].append(self.deck.card_stack[i])
        return result
