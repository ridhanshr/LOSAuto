"""
Card Generator Utility
Generates valid test card numbers using Luhn algorithm.
Similar functionality to https://paymentcardtools.com/test-card-generator

Usage:
    from src.utils.card_generator import generate_cards, generate_single_card
    
    # Generate multiple cards
    cards = generate_cards(prefix="4532", start_number=1000, count=10)
    
    # Generate single card
    card = generate_single_card(prefix="4532", account_number="123456789")
"""

from typing import List, Dict, Optional
from datetime import datetime
import random


def calculate_luhn_checksum(partial_card: str) -> int:
    """
    Calculate the Luhn checksum digit for a partial card number.
    
    Args:
        partial_card: Card number without the check digit
        
    Returns:
        The check digit (0-9)
    """
    digits = [int(d) for d in partial_card]
    
    # Process from right to left (starting from second-to-last digit)
    for i in range(len(digits) - 1, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    
    total = sum(digits)
    check_digit = (10 - (total % 10)) % 10
    
    return check_digit


def validate_card_number(card_number: str) -> bool:
    """
    Validate a card number using the Luhn algorithm.
    
    Args:
        card_number: Full card number to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not card_number.isdigit():
        return False
    
    digits = [int(d) for d in card_number]
    
    # Process from right to left, doubling every second digit
    for i in range(len(digits) - 2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    
    return sum(digits) % 10 == 0


def generate_single_card(
    prefix: str,
    account_number: Optional[str] = None,
    card_length: int = 16
) -> Dict[str, str]:
    """
    Generate a single valid test card number.
    
    Args:
        prefix: Card prefix/BIN (e.g., "4532" for Visa, "5425" for Mastercard)
        account_number: Optional account identifier, will be padded or truncated
        card_length: Total length of the card number (default: 16)
        
    Returns:
        Dictionary containing card details
    """
    # Calculate how many digits we need for the account number
    # prefix + account_number + check_digit = card_length
    account_length = card_length - len(prefix) - 1
    
    if account_number is None:
        # Generate random account number
        account_number = ''.join([str(random.randint(0, 9)) for _ in range(account_length)])
    else:
        # Pad or truncate account number
        account_number = account_number.zfill(account_length)[:account_length]
    
    # Build partial card number (without check digit)
    partial_card = prefix + account_number
    
    # Calculate check digit
    check_digit = calculate_luhn_checksum(partial_card)
    
    # Full card number
    card_number = partial_card + str(check_digit)
    
    return {
        "card_number": card_number,
        "prefix": prefix,
        "account_number": account_number,
        "check_digit": str(check_digit),
        "is_valid": validate_card_number(card_number),
        "card_length": len(card_number)
    }


def generate_cards(
    prefix: str,
    start_number: int = 0,
    count: int = 10,
    card_length: int = 16
) -> List[Dict[str, str]]:
    """
    Generate multiple valid test card numbers.
    
    Args:
        prefix: Card prefix/BIN (e.g., "4532" for Visa, "5425" for Mastercard)
        start_number: Starting account number (will increment from here)
        count: Number of cards to generate
        card_length: Total length of the card number (default: 16)
        
    Returns:
        List of dictionaries containing card details
    """
    cards = []
    
    for i in range(count):
        account_number = str(start_number + i)
        card = generate_single_card(
            prefix=prefix,
            account_number=account_number,
            card_length=card_length
        )
        card["sequence"] = i + 1
        cards.append(card)
    
    return cards


def generate_cards_with_expiry(
    prefix: str,
    start_number: int = 0,
    count: int = 10,
    card_length: int = 16,
    expiry_years_ahead: int = 3
) -> List[Dict[str, str]]:
    """
    Generate test cards with expiry date and CVV.
    
    Args:
        prefix: Card prefix/BIN
        start_number: Starting account number
        count: Number of cards to generate
        card_length: Total card number length
        expiry_years_ahead: How many years ahead for expiry date
        
    Returns:
        List of card details with expiry and CVV
    """
    cards = generate_cards(prefix, start_number, count, card_length)
    
    # Generate expiry date
    current_date = datetime.now()
    expiry_month = str(random.randint(1, 12)).zfill(2)
    expiry_year = str(current_date.year + expiry_years_ahead)[-2:]
    
    for card in cards:
        card["expiry_month"] = expiry_month
        card["expiry_year"] = expiry_year
        card["expiry_date"] = f"{expiry_month}/{expiry_year}"
        card["cvv"] = ''.join([str(random.randint(0, 9)) for _ in range(3)])
    
    return cards


def get_card_brand(prefix: str) -> str:
    """
    Identify card brand based on prefix.
    
    Args:
        prefix: Card prefix/BIN
        
    Returns:
        Card brand name
    """
    prefix_2 = prefix[:2] if len(prefix) >= 2 else prefix
    prefix_4 = prefix[:4] if len(prefix) >= 4 else prefix
    
    # Visa
    if prefix[0] == '4':
        return "Visa"
    
    # Mastercard
    if prefix_2 in ['51', '52', '53', '54', '55']:
        return "Mastercard"
    if len(prefix) >= 4:
        try:
            p4 = int(prefix_4)
            if 2221 <= p4 <= 2720:
                return "Mastercard"
        except ValueError:
            pass
    
    # American Express
    if prefix_2 in ['34', '37']:
        return "American Express"
    
    # Discover
    if prefix_4 == '6011' or prefix_2 == '65':
        return "Discover"
    
    # JCB
    if len(prefix) >= 4:
        try:
            p4 = int(prefix_4)
            if 3528 <= p4 <= 3589:
                return "JCB"
        except ValueError:
            pass
    
    # Diners Club
    if prefix_2 in ['36', '38'] or prefix[:3] in ['300', '301', '302', '303', '304', '305']:
        return "Diners Club"
    
    return "Unknown"


def format_card_number(card_number: str, separator: str = " ") -> str:
    """
    Format card number with separators for display.
    
    Args:
        card_number: The card number to format
        separator: Character to use as separator (default: space)
        
    Returns:
        Formatted card number
    """
    # Standard 16-digit format: XXXX XXXX XXXX XXXX
    if len(card_number) == 16:
        return separator.join([card_number[i:i+4] for i in range(0, 16, 4)])
    # Amex 15-digit format: XXXX XXXXXX XXXXX
    elif len(card_number) == 15:
        return f"{card_number[:4]}{separator}{card_number[4:10]}{separator}{card_number[10:]}"
    else:
        return card_number


# Convenience functions for popular card types
def generate_visa_cards(start_number: int = 0, count: int = 10) -> List[Dict[str, str]]:
    """Generate Visa test cards (prefix: 4532)"""
    return generate_cards(prefix="4532", start_number=start_number, count=count)


def generate_mastercard_cards(start_number: int = 0, count: int = 10) -> List[Dict[str, str]]:
    """Generate Mastercard test cards (prefix: 5425)"""
    return generate_cards(prefix="5425", start_number=start_number, count=count)


def generate_amex_cards(start_number: int = 0, count: int = 10) -> List[Dict[str, str]]:
    """Generate American Express test cards (prefix: 3714)"""
    return generate_cards(prefix="3714", start_number=start_number, count=count, card_length=15)


# Example/Test usage
# if __name__ == "__main__":
#     print("=" * 60)
#     print("Card Generator Test")
#     print("=" * 60)
    
    # Generate 5 Visa cards starting from account number 1000
    # print("\n[Visa Cards]")
    # visa_cards = generate_cards(prefix="46874002", start_number=1000, count=5)
    # for card in visa_cards:
    #     print(f"  {card['sequence']}. {card['card_number']} (Valid: {card['is_valid']})")
    
    # Generate cards with expiry and CVV
    # print("\n[Cards with Expiry & CVV]")
    # full_cards = generate_cards_with_expiry(prefix="5425", start_number=2000, count=3)
    # for card in full_cards:
    #     formatted = format_card_number(card["card_number"])
    #     print(f"  {card['sequence']}. {formatted} | Exp: {card['expiry_date']} | CVV: {card['cvv']}")


