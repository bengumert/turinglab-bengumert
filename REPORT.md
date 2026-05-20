# TuringLab Proje Raporu

**Öğrenci:** Emine Bengü Mert  
**Ders:** Otomata Teorisi ve Biçimsel Diller  

---

## 1. Giriş
Bu proje kapsamında, tek şeritli deterministik Turing Makineleri (Single-Tape Deterministic Turing Machine) tasarlamak, test etmek ve yürütmek amacıyla özel bir Python kütüphanesi (TuringLab) geliştirilmiştir. Turing makineleri, bilgisayar bilimlerinin temel teorik modellerinden biri olup modern algoritmaların hesaplanabilirlik sınırlarını çizer. Bu projenin amacı, teorik Turing makinesi davranışlarını pratik bir yazılım mühendisliği disiplini (TDD, modüler kod yapısı) ve kullanıcı dostu veri tanımlama (YAML) dilleriyle entegre etmektir. 

## 2. Mimari ve Tasarım Kararları
TuringLab kütüphanesi, performansı artırmak ve Python ekosisteminin avantajlarını kullanmak üzere tasarlanmıştır:
- **Şerit (Tape) Yapısı:** Sonsuz şerit temsili için klasik `list` veya `string` yerine **sparse dictionary** (`dict[int, str]`) kullanılmıştır. Böylece şeridin sağa veya sola sonsuz genişlemesi herhangi bir maliyet (O(n) kopyalama işlemi) veya negatif indeks "taşma (overflow)" hatası yaratmamaktadır.
- **Geçiş (Transition) Motoru:** YAML dosyalarından okunan geçişler, çalışma zamanında `Dict[Tuple[str, str], Tuple[str, str, str]]` formatında bir hash tablosuna dönüştürülmüştür. Bu sayede her bir okuma-yazma adımındaki lookup işlemi O(1) sabit zaman maliyetine indirilmiştir.
- **Nesne Yönelimli Yaklaşım:** Kod tabanı `SingleTapeTM`, `Tape`, `StepConfig` ve `RunResult` gibi sınıflara/veri yapılarına bölünerek modülerlik ve okunabilirlik maksimize edilmiştir. 
- **Durum (State) Yönetimi:** Kod hiçbir zaman öngörülemeyen bir hata ile (exception) çökmez. Bulunamayan geçişler `no_transition`, sonsuz döngüler ise `timeout` dönerek `RunResult` objesi üzerinden yönetilir.

## 3. Tasarlanan Turing Makineleri
Projede dört farklı Turing Makinesi algoritması geliştirilmiş ve entegre test süreçlerinden geçirilmiştir:

1. **Unary to Binary (TM-1):** Şeritte bulunan 1'lerden oluşan (unary) girdiyi, ikili (binary) formata çevirir. Sürekli uzayan binary sayının unary diziyle çarpışmasını engellemek için dinamik olarak sağa kaydırma (shift-right) alt yordamı geliştirilmiştir.
2. **Binary Compare (TM-2):** "A#B" formatındaki iki binary sayının büyüklüğünü (A > B) kıyaslar. 3 aşamadan (Leading Zero Elimination, Length Comparison, Value Comparison) oluşan karmaşık bir ping-pong algoritmasıyla O(N^2) zamanda sonuca ulaşır.
3. **String Copy (TM-3):** Şeritteki `{a,b}` kelimelerini sonuna `#` ekleyerek kendisinin kopyasını şeride yazar (`w#w`).
4. **Palindrome Checker (TM-4):** Şeridin iki ucundaki karakterleri merkeze doğru tüketerek (silerek) eşleşme kontrolü yapar. Hem tek hem çift uzunluktaki palindromları sorunsuz işleyen, `O(N^2)` karmaşıklığında çalışan optimal bir tasarımdır.

## 4. Kavramsal Tartışma: Halting Problemi
**Soru:** *TuringLab simülatörü içerisinde başka bir Turing makinesinin girdi üzerinde durup durmayacağını (Halting Problem) kesin olarak çözen genel bir YAML makinesi tasarlamak mümkün müdür?*

**Cevap:** Hayır, kesinlikle mümkün değildir. Alan Turing'in 1936'da ispatladığı üzere, Halting (Durma) problemi algoritma ile **çözülemeyen (undecidable)** bir problemdir. TuringLab motoru fiziksel bellek ve zamanla sınırlı olsa da teorik olarak Turing makinesi modelini uygular. Eğer Halting problemini çözen bir `H` makinesi yazılsaydı, bu `H` makinesini girdi olarak alıp kendi tersini yapan bir `D` (Deceiver) makinesi inşa edilebilirdi. `D`, `H`'a göre eğer duracaksa sonsuz döngüye girer, durmayacaksa dururdu. Bu bir paradokstur.

Pratikte TuringLab, makinelerin durup durmayacağını bilmediği için basit bir "kısa devre" mekanizması olarak `max_steps` (timeout) kullanır. Bu bir çözüm değil, makinenin simülatörü kilitlemesini engelleyen mühendislik önlemidir. 

## 5. Sınırlar ve İleri Çalışma
TuringLab şu an oldukça kararlı çalışmasına rağmen tek şeritli bir makinedir. 
- **Zaman Karmaşıklığı:** Algoritmalar (String Copy vb.) O(N) zamanda çözülebilecekken tek şerit zorunluluğu nedeniyle O(N^2) sürmektedir. Gelecekte Multi-Tape (Çoklu Şerit) desteği eklendiğinde zaman karmaşıklıkları optimize edilebilecektir.
- **Determinizm Sınırları:** Sadece deterministik geçişlere izin verilmektedir. Nondeterministic Turing Machine (NTM) desteği eklenmesi (bir durumdan ağaç yapısında birden çok yola sapabilme) projenin teorik kapsamını genişletecektir.
- **Görselleştirme:** Konsol bazlı `verbose` modu kullanışlıdır ancak ileride PyQt veya web tabanlı animasyonlu bir arayüz eklenebilir.

## 6. Kaynakça
- Sipser, M. (2012). *Introduction to the Theory of Computation* (3rd ed.). Cengage Learning.
- Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation*. Addison-Wesley.
