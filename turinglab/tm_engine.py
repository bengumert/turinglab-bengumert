from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Set, Tuple
import yaml

@dataclass
class StepConfig:
    """Represents a single step in the Turing Machine's execution history."""
    state: str
    tape: str
    head_position: int

@dataclass
class RunResult:
    """Encapsulates the result of a Turing Machine run."""
    accepted: bool
    reason: str
    final_tape: str
    steps: int
    history: List[StepConfig] = field(default_factory=list)

class Tape:
    """
    Represents an infinite Turing Machine tape.
    Uses a dictionary internally to provide an efficient sparse representation.
    """
    def __init__(self, initial_input: str, blank_symbol: str = "B"):
        self.blank_symbol = blank_symbol
        self._tape: Dict[int, str] = {}
        for i, char in enumerate(initial_input):
            self._tape[i] = char

    def read(self, position: int) -> str:
        """Reads the symbol at the given head position."""
        return self._tape.get(position, self.blank_symbol)

    def write(self, position: int, symbol: str) -> None:
        """Writes a symbol to the given head position."""
        self._tape[position] = symbol

    def get_tape_string(self, head_position: Optional[int] = None) -> str:
        """
        Returns string representation of tape. If head_position is provided, 
        formats with [head] for verbose output.
        Determines bounds based on written symbols and head_position.
        """
        keys = set(self._tape.keys())
        if head_position is not None:
            keys.add(head_position)
            
        if not keys:
            if head_position is not None:
                return f"[{self.blank_symbol}]"
            return self.blank_symbol
            
        min_idx = min(keys)
        max_idx = max(keys)
        
        chars = []
        for i in range(min_idx, max_idx + 1):
            char = self.read(i)
            if i == head_position:
                chars.append(f"[{char}]")
            else:
                chars.append(char)
                
        return "".join(chars)

class SingleTapeTM:
    """
    Deterministic single-tape Turing Machine engine.
    """
    def __init__(self, config: Dict[str, Any]):
        self.name: str = config.get("name", "Untitled TM")
        self.description: str = config.get("description", "")
        self.states: Set[str] = set(config.get("states", []))
        self.input_alphabet: Set[str] = set(config.get("input_alphabet", []))
        self.tape_alphabet: Set[str] = set(config.get("tape_alphabet", []))
        self.blank: str = config.get("blank", "B")
        self.start_state: str = config.get("start_state", "")
        self.accept_states: Set[str] = set(config.get("accept_states", []))
        self.reject_states: Set[str] = set(config.get("reject_states", []))
        
        # Dictionary for O(1) transition lookup: (state, read_symbol) -> (next_state, write_symbol, move_dir)
        self.transitions: Dict[Tuple[str, str], Tuple[str, str, str]] = {}
        self._parse_transitions(config.get("transitions", []))

    def _parse_transitions(self, transitions_list: List[Dict[str, str]]) -> None:
        """Parses YAML transitions into a more efficient lookup dictionary."""
        for t in transitions_list:
            # Keys are state and read symbol
            key = (t["state"], str(t["read"]))
            # Values are next state, write symbol, and move direction (L, R)
            value = (t["next"], str(t["write"]), t["move"])
            self.transitions[key] = value

    @classmethod
    def from_yaml(cls, filepath: str) -> "SingleTapeTM":
        """Loads a Turing Machine configuration from a YAML file."""
        with open(filepath, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            
        required_keys = ["states", "input_alphabet", "tape_alphabet", "blank", "start_state", "transitions"]
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Invalid YAML: Missing required key '{key}'")
                
        return cls(config)

    def run(self, input_string: str, max_steps: int = 1000, verbose: bool = False) -> RunResult:
        """Runs the Turing Machine on the given input string."""
        tape = Tape(input_string, self.blank)
        current_state = self.start_state
        head_position = 0
        history: List[StepConfig] = []
        steps = 0
        
        while steps <= max_steps:
            # Record current configuration
            current_tape_str_clean = tape.get_tape_string()
            current_tape_str_with_head = tape.get_tape_string(head_position)
            
            history.append(StepConfig(
                state=current_state, 
                tape=current_tape_str_clean, 
                head_position=head_position
            ))
            
            # Check for accept/reject state before reading transition
            if current_state in self.accept_states:
                if verbose:
                    print(f"Adım {steps} | Durum: {current_state} | Şerit: {current_tape_str_with_head} | Hareket: -")
                return RunResult(accepted=True, reason="accept", final_tape=current_tape_str_clean, steps=steps, history=history)
            
            if current_state in self.reject_states:
                if verbose:
                    print(f"Adım {steps} | Durum: {current_state} | Şerit: {current_tape_str_with_head} | Hareket: -")
                return RunResult(accepted=False, reason="reject", final_tape=current_tape_str_clean, steps=steps, history=history)
                
            read_symbol = tape.read(head_position)
            transition = self.transitions.get((current_state, read_symbol))
            
            if not transition:
                if verbose:
                    print(f"Adım {steps} | Durum: {current_state} | Şerit: {current_tape_str_with_head} | Hareket: -")
                return RunResult(accepted=False, reason="no_transition", final_tape=current_tape_str_clean, steps=steps, history=history)
                
            next_state, write_symbol, move_dir = transition
            
            if verbose:
                print(f"Adım {steps} | Durum: {current_state} | Şerit: {current_tape_str_with_head} | Hareket: {move_dir}")
                
            # Apply transition
            tape.write(head_position, write_symbol)
            current_state = next_state
            
            if move_dir == "R":
                head_position += 1
            elif move_dir == "L":
                head_position -= 1
                
            steps += 1
            
        return RunResult(accepted=False, reason="timeout", final_tape=tape.get_tape_string(), steps=max_steps, history=history)
