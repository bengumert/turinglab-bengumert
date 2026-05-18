# TuringLab

**Öğrenci:** Emine Bengü Mert  
**Ders:** Otomata Teorisi ve Biçimsel Diller · Bilgisayar Mühendisliği  
**Üniversite:** Selçuk Üniversitesi  

TuringLab, deterministik tek şeritli (single-tape) Turing makinelerini tasarlamak, test etmek ve görselleştirmek için geliştirilmiş modüler bir Python projesidir.

Proje, makinelerin tasarımlarını bağımsız YAML dosyalarından dinamik olarak yükleyerek çalıştırır.

## Özellikler

- **O(1) Karmaşıklıklı Şerit Mimarisi:** Sonsuz şerit simülasyonu için string işlemleri yerine "sparse dictionary" mantığı kullanılarak yüksek performans elde edilmiştir.
- **YAML Konfigürasyonu:** Turing makineleri kod karmaşası yaratmadan tamamen harici YAML dosyalarından yüklenir.
- **Adım Adım İzleme (Verbose Mod):** Her bir adımda kafa pozisyonu, güncel durum, şerit içeriği ve yön (L/R) ekrana yazdırılır.
- **Edge-Case Yönetimi:** Timeout (sonsuz döngü engelleme) ve No Transition (eksik geçiş) durumları gracefully handle edilir.
- **TDD (Test Driven Development):** Motor ve tasarlanan tüm makineler PyTest ile 100% senaryo uyumlu test edilmiştir.

## Dosya Yapısı

```
turinglab-eminebengumert/
├── turinglab/             # Core Turing Machine Engine
│   ├── __init__.py
│   └── tm_engine.py       # Tape & SingleTapeTM classes
├── machines/              # Turing Machine Tasarımları (YAML)
│   ├── unary_to_binary.yaml
│   ├── binary_compare.yaml
│   ├── string_copy.yaml
│   └── palindrome_checker.yaml
├── tests/                 # Unit test klasörü
│   ├── test_tm_engine.py
│   └── test_machines.py
├── docs/                  # Proje dökümantasyonları
│   └── design_notes.md    # Tasarım kararları ve algoritmik notlar
├── demo.py                # İnteraktif simülasyon aracı
└── requirements.txt       # Proje bağımlılıkları (pytest, pyyaml)
```

## Makineler (Tasarım Atölyesi)

1. **TM-1: Unary to Binary (`unary_to_binary.yaml`)**
   - Unary formatındaki (111) bir sayıyı, tek şeritte yaşanan çarpışmaları dinamik olarak sağa kaydırarak engelleyen gelişmiş bir algoritma ile Binary (11) formata dönüştürür.
2. **TM-2: Binary Compare (`binary_compare.yaml`)**
   - İki ikili sayıyı (Örn: `1011#1100`) karşılaştırır. 3 aşamalı (baştaki sıfırları atma, uzunluk karşılaştırma ve bit-by-bit değer kıyaslama) zigzag algoritması ile A > B durumunu test eder.
3. **TM-3: String Copy (`string_copy.yaml`)**
   - Verilen bir `{a, b}` metnini `w#w` formatında kopyalar.
4. **TM-4: Palindrome Checker (`palindrome_checker.yaml`) (Öğrenci Seçimi)**
   - Çift yönlü şerit tüketme algoritmasıyla verilen stringin palindrom olup olmadığını kontrol eder. Tekli, çiftli ve empty string varyasyonlarını destekler.

## Kurulum ve Çalıştırma

Proje bağımlılıklarını kurmak için:

```bash
pip install -r requirements.txt
```

### İnteraktif Demo
Terminal üzerinden makineleri interaktif test edebileceğiniz arayüz:

```bash
python demo.py
```

### Testleri Çalıştırma
Tüm makinelerin ve çekirdek motorun doğruluğunu PyTest ile otomatik doğrulamak için:

```bash
pytest
```

## Tasarım Notları (Design Notes)
Makinelerin yapım aşamasında izlenen algoritmik stratejiler, şerit alfabesi seçimleri, zaman karmaşıklıkları (Big-O analizleri) ve geliştirme sırasında karşılaşılan hataların çözümleri `docs/design_notes.md` dosyasında detaylıca açıklanmıştır.