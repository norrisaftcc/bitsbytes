"""
Doctests for the core functionality of the Marshmallows application.

This module uses the doctest module to test the MarshmallowManager class.
"""

import doctest
from marshmallow_lib.core import MarshmallowManager


def test_marshmallow_manager():
    """
    Tests for the MarshmallowManager class.
    
    >>> manager = MarshmallowManager()
    >>> len(manager.questions)
    0
    
    >>> len(manager.question_map)
    0
    
    >>> manager.next_id
    0
    
    >>> manager.add_question("")  # Empty questions should be rejected
    False
    
    >>> manager.add_question("Test question")  # Valid question should be added
    True
    
    >>> len(manager.questions)
    1
    
    >>> manager.questions[0]["text"]
    'Test question'
    
    >>> manager.questions[0]["id"]
    0
    
    >>> manager.questions[0]["status"]
    'approved'
    
    >>> manager.questions[0]["highlighted"]
    False
    
    >>> manager.questions[0]["votes"]
    0
    
    >>> 0 in manager.question_map  # Question map should have O(1) access
    True
    
    >>> manager.question_map[0]["text"]
    'Test question'
    
    >>> manager.vote_for_question(0)  # Test voting
    True
    
    >>> manager.question_map[0]["votes"]
    1
    
    >>> manager.vote_for_question(999)  # Non-existent question
    False
    
    >>> manager.highlight_question(0, True)  # Test highlighting
    True
    
    >>> manager.question_map[0]["highlighted"]
    True
    
    >>> manager.set_question_status(0, "pending")  # Test status change
    True
    
    >>> manager.question_map[0]["status"]
    'pending'
    
    >>> random_q = manager.get_random_question()  # Test getting random questions
    >>> random_q is None or random_q["text"] == "Test question"
    True
    
    >>> manager.add_question("Another question")  # Add another question
    True
    
    >>> len(manager.questions)
    2
    
    >>> sorted_by_newest = manager.get_sorted_questions("newest")
    >>> len(sorted_by_newest)
    2
    
    >>> sorted_by_votes = manager.get_sorted_questions("votes")
    >>> len(sorted_by_votes)
    2
    
    >>> manager.clear_all_questions()  # Test clearing all questions
    >>> len(manager.questions)
    0
    
    >>> len(manager.question_map)
    0
    
    >>> manager.next_id
    0
    """
    return doctest.testmod()


if __name__ == "__main__":
    test_marshmallow_manager()