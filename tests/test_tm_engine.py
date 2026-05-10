import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from turinglab import SingleTapeTM

def test_binary_increment_valid():
    """Test binary increment machine with a valid input."""
    tm = SingleTapeTM.from_yaml("machines/binary_increment.yaml")
    result = tm.run("1011")
    assert result.accepted is True
    assert result.final_tape.strip("B") == "1100"
    assert result.reason == "accept"
    assert len(result.history) > 0

def test_unary_increment_valid():
    """Test unary increment machine with a valid input."""
    tm = SingleTapeTM.from_yaml("machines/unary_increment.yaml")
    result = tm.run("111")
    assert result.accepted is True
    assert result.final_tape.strip("B") == "1111"

def test_even_a_accepts():
    """Test even_a machine with an accepted input."""
    tm = SingleTapeTM.from_yaml("machines/even_a.yaml")
    # abab has 2 a's (even)
    result = tm.run("abab")
    assert result.accepted is True

def test_even_a_rejects():
    """Test even_a machine with a rejected input."""
    tm = SingleTapeTM.from_yaml("machines/even_a.yaml")
    # aba has 2 a's? Wait, a (1) b a (2). Total 2. Oh, let's trace "aba":
    # q_even(a)->q_odd, q_odd(b)->q_odd, q_odd(a)->q_even. Ends at q_even. Then sees B -> accepts.
    # So "aba" has 2 'a's, accepted. 
    # Let's test "baa". b->q_even, a->q_odd, a->q_even. Accepted.
    # Let's test "baaab". 3 'a's -> rejected.
    result = tm.run("baaab")
    assert result.accepted is False
    assert result.reason == "reject"

def test_timeout_behavior():
    """Test if max_steps limits the execution properly."""
    tm = SingleTapeTM.from_yaml("machines/unary_increment.yaml")
    # Hack transitions to create an infinite loop
    tm.transitions[("q0", "1")] = ("q0", "1", "L")
    tm.transitions[("q0", "B")] = ("q0", "B", "R") 
    result = tm.run("11", max_steps=10)
    assert result.accepted is False
    assert result.reason == "timeout"
    assert result.steps == 10

def test_no_transition():
    """Test behavior when no transition is defined for a symbol."""
    tm = SingleTapeTM.from_yaml("machines/even_a.yaml")
    # The machine only knows 'a', 'b', 'B'. Sending 'c' will have no transition.
    result = tm.run("c")
    assert result.accepted is False
    assert result.reason == "no_transition"

def test_invalid_yaml(tmp_path):
    """Test that a missing required key throws ValueError."""
    broken_yaml_path = tmp_path / "broken.yaml"
    broken_yaml_path.write_text("name: broken\nstates: [q0]\n")
    
    with pytest.raises(ValueError, match="Invalid YAML: Missing required key"):
        SingleTapeTM.from_yaml(str(broken_yaml_path))

def test_verbose_output(capsys):
    """Test that verbose output correctly logs the steps."""
    tm = SingleTapeTM.from_yaml("machines/unary_increment.yaml")
    tm.run("1", verbose=True)
    captured = capsys.readouterr()
    
    assert "Adım 0 | Durum: q0" in captured.out
    assert "Hareket: R" in captured.out
    # Check if the bracket formatting for head is printed
    assert "[" in captured.out and "]" in captured.out
