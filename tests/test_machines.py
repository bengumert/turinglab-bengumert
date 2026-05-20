import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from turinglab import SingleTapeTM

def test_unary_to_binary():
    tm = SingleTapeTM.from_yaml("machines/unary_to_binary.yaml")
    
    # Test 3: "111" -> "11" (Unary 3'ü Binary 3'e çevirme)
    result = tm.run("111", max_steps=5000)
    assert result.accepted is True
    assert result.final_tape.strip("B") == "11"
    
    # Test 4: "1111" -> "100" (Unary 4'ü Binary 4'e çevirme)
    result = tm.run("1111", max_steps=5000)
    assert result.accepted is True
    assert result.final_tape.strip("B") == "100"
    
    # Test 1: "1" -> "1"
    result = tm.run("1", max_steps=5000)
    assert result.accepted is True
    assert result.final_tape.strip("B") == "1"
    
    # Test 7: "1111111" -> "111" (Unary 7'yi Binary 7'ye çevirme)
    result = tm.run("1111111", max_steps=5000)
    assert result.accepted is True
    assert result.final_tape.strip("B") == "111"
    
    # Test boş string (empty) durumu
    result = tm.run("", max_steps=5000)
    assert result.accepted is True
    assert result.final_tape.strip("B") == ""

def test_binary_compare():
    tm = SingleTapeTM.from_yaml("machines/binary_compare.yaml")
    
    # 1. A > B (Aynı uzunluk)
    res = tm.run("1011#1100") # 1011 = 11, 1100 = 12. Yani 11 < 12 olduğu için REDDETMELİ
    assert res.accepted is False
    
    res = tm.run("1101#1011") # 13 > 11 olduğu için KABUL ETMELİ
    assert res.accepted is True
    
    # 2. A < B (Aynı uzunluk)
    res = tm.run("10#11")
    assert res.accepted is False
    
    # 3. A == B (Eşitlik durumu)
    res = tm.run("110#110")
    assert res.accepted is False
    
    # 4. A > B (Farklı uzunluk)
    res = tm.run("100#11") # 4 > 3
    assert res.accepted is True
    
    # 5. A < B (Farklı uzunluk)
    res = tm.run("11#100")
    assert res.accepted is False
    
    # 6. Baştaki anlamsız sıfırlar (Leading Zeros) A > B
    res = tm.run("0010#1") # 2 > 1. A'nın uzunluğu 4, B'nin 1 ama efektif olarak 2 bit vs 1 bit.
    assert res.accepted is True
    
    # 7. Baştaki anlamsız sıfırlar (Leading Zeros) A < B
    res = tm.run("0001#0010") # 1 < 2
    assert res.accepted is False

    # 8. Sıfır vs Sıfır
    res = tm.run("0#0")
    assert res.accepted is False

    # 9. 0 vs 1
    res = tm.run("0#1")
    assert res.accepted is False

    # 10. 1 vs 0
    res = tm.run("1#0")
    assert res.accepted is True

def test_string_copy():
    tm = SingleTapeTM.from_yaml("machines/string_copy.yaml")
    
    # 1. Standart kopya testi
    res = tm.run("aba")
    assert res.accepted is True
    assert res.final_tape.strip("B") == "aba#aba"
    
    # 2. Tek karakterli metin
    res = tm.run("a")
    assert res.accepted is True
    assert res.final_tape.strip("B") == "a#a"
    
    res = tm.run("b")
    assert res.accepted is True
    assert res.final_tape.strip("B") == "b#b"
    
    # 3. Daha uzun bir metin
    res = tm.run("bbabaa")
    assert res.accepted is True
    assert res.final_tape.strip("B") == "bbabaa#bbabaa"
    
    # 4. Boş metin (empty string) durumu
    res = tm.run("")
    assert res.accepted is True
    assert res.final_tape.strip("B") == "#"

def test_student_choice_palindrome():
    tm = SingleTapeTM.from_yaml("machines/student_choice.yaml")
    
    # 1. Çift uzunluklu (Even) palindrom
    res = tm.run("abba")
    assert res.accepted is True
    
    # 2. Tek uzunluklu (Odd) palindrom
    res = tm.run("ababa")
    assert res.accepted is True
    
    # 3. Palindrom olmayan string
    res = tm.run("abab")
    assert res.accepted is False
    
    # 4. Tek karakter
    res = tm.run("a")
    assert res.accepted is True
    
    res = tm.run("b")
    assert res.accepted is True
    
    # 5. Boş string (empty)
    res = tm.run("")
    assert res.accepted is True
    
    # 6. Uzun palindrom testi
    res = tm.run("bbabaaaababb")
    assert res.accepted is True
