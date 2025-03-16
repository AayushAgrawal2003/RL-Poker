import numpy as np
from collections import Counter
from itertools import combinations


def deal_card(current_cards,number_of_cards):
    cards = []
    for n in range(number_of_cards):
        card = (np.random.randint(1,13),np.random.randint(0,4))
        while card in current_cards:
            card = (np.random.randint(1,13),np.random.randint(0,4))

        current_cards.add(card)
        cards.append(card)
    return cards, current_cards


def get_card_representation(number, suit):
    suits = {0: "♠", 1: "♥", 2: "♦", 3: "♣"}
    numbers = {1: "A", 11: "J", 12: "Q", 13: "K"}
    
    card_number = numbers.get(number, str(number))  # Convert number to face card if applicable
    card_suit = suits.get(suit, "?")  # Get suit symbol
    
    return [
        "┌───┐",
        f"│{card_number:<2} │",
        f"│ {card_suit} │",
        f"│ {card_number:>2}│",
        "└───┘"
    ]

def print_cards_horizontally(cards):
    lines = ["" for _ in range(5)]  # Each card has 5 lines
    for card in cards:
        card_lines = get_card_representation(*card)
        for i in range(5):
            lines[i] += card_lines[i] + "  "  # Add spacing between cards
    
    for line in lines:
        print(line)

def evaluate_hand(hand):
    hand = sorted(hand, key=lambda x: x[0])
    numbers = [card[0] for card in hand]
    suits = [card[1] for card in hand]
    
    is_flush = len(set(suits)) == 1
    is_straight = (len(set(numbers)) == 5 and max(numbers) - min(numbers) == 4)
    
    if set(numbers) == {1, 10, 11, 12, 13}:  # A, 10, J, Q, K
        is_straight = True
    
    number_counts = Counter(numbers)
    counts = sorted(number_counts.values(), reverse=True)
    
    if is_flush and is_straight:
        return (9, max(numbers))  # Straight Flush
    elif counts == [4, 1]:
        return (8, max(number_counts, key=number_counts.get))  # Four of a Kind
    elif counts == [3, 2]:
        return (7, max(number_counts, key=number_counts.get))  # Full House
    elif is_flush:
        return (6, sorted(numbers, reverse=True))  # Flush
    elif is_straight:
        return (5, max(numbers))  # Straight
    elif counts == [3, 1, 1]:
        return (4, max(number_counts, key=number_counts.get))  # Three of a Kind
    elif counts == [2, 2, 1]:
        pairs = sorted([num for num, count in number_counts.items() if count == 2], reverse=True)
        return (3, pairs, max(number_counts, key=lambda x: (number_counts[x], x)))  # Two Pair
    elif counts == [2, 1, 1, 1]:
        return (2, max(number_counts, key=number_counts.get))  # One Pair
    else:
        return (1, sorted(numbers, reverse=True))  # High Card

def best_hand(community, hole):
    best = max(combinations(community + hole, 5), key=evaluate_hand)
    return best, evaluate_hand(best)

def best_two_hands(players_hands, community):
    evaluated_hands = [(best_hand(community, hole), hole) for hole in players_hands]
    evaluated_hands.sort(reverse=True, key=lambda x: x[0][1])
    return evaluated_hands[0][0][0], evaluated_hands[1][0][0] if len(evaluated_hands) > 1 else None


    
    