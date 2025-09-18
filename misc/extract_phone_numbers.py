import re
from typing import List

def extract_phone_numbers(text: str) -> List[str]:
    """
    Extract phone numbers from the given text.
    
    This function uses regular expressions to identify and extract phone numbers in 
    various common formats from the provided text.
    
    Args:
        text (str): The input text from which to extract phone numbers.
    
    Returns:
        List[str]: A list of extracted phone numbers as strings.
    
    Examples:
        >>> extract_phone_numbers("Call me at (123) 456-7890 or 987-654-3210")
        ['(123) 456-7890', '987-654-3210']
        >>> extract_phone_numbers("No phone numbers here")
        []
    """
       
    # Pattern to match various phone number formats
    pattern = r'''
    (?:
        # International format with country code
        (?:\+\d{1,3}\s*)?
        # Optional area code in parentheses
        (?:\(?\d{3}\)?[\s.-]?)?
        # First part of the number
        \d{3}
        # Separator (space, dot, or hyphen)
        [\s.-]?
        # Second part of the number
        \d{4}
        |
        # Format for some European/international numbers
        \+\d{1,3}[\s.-]?\d{2}[\s.-]?\d{2}[\s.-]?\d{2}[\s.-]?\d{2}
    )
    '''
    
    # Using re.VERBOSE to allow for comments and whitespace in the pattern
    matches = re.findall(pattern, text, re.VERBOSE)
    
    # Clean up matches (remove extra whitespace)
    cleaned_matches = [re.sub(r'\s+', ' ', match).strip() for match in matches]
    
    return cleaned_matches


def test_extract_phone_numbers():
    """
    Test the extract_phone_numbers function with various test cases.
    """
    # Test case 1: Various US formats
    text1 = "Contact us at (123) 456-7890, 987-654-3210, or 555.123.4567"
    expected1 = ['(123) 456-7890', '987-654-3210', '555.123.4567']
    assert extract_phone_numbers(text1) == expected1
    
    # Test case 2: International formats
    text2 = "Call +1 (123) 456-7890 or +44 20 1234 5678"
    expected2 = ['+1 (123) 456-7890', '+44 20 1234 5678']
    assert extract_phone_numbers(text2) == expected2
    
    # Test case 3: Mixed formats in a paragraph
    text3 = """
    Please contact our support team at (123) 456-7890 or sales at 987.654.3210.
    For international inquiries: +1 123-456-7890.
    """
    expected3 = ['(123) 456-7890', '987.654.3210', '+1 123-456-7890']
    assert extract_phone_numbers(text3) == expected3
    
    # Test case 4: No phone numbers
    text4 = "This text contains no phone numbers"
    expected4 = []
    assert extract_phone_numbers(text4) == expected4
    
    # Test case 5: Error case - non-string input
    try:
        extract_phone_numbers(12345)
        assert False, "Expected TypeError was not raised"
    except TypeError:
        pass
    
    print("All tests passed!")


if __name__ == "__main__":
    # Run the test function
    test_extract_phone_numbers()
    
    # Additional example usage
    sample_text = """
    Contact information:
    - Customer Service: (800) 123-4567
    - Technical Support: 555-987-6543
    - International: +1 234-567-8901
    - UK Office: +44 20 7946 0958
    - Raw number: 1234567890
    """
    
    found_numbers = extract_phone_numbers(sample_text)
    print("Found phone numbers:")
    for number in found_numbers:
        print(f"- {number}")