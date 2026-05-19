import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from turinglab.ntm import NondeterministicTM

def test_ntm_has_01_valid_1():
    tm = NondeterministicTM.from_yaml("machines/ntm_has_01.yaml")
    res = tm.run("01")
    assert res.accepted is True
    assert len(res.accepting_path) > 0

def test_ntm_has_01_valid_2():
    tm = NondeterministicTM.from_yaml("machines/ntm_has_01.yaml")
    res = tm.run("11100100")
    assert res.accepted is True

def test_ntm_has_01_invalid_1():
    tm = NondeterministicTM.from_yaml("machines/ntm_has_01.yaml")
    res = tm.run("11000")
    assert res.accepted is False
    assert res.reason == "exhausted"

def test_ntm_has_01_invalid_2():
    tm = NondeterministicTM.from_yaml("machines/ntm_has_01.yaml")
    res = tm.run("111")
    assert res.accepted is False

def test_ntm_has_01_empty():
    tm = NondeterministicTM.from_yaml("machines/ntm_has_01.yaml")
    res = tm.run("")
    assert res.accepted is False