import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from PIL import Image, ImageDraw, ImageFont
import imageio.v2 as imageio
from typing import Optional
from turinglab import SingleTapeTM
from turinglab.tm_engine import Tape

def visualize_machine(yaml_path: str, input_str: str, max_steps: int = 100):
    tm = SingleTapeTM.from_yaml(yaml_path)
    tape = Tape(input_str, tm.blank)
    current_state = tm.start_state
    head_position = 0
    steps = 0
    
    output_dir = f"docs/images/{tm.name}"
    os.makedirs(output_dir, exist_ok=True)
    frames = []
    
    try:
        font = ImageFont.truetype("arial.ttf", 24)
        small_font = ImageFont.truetype("arial.ttf", 14)
    except IOError:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
        
    while steps <= max_steps:
        img = Image.new('RGB', (800, 300), color=(245, 245, 245))
        d = ImageDraw.Draw(img)
        
        d.text((20, 20), f"TuringLab Visualizer - Makine: {tm.name}", fill=(50, 50, 50), font=font)
        d.text((20, 60), f"Adım: {steps} | Durum: {current_state}", fill=(0, 100, 200), font=font)
        
        keys = tape._tape.keys()
        min_idx = min(min(keys) if keys else 0, head_position) - 3
        max_idx = max(max(keys) if keys else 0, head_position) + 3
        
        cell_size = 50
        start_x = max(20, 400 - ((max_idx - min_idx) * cell_size) // 2)
        start_y = 140
        
        for i in range(min_idx, max_idx + 1):
            char = tape.read(i)
            x = start_x + (i - min_idx) * cell_size
            
            fill_color = (255, 255, 255)
            if i == head_position:
                fill_color = (255, 220, 220)
                d.polygon([(x + cell_size//2, start_y + cell_size + 5),
                           (x + cell_size//2 - 10, start_y + cell_size + 20),
                           (x + cell_size//2 + 10, start_y + cell_size + 20)], fill=(200, 0, 0))
                d.text((x + cell_size//2 - 18, start_y + cell_size + 25), "KAFA", fill=(200, 0, 0), font=small_font)
                
            d.rectangle([x, start_y, x + cell_size, start_y + cell_size], fill=fill_color, outline=(100, 100, 100), width=2)
            d.text((x + cell_size//2 - 8, start_y + cell_size//2 - 12), char, fill=(0, 0, 0), font=font)
            
        if current_state in tm.accept_states or current_state in tm.reject_states:
            result_text = "KABUL (ACCEPT) Y" if current_state in tm.accept_states else "RET (REJECT) N"
            color = (0, 150, 0) if current_state in tm.accept_states else (200, 0, 0)
            d.text((20, 250), f"SONUC: {result_text}", fill=color, font=font)
            
        frame_path = f"{output_dir}/frame_{steps:03d}.png"
        img.save(frame_path)
        frames.append(imageio.imread(frame_path))
        
        if current_state in tm.accept_states or current_state in tm.reject_states:
            break
            
        read_symbol = tape.read(head_position)
        transition = tm.transitions.get((current_state, read_symbol))
        if not transition:
            d.text((20, 250), "SONUC: GECIS BULUNAMADI (CRASH)", fill=(200, 0, 0), font=font)
            img.save(frame_path)
            frames[-1] = imageio.imread(frame_path)
            break
            
        next_state, write_symbol, move_dir = transition
        tape.write(head_position, write_symbol)
        current_state = next_state
        if move_dir == "R": head_position += 1
        elif move_dir == "L": head_position -= 1
        steps += 1
        
    gif_path = f"{output_dir}/animation.gif"
    imageio.mimsave(gif_path, frames, fps=2)

if __name__ == "__main__":
    visualize_machine("machines/unary_to_binary.yaml", "11")