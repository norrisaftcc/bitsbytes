"""
Pytest configuration file for the justask app tests.
"""

import pytest
import sys
import os
from pathlib import Path

# Add the parent directory to sys.path so we can import the marshmallow_lib module
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))