import os
import time
from pathlib import Path
from turinglab import SingleTapeTM

def print_header(title):
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)

def main():
    machines_dir = Path("machines")
    if not machines_dir.exists() or not machines_dir.is_dir():
        print("Hata: 'machines' dizini bulunamadı.")
        return

    yaml_files = list(machines_dir.glob("*.yaml"))
    if not yaml_files:
        print("Hata: 'machines' dizininde hiç YAML dosyası bulunamadı.")
        return

    print_header("TuringLab - Demo Aracı")
    print("Mevcut Turing Makineleri:")
    for idx, file_path in enumerate(yaml_files, 1):
        print(f"[{idx}] {file_path.name}")
    print("[0] Çıkış")

    try:
        choice = int(input("\nÇalıştırmak istediğiniz makinenin numarasını girin: "))
    except ValueError:
        print("Geçersiz giriş. Lütfen bir sayı girin.")
        return

    if choice == 0:
        print("Çıkış yapılıyor...")
        return
    if choice < 1 or choice > len(yaml_files):
        print("Geçersiz makine numarası.")
        return

    selected_file = yaml_files[choice - 1]
    
    try:
        tm = SingleTapeTM.from_yaml(str(selected_file))
    except Exception as e:
        print(f"Makine yüklenirken hata oluştu: {e}")
        return

    print_header(f"Makine: {tm.name}")
    print(f"Açıklama: {tm.description}")
    
    input_str = input("\nBaşlangıç şeridini (input string) girin: ")
    
    verbose_choice = input("Adım adım çalışma detayları (verbose mode) gösterilsin mi? (E/H) [H]: ").strip().lower()
    verbose = verbose_choice == 'e'

    print("\nÇalıştırılıyor...\n")
    time.sleep(0.5)

    result = tm.run(input_str, max_steps=10000, verbose=verbose)

    print_header("Simülasyon Sonucu")
    print(f"Başarı Durumu: {'KABUL (ACCEPT)' if result.accepted else 'RET (REJECT)'}")
    print(f"Adım Sayısı:   {result.steps}")
    print(f"Son Şerit:     {result.final_tape}")
    
    if not result.accepted and result.reason != "rejected":
        print(f"Ret Sebebi:    {result.reason}")

if __name__ == "__main__":
    try:
        while True:
            main()
            print()
            cont = input("Başka bir makine çalıştırmak ister misiniz? (E/H) [E]: ").strip().lower()
            if cont == 'h':
                break
    except KeyboardInterrupt:
        print("\nÇıkış yapılıyor...")
