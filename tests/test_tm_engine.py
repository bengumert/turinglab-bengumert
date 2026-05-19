import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from turinglab import SingleTapeTM

def test_binary_increment_valid():
    """Geçerli bir girdi ile binary increment makinesini test ediyorum."""
    tm = SingleTapeTM.from_yaml("machines/binary_increment.yaml")
    result = tm.run("1011")
    assert result.accepted is True
    assert result.final_tape.strip("B") == "1100"
    assert result.reason == "accept"
    assert len(result.history) > 0

def test_unary_increment_valid():
    """Geçerli bir girdi ile unary increment makinesini test ediyorum."""
    tm = SingleTapeTM.from_yaml("machines/unary_increment.yaml")
    result = tm.run("111")
    assert result.accepted is True
    assert result.final_tape.strip("B") == "1111"

def test_even_a_accepts():
    """Kabul edilecek bir girdi ile çift 'a' sayan makineyi (even_a) test ediyorum."""
    tm = SingleTapeTM.from_yaml("machines/even_a.yaml")
    # abab kelimesinde 2 tane 'a' var (çift), o yüzden kabul edilmeli.
    result = tm.run("abab")
    assert result.accepted is True

def test_even_a_rejects():
    """Reddedilecek bir girdi ile çift 'a' sayan makineyi (even_a) test ediyorum."""
    tm = SingleTapeTM.from_yaml("machines/even_a.yaml")
    # "baaab" stringinde 3 tane 'a' var -> tek sayı olduğu için reddedilecek (reject).
    result = tm.run("baaab")
    assert result.accepted is False
    assert result.reason == "reject"

def test_timeout_behavior():
    """Makine sonsuz döngüye girerse max_steps'in onu durdurup durdurmadığını test ediyorum."""
    tm = SingleTapeTM.from_yaml("machines/unary_increment.yaml")
    # Sonsuz döngü simüle etmek için geçişleri (transitions) anlık olarak hackliyorum :)
    tm.transitions[("q0", "1")] = ("q0", "1", "L")
    tm.transitions[("q0", "B")] = ("q0", "B", "R")
    result = tm.run("11", max_steps=10)
    assert result.accepted is False
    assert result.reason == "timeout"
    assert result.steps == 10

def test_no_transition():
    """Okunan sembol için bir geçiş kuralı yoksa (no_transition) makinenin çökmeden ret verip vermediğini test ediyorum."""
    tm = SingleTapeTM.from_yaml("machines/even_a.yaml")
    # Makine sadece 'a', 'b', 'B' biliyor. 'c' gönderdiğimizde ne yapacağını bilemeyip ret vermeli.
    result = tm.run("c")
    assert result.accepted is False
    assert result.reason == "no_transition"

def test_invalid_yaml(tmp_path):
    """YAML dosyasında eksik/yanlış anahtarlar varsa uygun ValueError fırlatılıp fırlatılmadığını test ediyorum."""
    broken_yaml_path = tmp_path / "broken.yaml"
    broken_yaml_path.write_text("name: broken\nstates: [q0]\n")
    
    with pytest.raises(ValueError, match="Invalid YAML: Missing required key"):
        SingleTapeTM.from_yaml(str(broken_yaml_path))

def test_verbose_output(capsys):
    """Verbose (detaylı) çıktının adımları ve şeridi terminale doğru basıp basmadığını test ediyorum."""
    tm = SingleTapeTM.from_yaml("machines/unary_increment.yaml")
    tm.run("1", verbose=True)
    captured = capsys.readouterr()
    
    assert "Adım 0 | Durum: q0" in captured.out
    assert "Hareket: R" in captured.out
    # Kafa pozisyonunun el kitabındaki gibi köşeli parantez [ ] içine alındığından emin oluyorum.
    assert "[" in captured.out and "]" in captured.out
