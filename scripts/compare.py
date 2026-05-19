import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import matplotlib.pyplot as plt
from turinglab import SingleTapeTM
from turinglab.ntm import NondeterministicTM

def main():
    dtm = SingleTapeTM.from_yaml("machines/single_has_01.yaml")
    ntm = NondeterministicTM.from_yaml("machines/ntm_has_01.yaml")

    lengths = []
    dtm_steps = []
    ntm_steps = []

    for i in range(2, 21):
        input_str = "0" * (i - 1) + "1"
        lengths.append(i)

        dtm_res = dtm.run(input_str)
        dtm_steps.append(dtm_res.steps)

        ntm_res = ntm.run(input_str)
        ntm_steps.append(ntm_res.steps_explored)

    plt.figure(figsize=(10, 6))
    plt.plot(lengths, dtm_steps, label="Deterministic TM (Adım Sayısı)", marker='o')
    plt.plot(lengths, ntm_steps, label="Nondeterministic TM (İncelenen Dal Sayısı)", marker='s')
    
    plt.title("DTM vs NTM: '01' Alt-dizgisi Arama Performansı")
    plt.xlabel("Girdi Uzunluğu (n)")
    plt.ylabel("Hesaplama Maliyeti (Adım / Dal Sayısı)")
    plt.legend()
    plt.grid(True)
    
    os.makedirs("docs/images", exist_ok=True)
    plt.savefig("docs/images/comparison.png")

if __name__ == "__main__":
    main()