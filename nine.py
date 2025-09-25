#!/usr/bin/env python3
"""
Nine - A program demonstrating interesting properties of the number 9
"""

def multiplication_table():
    """Display the multiplication table for 9"""
    print("Multiplication Table for 9:")
    print("=" * 25)
    for i in range(1, 11):
        result = 9 * i
        print(f"9 × {i:2d} = {result:2d}")
    print()

def digital_root_property():
    """Demonstrate the digital root property of multiples of 9"""
    print("Digital Root Property:")
    print("All multiples of 9 have a digital root of 9")
    print("=" * 40)
    
    def digital_root(n):
        while n >= 10:
            n = sum(int(digit) for digit in str(n))
        return n
    
    for i in range(1, 11):
        multiple = 9 * i
        root = digital_root(multiple)
        print(f"9 × {i:2d} = {multiple:3d} → digital root: {root}")
    print()

def nine_facts():
    """Display interesting facts about the number 9"""
    print("Interesting Facts about 9:")
    print("=" * 27)
    facts = [
        "9 is the largest single-digit number",
        "9 is a perfect square (3²)",
        "9 is a perfect cube root (∛729 = 9)",
        "In base 10, any number multiplied by 9 has digits that sum to 9",
        "9 appears in many mystical and cultural contexts",
        "A nonagon is a 9-sided polygon",
        "There are 9 planets in our solar system (including Pluto)",
        "9 is considered lucky in many cultures"
    ]
    
    for i, fact in enumerate(facts, 1):
        print(f"{i}. {fact}")
    print()

def check_divisibility_by_nine(number):
    """Check if a number is divisible by 9 using the digit sum rule"""
    digit_sum = sum(int(digit) for digit in str(abs(number)))
    return digit_sum % 9 == 0

def divisibility_test():
    """Demonstrate the divisibility rule for 9"""
    print("Divisibility Test for 9:")
    print("A number is divisible by 9 if the sum of its digits is divisible by 9")
    print("=" * 65)
    
    test_numbers = [18, 27, 45, 81, 123, 456, 999, 1234, 9876]
    
    for num in test_numbers:
        digit_sum = sum(int(digit) for digit in str(num))
        is_divisible = check_divisibility_by_nine(num)
        status = "✓" if is_divisible else "✗"
        print(f"{num:4d}: digit sum = {digit_sum:2d} → {status} {'divisible' if is_divisible else 'not divisible'}")
    print()

def main():
    """Main function to run all demonstrations"""
    print("🔢 Welcome to the Number Nine Program! 🔢")
    print("=" * 40)
    print()
    
    multiplication_table()
    digital_root_property()
    nine_facts()
    divisibility_test()
    
    print("Thanks for exploring the wonderful world of 9! 🎉")

if __name__ == "__main__":
    main()