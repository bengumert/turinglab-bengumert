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

def test_binary_compare():
    tm = SingleTapeTM.from_yaml("machines/binary_compare.yaml")
    
    # 1. A > B (Same length)
    res = tm.run("1011#1100") # wait, 1011 is 11, 1100 is 12. So 11 < 12! REJECT
    assert res.accepted is False
    
    res = tm.run("1101#1011") # 13 > 11. ACCEPT
    assert res.accepted is True
    
    # 2. A < B (Same length)
    res = tm.run("10#11")
    assert res.accepted is False
    
    # 3. A == B
    res = tm.run("110#110")
    assert res.accepted is False
    
    # 4. A > B (Different length)
    res = tm.run("100#11") # 4 > 3
    assert res.accepted is True
    
    # 5. A < B (Different length)
    res = tm.run("11#100")
    assert res.accepted is False
    
    # 6. Leading Zeros A > B
    res = tm.run("0010#1") # 2 > 1. Length of A is 4, length of B is 1. But effective length is 2 vs 1.
    assert res.accepted is True
    
    # 7. Leading Zeros A < B
    res = tm.run("0001#0010") # 1 < 2
    assert res.accepted is False

    # 8. Zero vs Zero
    res = tm.run("0#0")
    assert res.accepted is False

    # 9. 0 vs 1
    res = tm.run("0#1")
    assert res.accepted is False

    # 10. 1 vs 0
    res = tm.run("1#0")
    assert res.accepted is True
