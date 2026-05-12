import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from turinglab import SingleTapeTM

def test_unary_to_binary():
    tm = SingleTapeTM.from_yaml("machines/unary_to_binary.yaml")
    
    # Test 3: "111" -> "11"
    result = tm.run("111", max_steps=5000)
    assert result.accepted is True
    assert result.final_tape.strip("B") == "11"
    
    # Test 4: "1111" -> "100"
    result = tm.run("1111", max_steps=5000)
    assert result.accepted is True
    assert result.final_tape.strip("B") == "100"
    
    # Test 1: "1" -> "1"
    result = tm.run("1", max_steps=5000)
    assert result.accepted is True
    assert result.final_tape.strip("B") == "1"
    
    # Test 7: "1111111" -> "111"
    result = tm.run("1111111", max_steps=5000)
    assert result.accepted is True
    assert result.final_tape.strip("B") == "111"
    
    # Test empty: "" -> ""
    result = tm.run("", max_steps=5000)
    assert result.accepted is True
    assert result.final_tape.strip("B") == ""
