"""
Core functionality for the Marshmallows anonymous questions app.

This module contains the shared business logic that can be used by different
front-end interfaces (Streamlit GUI, console GUI, etc.).
"""

import datetime
import random
import uuid
import json
import os
from pathlib import Path
from typing import Dict, List, Set, Optional, Any, Union


class MarshmallowManager:
    """Manages marshmallow questions with various operations."""
    
    def __init__(self, storage_type: str = "memory"):
        """
        Initialize the Marshmallow Manager.
        
        Args:
            storage_type: Type of storage to use ("memory" or "file")
        """
        self.questions = []
        self.question_map = {}  # Dictionary for O(1) lookups by ID
        self.viewed_questions = set()
        self.storage_type = storage_type
        self.storage_path = Path("marshmallow_data.json")
        self.next_id = 0  # Track the next ID to use
        
        # Generate a unique session ID
        self.session_id = str(uuid.uuid4())
        
        # Create a random user ID
        self.user_id = self._generate_user_id()
        
        # Load questions if using file storage
        if self.storage_type == "file" and self.storage_path.exists():
            self.load_questions()
    
    def _generate_user_id(self) -> str:
        """Generate a random user identifier (colored animal name)."""
        animal_names = ["Dolphin", "Penguin", "Tiger", "Elephant", "Koala", 
                        "Flamingo", "Panda", "Zebra", "Fox", "Owl"]
        colors = ["Red", "Blue", "Green", "Purple", "Golden", 
                 "Silver", "Orange", "Teal", "Emerald", "Azure"]
        return f"{random.choice(colors)} {random.choice(animal_names)}"
    
    def add_question(self, question_text: str, user_id: Optional[str] = None) -> bool:
        """
        Add a new question.
        
        Args:
            question_text: The text of the question
            user_id: Optional user identifier (uses self.user_id if None)
            
        Returns:
            bool: True if question was added, False otherwise
        """
        if not question_text.strip():
            return False
            
        if user_id is None:
            user_id = self.user_id
        
        # Use the next available ID
        question_id = self.next_id
        self.next_id += 1
            
        question = {
            "id": question_id,
            "text": question_text,
            "timestamp": datetime.datetime.now(),
            "status": "approved",  # All questions are immediately approved
            "user_id": user_id,
            "highlighted": False,
            "votes": 0
        }
        
        # Add to both list and map
        self.questions.append(question)
        self.question_map[question_id] = question
        
        # Save to file if using file storage
        if self.storage_type == "file":
            self.save_questions()
            
        return True
    
    def get_random_question(self) -> Optional[Dict]:
        """
        Get a random approved question.
        
        Returns:
            Dict or None: A random question or None if no questions available
        """
        approved_questions = [q for q in self.questions if q["status"] == "approved"]
        if not approved_questions:
            return None
        
        # Filter out recently viewed questions unless all have been viewed
        unviewed = [q for q in approved_questions if q["id"] not in self.viewed_questions]
        if not unviewed and approved_questions:
            # Reset viewed questions if all have been seen
            self.viewed_questions = set()
            unviewed = approved_questions
        
        if unviewed:
            question = random.choice(unviewed)
            self.viewed_questions.add(question["id"])
            return question
        return None
    
    def vote_for_question(self, question_id: int) -> bool:
        """
        Increment votes for a question.
        
        Args:
            question_id: ID of the question to vote for
            
        Returns:
            bool: True if vote successful, False otherwise
        """
        # O(1) lookup using dictionary
        if question_id in self.question_map:
            self.question_map[question_id]["votes"] += 1
            if self.storage_type == "file":
                self.save_questions()
            return True
        return False
    
    def highlight_question(self, question_id: int, highlighted: bool = True) -> bool:
        """
        Set highlight status for a question.
        
        Args:
            question_id: ID of the question
            highlighted: Whether to highlight or unhighlight
            
        Returns:
            bool: True if successful, False otherwise
        """
        # O(1) lookup using dictionary
        if question_id in self.question_map:
            self.question_map[question_id]["highlighted"] = highlighted
            if self.storage_type == "file":
                self.save_questions()
            return True
        return False
    
    def set_question_status(self, question_id: int, status: str) -> bool:
        """
        Change status of a question.
        
        Args:
            question_id: ID of the question
            status: New status ("approved", "pending", etc.)
            
        Returns:
            bool: True if successful, False otherwise
        """
        # O(1) lookup using dictionary
        if question_id in self.question_map:
            self.question_map[question_id]["status"] = status
            if self.storage_type == "file":
                self.save_questions()
            return True
        return False
    
    def delete_question(self, question_id: int) -> bool:
        """
        Delete a question.
        
        Args:
            question_id: ID of the question to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        # O(1) lookup using dictionary
        if question_id in self.question_map:
            # Remove from list
            for i, q in enumerate(self.questions):
                if q["id"] == question_id:
                    self.questions.pop(i)
                    break
                    
            # Remove from dictionary
            del self.question_map[question_id]
            
            # Remove from viewed questions if present
            if question_id in self.viewed_questions:
                self.viewed_questions.remove(question_id)
                
            if self.storage_type == "file":
                self.save_questions()
                
            return True
        return False
    
    def clear_all_questions(self) -> None:
        """Clear all questions."""
        self.questions = []
        self.question_map = {}
        self.viewed_questions = set()
        self.next_id = 0
        
        if self.storage_type == "file":
            self.save_questions()
    
    def get_sorted_questions(self, sort_by: str = "newest") -> List[Dict]:
        """
        Get questions sorted according to specified method.
        
        Args:
            sort_by: Sorting method ("newest", "votes", "random")
            
        Returns:
            List of sorted questions
        """
        if sort_by == "newest":
            return sorted(self.questions, key=lambda x: x["timestamp"], reverse=True)
        elif sort_by == "votes":
            return sorted(self.questions, key=lambda x: x["votes"], reverse=True)
        elif sort_by == "random":
            sorted_questions = self.questions.copy()
            random.shuffle(sorted_questions)
            return sorted_questions
        else:
            return self.questions
    
    def get_question_by_id(self, question_id: int) -> Optional[Dict]:
        """
        Get a question by its ID.
        
        Args:
            question_id: ID of the question to retrieve
            
        Returns:
            Dict or None: The question if found, None otherwise
        """
        return self.question_map.get(question_id)
    
    def save_questions(self) -> None:
        """Save questions to file storage."""
        if self.storage_type != "file":
            return
            
        # Save the next_id too for continuity across sessions
        data_to_save = {
            "next_id": self.next_id,
            "questions": []
        }
        
        # Convert datetime objects to strings for JSON serialization
        for q in self.questions:
            q_copy = q.copy()
            q_copy["timestamp"] = q_copy["timestamp"].isoformat()
            data_to_save["questions"].append(q_copy)
            
        with open(self.storage_path, 'w') as f:
            json.dump(data_to_save, f)
    
    def load_questions(self) -> None:
        """Load questions from file storage."""
        if not self.storage_path.exists():
            return
            
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
            
            # Handle both old and new format
            if isinstance(data, list):
                # Old format (just a list of questions)
                serialized_questions = data
                self.next_id = len(serialized_questions)
            else:
                # New format (dict with next_id and questions)
                serialized_questions = data.get("questions", [])
                self.next_id = data.get("next_id", len(serialized_questions))
                
            # Convert string timestamps back to datetime objects
            self.questions = []
            self.question_map = {}
            
            for q in serialized_questions:
                q["timestamp"] = datetime.datetime.fromisoformat(q["timestamp"])
                self.questions.append(q)
                self.question_map[q["id"]] = q
                
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading questions: {e}")
            self.questions = []
            self.question_map = {}
            self.next_id = 0