"""
Console-based GUI for the Marshmallows anonymous questions app.

This module provides a text-based interface for the application, using the
core functionality from the marshmallow_lib package.
"""

import os
import sys
import time
from typing import List, Dict, Optional
import datetime
from .core import MarshmallowManager


class ConsoleGUI:
    """Console-based interface for the Marshmallows application."""
    
    def __init__(self, storage_type: str = "file"):
        """
        Initialize the console GUI.
        
        Args:
            storage_type: Type of storage to use (defaults to "file" for persistence)
        """
        self.manager = MarshmallowManager(storage_type=storage_type)
        self.admin_mode = False
        self.admin_password = "instructor"
        self.running = True
        
        # ANSI color codes for terminal output
        self.colors = {
            "reset": "\033[0m",
            "bold": "\033[1m",
            "blue": "\033[94m",
            "green": "\033[92m",
            "yellow": "\033[93m",
            "red": "\033[91m",
            "magenta": "\033[95m",
            "cyan": "\033[96m",
        }
    
    def clear_screen(self):
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print the application header."""
        self.clear_screen()
        print(f"{self.colors['bold']}{self.colors['magenta']}====================================={self.colors['reset']}")
        print(f"{self.colors['bold']}{self.colors['magenta']} MARSHMALLOWS - ANONYMOUS QUESTIONS {self.colors['reset']}")
        print(f"{self.colors['bold']}{self.colors['magenta']}====================================={self.colors['reset']}")
        print(f"You are: {self.colors['cyan']}{self.manager.user_id}{self.colors['reset']}")
        if self.admin_mode:
            print(f"{self.colors['red']}[ADMIN MODE]{self.colors['reset']}")
        print()
    
    def print_question(self, question: Dict, show_details: bool = False):
        """
        Print a formatted question.
        
        Args:
            question: Question dictionary
            show_details: Whether to show admin details
        """
        if question["highlighted"]:
            prefix = f"{self.colors['blue']}★ "
            suffix = f"{self.colors['reset']}"
        else:
            prefix = "  "
            suffix = ""
            
        status_display = ""
        if show_details:
            status = question.get("status", "approved")
            if status == "pending":
                status_display = f"{self.colors['yellow']}[PENDING]{self.colors['reset']} "
            elif status == "approved":
                status_display = f"{self.colors['green']}[APPROVED]{self.colors['reset']} "
        
        # Format timestamp
        timestamp = question["timestamp"]
        if isinstance(timestamp, datetime.datetime):
            time_str = timestamp.strftime('%I:%M %p')
        else:
            time_str = str(timestamp)
            
        # Print the question
        print(f"{prefix}{status_display}\"{question['text']}\"")
        print(f"   {self.colors['cyan']}Posted: {time_str} | Votes: {question['votes']}{suffix}")
        print()
    
    def print_menu(self):
        """Print the main menu options."""
        print(f"{self.colors['bold']}MENU OPTIONS:{self.colors['reset']}")
        print(f"1. {self.colors['green']}Add a Marshmallow{self.colors['reset']}")
        print(f"2. {self.colors['yellow']}Pick a Random Marshmallow{self.colors['reset']}")
        print(f"3. {self.colors['blue']}See All Marshmallows{self.colors['reset']}")
        
        if self.admin_mode:
            print(f"4. {self.colors['red']}Admin Controls{self.colors['reset']}")
            print(f"5. {self.colors['red']}Exit Admin Mode{self.colors['reset']}")
        else:
            print(f"4. {self.colors['magenta']}Enter Admin Mode{self.colors['reset']}")
            
        print(f"0. {self.colors['bold']}Exit{self.colors['reset']}")
        print()
    
    def get_input(self, prompt: str) -> str:
        """
        Get user input with a prompt.
        
        Args:
            prompt: The prompt to display
            
        Returns:
            User input string
        """
        return input(f"{prompt}: ")
    
    def add_marshmallow(self):
        """Handle adding a new question."""
        self.print_header()
        print(f"{self.colors['green']}=== ADD A MARSHMALLOW ==={self.colors['reset']}")
        print("Type your anonymous question below.")
        print("Your identity will be shown as: " + 
              f"{self.colors['cyan']}{self.manager.user_id}{self.colors['reset']}")
        print()
        
        question_text = input("> ")
        
        if self.manager.add_question(question_text):
            print()
            print(f"{self.colors['green']}Your marshmallow has been tossed into the pile!{self.colors['reset']}")
        else:
            print()
            print(f"{self.colors['red']}Please enter a question before submitting.{self.colors['reset']}")
            
        print()
        input("Press Enter to continue...")
    
    def pick_random_marshmallow(self):
        """Handle picking a random question."""
        self.print_header()
        print(f"{self.colors['yellow']}=== PICK A RANDOM MARSHMALLOW ==={self.colors['reset']}")
        
        random_question = self.manager.get_random_question()
        
        if random_question:
            self.print_question(random_question)
            
            print(f"Options: {self.colors['green']}V{self.colors['reset']}ote, {self.colors['blue']}B{self.colors['reset']}ack")
            choice = self.get_input("Enter choice (V/B)").lower()
            
            if choice == 'v':
                self.manager.vote_for_question(random_question['id'])
                print(f"{self.colors['green']}Vote recorded!{self.colors['reset']}")
                time.sleep(1)
        else:
            print(f"{self.colors['yellow']}No marshmallows available. Be the first to add one!{self.colors['reset']}")
            print()
            input("Press Enter to continue...")
    
    def see_all_marshmallows(self):
        """Handle viewing all questions."""
        while True:
            self.print_header()
            print(f"{self.colors['blue']}=== SEE ALL MARSHMALLOWS ==={self.colors['reset']}")
            
            # Sort options
            print("Sort by:")
            print("1. Newest First")
            print("2. Most Voted")
            print("3. Random Order")
            print("0. Back to Main Menu")
            
            sort_choice = self.get_input("Enter choice")
            
            if sort_choice == '0':
                break
                
            sort_method = "newest"  # Default
            if sort_choice == '1':
                sort_method = "newest"
            elif sort_choice == '2':
                sort_method = "votes"
            elif sort_choice == '3':
                sort_method = "random"
            
            # Display questions
            self.print_header()
            print(f"{self.colors['blue']}=== ALL MARSHMALLOWS (Sorted by: {sort_method}) ==={self.colors['reset']}")
            
            # Get questions with appropriate sorting
            sorted_questions = self.manager.get_sorted_questions(sort_method)
            
            if sorted_questions:
                # Display the questions
                for i, q in enumerate(sorted_questions):
                    if q["status"] == "pending" and not self.admin_mode:
                        continue  # Skip pending questions for non-admins
                    
                    print(f"{self.colors['bold']}#{i+1}{self.colors['reset']}")
                    self.print_question(q, self.admin_mode)
                
                # Options for interacting with questions
                print("Options:")
                print(f"{self.colors['green']}V{self.colors['reset']}: Vote for a question")
                
                if self.admin_mode:
                    print(f"{self.colors['yellow']}H{self.colors['reset']}: Hide/Show a question")
                    print(f"{self.colors['blue']}S{self.colors['reset']}: Highlight/Unhighlight a question")
                    print(f"{self.colors['red']}D{self.colors['reset']}: Delete a question")
                
                print(f"{self.colors['reset']}B{self.colors['reset']}: Back to sort options")
                
                choice = self.get_input("Enter choice").lower()
                
                if choice == 'b':
                    continue
                elif choice == 'v':
                    q_num = self.get_input("Enter question number to vote for")
                    try:
                        q_index = int(q_num) - 1
                        if 0 <= q_index < len(sorted_questions):
                            self.manager.vote_for_question(sorted_questions[q_index]['id'])
                            print(f"{self.colors['green']}Vote recorded!{self.colors['reset']}")
                        else:
                            print(f"{self.colors['red']}Invalid question number.{self.colors['reset']}")
                    except ValueError:
                        print(f"{self.colors['red']}Please enter a valid number.{self.colors['reset']}")
                    time.sleep(1)
                elif choice == 'h' and self.admin_mode:
                    q_num = self.get_input("Enter question number to hide/show")
                    try:
                        q_index = int(q_num) - 1
                        if 0 <= q_index < len(sorted_questions):
                            q = sorted_questions[q_index]
                            new_status = "pending" if q["status"] == "approved" else "approved"
                            self.manager.set_question_status(q['id'], new_status)
                            print(f"{self.colors['green']}Question status updated!{self.colors['reset']}")
                        else:
                            print(f"{self.colors['red']}Invalid question number.{self.colors['reset']}")
                    except ValueError:
                        print(f"{self.colors['red']}Please enter a valid number.{self.colors['reset']}")
                    time.sleep(1)
                elif choice == 's' and self.admin_mode:
                    q_num = self.get_input("Enter question number to highlight/unhighlight")
                    try:
                        q_index = int(q_num) - 1
                        if 0 <= q_index < len(sorted_questions):
                            q = sorted_questions[q_index]
                            self.manager.highlight_question(q['id'], not q["highlighted"])
                            print(f"{self.colors['green']}Highlight status updated!{self.colors['reset']}")
                        else:
                            print(f"{self.colors['red']}Invalid question number.{self.colors['reset']}")
                    except ValueError:
                        print(f"{self.colors['red']}Please enter a valid number.{self.colors['reset']}")
                    time.sleep(1)
                elif choice == 'd' and self.admin_mode:
                    q_num = self.get_input("Enter question number to delete")
                    try:
                        q_index = int(q_num) - 1
                        if 0 <= q_index < len(sorted_questions):
                            q = sorted_questions[q_index]
                            confirm = self.get_input(f"Are you sure you want to delete this question? (y/n)").lower()
                            if confirm == 'y':
                                self.manager.delete_question(q['id'])
                                print(f"{self.colors['green']}Question deleted!{self.colors['reset']}")
                        else:
                            print(f"{self.colors['red']}Invalid question number.{self.colors['reset']}")
                    except ValueError:
                        print(f"{self.colors['red']}Please enter a valid number.{self.colors['reset']}")
                    time.sleep(1)
            else:
                print(f"{self.colors['yellow']}No marshmallows have been added yet. Be the first!{self.colors['reset']}")
                print()
                input("Press Enter to continue...")
                break
    
    def admin_controls(self):
        """Handle admin-specific controls."""
        while True:
            self.print_header()
            print(f"{self.colors['red']}=== ADMIN CONTROLS ==={self.colors['reset']}")
            print("1. Clear All Marshmallows")
            print("0. Back to Main Menu")
            
            choice = self.get_input("Enter choice")
            
            if choice == '0':
                break
            elif choice == '1':
                confirm = self.get_input("Are you sure you want to delete ALL questions? (y/n)").lower()
                if confirm == 'y':
                    self.manager.clear_all_questions()
                    print(f"{self.colors['green']}All questions cleared!{self.colors['reset']}")
                    time.sleep(1)
    
    def enter_admin_mode(self):
        """Handle entering admin mode."""
        self.print_header()
        print(f"{self.colors['magenta']}=== ENTER ADMIN MODE ==={self.colors['reset']}")
        
        password = self.get_input("Enter admin password")
        
        if password == self.admin_password:
            self.admin_mode = True
            print(f"{self.colors['green']}Admin mode activated!{self.colors['reset']}")
        else:
            print(f"{self.colors['red']}Incorrect password.{self.colors['reset']}")
            
        time.sleep(1)
    
    def exit_admin_mode(self):
        """Handle exiting admin mode."""
        self.admin_mode = False
        print(f"{self.colors['green']}Exited admin mode.{self.colors['reset']}")
        time.sleep(1)
    
    def run(self):
        """Run the main application loop."""
        while self.running:
            self.print_header()
            self.print_menu()
            
            choice = self.get_input("Enter your choice")
            
            if choice == '0':
                self.running = False
            elif choice == '1':
                self.add_marshmallow()
            elif choice == '2':
                self.pick_random_marshmallow()
            elif choice == '3':
                self.see_all_marshmallows()
            elif choice == '4':
                if self.admin_mode:
                    self.admin_controls()
                else:
                    self.enter_admin_mode()
            elif choice == '5' and self.admin_mode:
                self.exit_admin_mode()
            else:
                print(f"{self.colors['red']}Invalid choice, please try again.{self.colors['reset']}")
                time.sleep(1)
        
        print(f"{self.colors['green']}Thank you for using Marshmallows!{self.colors['reset']}")


def run_console_app(storage_type: str = "file"):
    """
    Run the console GUI application.
    
    Args:
        storage_type: Type of storage to use (defaults to "file" for persistence)
    """
    app = ConsoleGUI(storage_type=storage_type)
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nExiting Marshmallows. Goodbye!")
        sys.exit(0)