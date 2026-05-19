import yaml
from typing import Dict, List, Any, Set, Tuple, Optional
from dataclasses import dataclass, field
from collections import deque
import copy

from .tm_engine import Tape, StepConfig

@dataclass
class NTMRunResult:
    accepted: bool
    reason: str
    steps_explored: int
    accepting_path: List[StepConfig] = field(default_factory=list)

class NondeterministicTM:
    def __init__(self, config: Dict[str, Any]):
        self.name: str = config.get("name", "Untitled NTM")
        self.description: str = config.get("description", "")
        self.states: Set[str] = set(config.get("states", []))
        self.input_alphabet: Set[str] = set(config.get("input_alphabet", []))
        self.tape_alphabet: Set[str] = set(config.get("tape_alphabet", []))
        self.blank: str = config.get("blank", "B")
        self.start_state: str = config.get("start_state", "")
        self.accept_states: Set[str] = set(config.get("accept_states", []))
        self.reject_states: Set[str] = set(config.get("reject_states", []))

        self.transitions: Dict[Tuple[str, str], List[Tuple[str, str, str]]] = {}
        self._parse_transitions(config.get("transitions", []))

    def _parse_transitions(self, transitions_list: List[Dict[str, Any]]) -> None:
        for t in transitions_list:
            key = (t["state"], str(t["read"]))
            choices = t.get("choices", [])
            
            if not choices and "next" in t:
                choices = [{"next": t["next"], "write": t["write"], "move": t["move"]}]
                
            parsed_choices = []
            for c in choices:
                parsed_choices.append((c["next"], str(c["write"]), c["move"]))
                
            if key not in self.transitions:
                self.transitions[key] = []
            self.transitions[key].extend(parsed_choices)

    @classmethod
    def from_yaml(cls, filepath: str) -> "NondeterministicTM":
        with open(filepath, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        
        required_keys = ["states", "input_alphabet", "tape_alphabet", "blank", "start_state", "transitions"]
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Invalid YAML: Missing required key '{key}'")
                
        return cls(config)

    def run(self, input_string: str, max_depth: int = 100, max_branches: int = 10000, verbose: bool = False) -> NTMRunResult:
        initial_tape = Tape(input_string, self.blank)
        
        initial_config = StepConfig(
            state=self.start_state,
            tape=initial_tape.get_tape_string(),
            head_position=0
        )
        
        queue = deque([(self.start_state, initial_tape._tape.copy(), 0, 0, [initial_config])])
        branches_explored = 0

        while queue:
            if branches_explored >= max_branches:
                return NTMRunResult(accepted=False, reason="max_branches_exceeded", steps_explored=branches_explored)
                
            curr_state, curr_tape_dict, head_pos, depth, path = queue.popleft()
            branches_explored += 1
            
            if curr_state in self.accept_states:
                if verbose:
                    print(f"Kabul edildi! Bulunan yol uzunluğu: {depth}, Toplam incelenen dal: {branches_explored}")
                return NTMRunResult(accepted=True, reason="accept", steps_explored=branches_explored, accepting_path=path)
                
            if curr_state in self.reject_states or depth >= max_depth:
                continue

            read_symbol = curr_tape_dict.get(head_pos, self.blank)
            choices = self.transitions.get((curr_state, read_symbol), [])
            
            for next_state, write_symbol, move_dir in choices:
                new_tape_dict = curr_tape_dict.copy()
                new_tape_dict[head_pos] = write_symbol
                
                new_head_pos = head_pos + 1 if move_dir == "R" else head_pos - 1 if move_dir == "L" else head_pos
                
                temp_tape = Tape("", self.blank)
                temp_tape._tape = new_tape_dict
                
                new_step = StepConfig(
                    state=next_state,
                    tape=temp_tape.get_tape_string(),
                    head_position=new_head_pos
                )
                
                new_path = list(path)
                new_path.append(new_step)
                
                queue.append((next_state, new_tape_dict, new_head_pos, depth + 1, new_path))
                
        return NTMRunResult(accepted=False, reason="exhausted", steps_explored=branches_explored)