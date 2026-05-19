import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from turinglab.multi_tape import MultiTapeTM

def test_binary_add_multi_1():
    """Test 3 + 5 = 8"""
    tm = MultiTapeTM.from_yaml("machines/binary_add_multi.yaml")
    res = tm.run("11#101")
    assert res.accepted
    assert res.final_tapes[0].strip("B") == "1000"

def test_binary_add_multi_2():
    """Test 1 + 1 = 2"""
    tm = MultiTapeTM.from_yaml("machines/binary_add_multi.yaml")
    res = tm.run("1#1")
    assert res.accepted
    assert res.final_tapes[0].strip("B") == "10"

def test_binary_add_multi_3():
    """Test 15 + 1 = 16"""
    tm = MultiTapeTM.from_yaml("machines/binary_add_multi.yaml")
    res = tm.run("1111#1")
    assert res.accepted
    assert res.final_tapes[0].strip("B") == "10000"

def test_binary_add_multi_4():
    """Test 0 + 0 = 0"""
    tm = MultiTapeTM.from_yaml("machines/binary_add_multi.yaml")
    res = tm.run("0#0")
    assert res.accepted
    assert res.final_tapes[0].strip("B") == "0"

def test_binary_add_multi_5():
    """Test 10 + 10 = 20"""
    tm = MultiTapeTM.from_yaml("machines/binary_add_multi.yaml")
    res = tm.run("1010#1010")
    assert res.accepted
    assert res.final_tapes[0].strip("B") == "10100"
