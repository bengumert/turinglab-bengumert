import yaml
from typing import Dict, List, Any, Set, Tuple, Optional
from dataclasses import dataclass, field
from .tm_engine import Tape

@dataclass
class MultiStepConfig:
    state: str
    tapes: List[str]
    head_positions: List[int]

@dataclass
class MultiRunResult:
    accepted: bool
    reason: str
    final_tapes: List[str]
    steps: int
    history: List[MultiStepConfig] = field(default_factory=list)

class MultiTapeTM:
    def __init__(self, config: Dict[str, Any]):
        self.name: str = config.get("name", "Untitled Multi-Tape TM")
        self.description: str = config.get("description", "")
        self.num_tapes: int = config.get("num_tapes", 1)
        self.states: Set[str] = set(config.get("states", []))
        self.input_alphabet: Set[str] = set(config.get("input_alphabet", []))
        self.tape_alphabet: Set[str] = set(config.get("tape_alphabet", []))
        self.blank: str = config.get("blank", "B")
        self.start_state: str = config.get("start_state", "")
        self.accept_states: Set[str] = set(config.get("accept_states", []))
        self.reject_states: Set[str] = set(config.get("reject_states", []))

        # transitions: (state, (read1, read2, ...)) -> (next_state, (write1, write2, ...), (move1, move2, ...))
        self.transitions: Dict[Tuple[str, Tuple[str, ...]], Tuple[str, Tuple[str, ...], Tuple[str, ...]]] = {}
        self._parse_transitions(config.get("transitions", []))

    def _parse_transitions(self, transitions_list: List[Dict[str, Any]]) -> None:
        for t in transitions_list:
            read_tuple = tuple(str(x) for x in t["read"])
            write_tuple = tuple(str(x) for x in t["write"])
            move_tuple = tuple(t["move"])
            
            if len(read_tuple) != self.num_tapes or len(write_tuple) != self.num_tapes or len(move_tuple) != self.num_tapes:
                raise ValueError("Transition lists must match num_tapes")
                
            key = (t["state"], read_tuple)
            value = (t["next"], write_tuple, move_tuple)
            self.transitions[key] = value

    @classmethod
    def from_yaml(cls, filepath: str) -> "MultiTapeTM":
        with open(filepath, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        
        required_keys = ["num_tapes", "states", "input_alphabet", "tape_alphabet", "blank", "start_state", "transitions"]
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Invalid YAML: Missing required key '{key}'")
                
        return cls(config)

    def run(self, input_string: str, max_steps: int = 1000, verbose: bool = False) -> MultiRunResult:
        tapes = [Tape(input_string if i == 0 else "", self.blank) for i in range(self.num_tapes)]
        head_positions = [0] * self.num_tapes
        current_state = self.start_state
        history: List[MultiStepConfig] = []
        steps = 0

        while steps <= max_steps:
            current_tapes_clean = [t.get_tape_string() for t in tapes]
            current_tapes_with_head = [t.get_tape_string(pos) for t, pos in zip(tapes, head_positions)]

            history.append(MultiStepConfig(
                state=current_state,
                tapes=current_tapes_clean,
                head_positions=list(head_positions)
            ))

            if current_state in self.accept_states:
                if verbose:
                    print(f"Adım {steps} | Durum: {current_state} | Şeritler: {current_tapes_with_head} | Hareket: -")
                return MultiRunResult(accepted=True, reason="accept", final_tapes=current_tapes_clean, steps=steps, history=history)

            if current_state in self.reject_states:
                if verbose:
                    print(f"Adım {steps} | Durum: {current_state} | Şeritler: {current_tapes_with_head} | Hareket: -")
                return MultiRunResult(accepted=False, reason="reject", final_tapes=current_tapes_clean, steps=steps, history=history)

            read_symbols = tuple(t.read(pos) for t, pos in zip(tapes, head_positions))
            transition = self.transitions.get((current_state, read_symbols))

            if not transition:
                if verbose:
                    print(f"Adım {steps} | Durum: {current_state} | Şeritler: {current_tapes_with_head} | Hareket: -")
                return MultiRunResult(accepted=False, reason="no_transition", final_tapes=current_tapes_clean, steps=steps, history=history)

            next_state, write_symbols, move_dirs = transition

            if verbose:
                print(f"Adım {steps} | Durum: {current_state} | Şeritler: {current_tapes_with_head} | Hareket: {move_dirs}")

            for i in range(self.num_tapes):
                tapes[i].write(head_positions[i], write_symbols[i])
                if move_dirs[i] == "R":
                    head_positions[i] += 1
                elif move_dirs[i] == "L":
                    head_positions[i] -= 1

            current_state = next_state
            steps += 1

        final_tapes = [t.get_tape_string() for t in tapes]
        return MultiRunResult(accepted=False, reason="timeout", final_tapes=final_tapes, steps=max_steps, history=history)
