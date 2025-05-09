"""
Unit tests for the core functionality of the Marshmallows application.
"""

import pytest
import datetime
from marshmallow_lib.core import MarshmallowManager


class TestMarshmallowManager:
    """Tests for the MarshmallowManager class."""
    
    def test_initialization(self):
        """Test that the manager initializes correctly."""
        manager = MarshmallowManager()
        
        # Initial state should be empty
        assert len(manager.questions) == 0
        assert len(manager.question_map) == 0
        assert len(manager.viewed_questions) == 0
        assert manager.next_id == 0
        
        # Session ID should be a UUID string
        assert isinstance(manager.session_id, str)
        
        # User ID should be a colored animal name
        assert isinstance(manager.user_id, str)
        assert ' ' in manager.user_id  # Should have a space between color and animal
        
    def test_add_question(self):
        """Test adding questions."""
        manager = MarshmallowManager()
        
        # Empty question should be rejected
        assert not manager.add_question("")
        assert not manager.add_question("   ")
        
        # Valid question should be added
        assert manager.add_question("Test question")
        assert len(manager.questions) == 1
        assert len(manager.question_map) == 1
        assert manager.questions[0]["text"] == "Test question"
        assert manager.questions[0]["id"] == 0
        assert manager.questions[0]["status"] == "approved"
        assert manager.questions[0]["highlighted"] is False
        assert manager.questions[0]["votes"] == 0
        
        # Next question should get ID = 1
        assert manager.add_question("Another test")
        assert manager.questions[1]["id"] == 1
        assert manager.next_id == 2
        
        # Question map should have O(1) access
        assert 0 in manager.question_map
        assert 1 in manager.question_map
        assert manager.question_map[0]["text"] == "Test question"
        assert manager.question_map[1]["text"] == "Another test"
    
    def test_get_random_question(self):
        """Test getting random questions."""
        manager = MarshmallowManager()
        
        # No questions should return None
        assert manager.get_random_question() is None
        
        # Add a question and get it
        manager.add_question("Test question")
        random_q = manager.get_random_question()
        assert random_q is not None
        assert random_q["text"] == "Test question"
        
        # After viewing all questions, viewed set should reset
        assert len(manager.viewed_questions) == 1
        random_q = manager.get_random_question()
        assert random_q is not None
        assert len(manager.viewed_questions) == 1  # Got the same question again
    
    def test_question_operations(self):
        """Test operations on questions (vote, highlight, status, delete)."""
        manager = MarshmallowManager()
        
        # Add a test question
        manager.add_question("Test question")
        q_id = 0
        
        # Test voting
        assert manager.vote_for_question(q_id)
        assert manager.question_map[q_id]["votes"] == 1
        assert manager.vote_for_question(q_id)
        assert manager.question_map[q_id]["votes"] == 2
        
        # Test non-existent question
        assert not manager.vote_for_question(999)
        
        # Test highlighting
        assert manager.highlight_question(q_id, True)
        assert manager.question_map[q_id]["highlighted"] is True
        assert manager.highlight_question(q_id, False)
        assert manager.question_map[q_id]["highlighted"] is False
        
        # Test status change
        assert manager.set_question_status(q_id, "pending")
        assert manager.question_map[q_id]["status"] == "pending"
        
        # Test deletion
        assert manager.delete_question(q_id)
        assert len(manager.questions) == 0
        assert len(manager.question_map) == 0
        assert q_id not in manager.question_map
    
    def test_sorted_questions(self):
        """Test getting sorted questions."""
        manager = MarshmallowManager()
        
        # Add questions with different timestamps and votes
        manager.add_question("First question")
        # Manually adjust timestamp to ensure order
        manager.question_map[0]["timestamp"] = datetime.datetime(2023, 1, 1)
        
        manager.add_question("Second question with votes")
        manager.question_map[1]["timestamp"] = datetime.datetime(2023, 1, 2)
        manager.question_map[1]["votes"] = 5
        
        manager.add_question("Third question")
        manager.question_map[2]["timestamp"] = datetime.datetime(2023, 1, 3)
        
        # Test newest sorting
        newest = manager.get_sorted_questions("newest")
        assert newest[0]["id"] == 2  # Most recent first
        assert newest[2]["id"] == 0  # Oldest last
        
        # Test votes sorting
        by_votes = manager.get_sorted_questions("votes")
        assert by_votes[0]["id"] == 1  # Most votes first
        
        # Test random sorting (just check it returns all questions)
        random_sort = manager.get_sorted_questions("random")
        assert len(random_sort) == 3
        
        # Test default sorting (if invalid sort method)
        default = manager.get_sorted_questions("invalid_sort")
        assert len(default) == 3
    
    def test_clear_all_questions(self):
        """Test clearing all questions."""
        manager = MarshmallowManager()
        
        # Add some questions
        manager.add_question("Q1")
        manager.add_question("Q2")
        manager.add_question("Q3")
        
        # View a question to populate viewed_questions
        random_q = manager.get_random_question()
        assert len(manager.viewed_questions) == 1
        
        # Clear all questions
        manager.clear_all_questions()
        assert len(manager.questions) == 0
        assert len(manager.question_map) == 0
        assert len(manager.viewed_questions) == 0
        assert manager.next_id == 0