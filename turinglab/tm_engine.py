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

    def to_string(self) -> str:
        """
        Returns a simplified string representation of the tape for the final state.
        It strips bounding blank symbols unless the tape is completely empty.
        """
        if not self._tape:
            return self.blank_symbol
            
        min_idx = min(self._tape.keys())
        max_idx = max(self._tape.keys())
        
        chars = [self.read(i) for i in range(min_idx, max_idx + 1)]
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
        
        # We will add validation logic here in the next step.
        return cls(config)

    def run(self, input_string: str, max_steps: int = 1000, verbose: bool = False) -> RunResult:
        """
        Runs the Turing Machine on the given input string.
        (Implementation details will be added in the next step)
        """
        # Placeholder for RunResult to satisfy the current API skeleton.
        return RunResult(
            accepted=False,
            reason="not_implemented",
            final_tape=input_string,
            steps=0,
            history=[]
        )
