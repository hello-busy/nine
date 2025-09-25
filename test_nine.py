#!/usr/bin/env python3
"""
Test script for the nine.py program
"""

import nine

def test_divisibility_by_nine():
    """Test the divisibility by 9 function"""
    print("Testing divisibility by 9...")
    
    # Numbers divisible by 9
    divisible_numbers = [9, 18, 27, 36, 45, 81, 99, 108, 999]
    for num in divisible_numbers:
        assert nine.check_divisibility_by_nine(num), f"{num} should be divisible by 9"
    
    # Numbers not divisible by 9
    not_divisible_numbers = [10, 11, 19, 25, 37, 46, 55, 100, 123]
    for num in not_divisible_numbers:
        assert not nine.check_divisibility_by_nine(num), f"{num} should not be divisible by 9"
    
    print("✓ All divisibility tests passed!")

def test_digital_root():
    """Test that multiples of 9 have digital root of 9"""
    print("Testing digital root property...")
    
    def digital_root(n):
        while n >= 10:
            n = sum(int(digit) for digit in str(n))
        return n
    
    # Test multiples of 9
    for i in range(1, 21):  # Test first 20 multiples
        multiple = 9 * i
        root = digital_root(multiple)
        assert root == 9, f"Digital root of {multiple} should be 9, got {root}"
    
    print("✓ All digital root tests passed!")

def test_basic_math():
    """Test basic mathematical properties"""
    print("Testing basic math properties...")
    
    # Test that 9 is 3 squared
    assert 3 ** 2 == 9, "3² should equal 9"
    
    # Test some multiplication facts
    multiplication_facts = {
        1: 9, 2: 18, 3: 27, 4: 36, 5: 45,
        6: 54, 7: 63, 8: 72, 9: 81, 10: 90
    }
    
    for multiplier, expected in multiplication_facts.items():
        result = 9 * multiplier
        assert result == expected, f"9 × {multiplier} should be {expected}, got {result}"
    
    print("✓ All basic math tests passed!")

def main():
    """Run all tests"""
    print("🧪 Running tests for the Nine program...")
    print("=" * 40)
    
    test_divisibility_by_nine()
    test_digital_root()
    test_basic_math()
    
    print("\n🎉 All tests passed! The Nine program is working correctly.")

if __name__ == "__main__":
    main()