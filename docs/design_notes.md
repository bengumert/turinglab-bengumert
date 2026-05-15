# TuringLab - Design Notes

## TM-1: Unary to Binary (unary_to_binary.yaml)

**1. Strateji:**  
Turing makinesinin yüksek seviyeli algoritması, unary sayının başından başlayarak her bir '1'i sırayla 'X' ile işaretlemeye dayanır. Her bir işaretleme işlemi sonrasında kafa, şeridin sağına (boşluğa) gider ve orada tutulan ikili (binary) sayıyı bir artırır (binary increment). Ancak ikili sayının her adımda sola doğru büyümesi ve 'X'lere çarpmasını engellemek için, ikili sayı ile unary dizi arasındaki boşluk (gap) her döngüde kontrol edilir. Eğer boşluk kapanmışsa, ikili sayı bütünüyle bir hücre sağa kaydırılır (shift right). En sonunda sadece ikili sayı kalır.

**2. Durum Sayısı:**  
13 durum kullanıldı. Makinenin yapması gereken iş çok yönlü olduğu için (sağa gitme, boşluk kontrolü, sağa kaydırma, ikili artırma ve sola dönme) her bir alt fonksiyon için ayrı durum setleri gerekti. Ancak alt yordamlar modüler tasarlandığı için daha az durumla yapmak okunabilirliği aşırı düşürürdü.

**3. Şerit Alfabesi Seçimi:**  
Şartnamede verilen `{1, 0, B, X}` kullanıldı. `X`, unary sayının işlenmiş kısımlarını tutmak için, `B` ise unary sayı ile binary sayı arasında hareketli bir bariyer/boşluk olarak görev yaptı. Ek bir işaretleyici kullanılmadı.

**4. Karmaşıklık:**  
Girdi uzunluğu n olsun. Her '1' sembolü için kafa tüm diziyi bir kez sağa ve bir kez sola tarar. Kaydırma (shift) işlemi yalnızca log(n) adımda bir gerekir ve O(log n) sürer. Dolayısıyla genel zaman karmaşıklığı O(n^2)'dir. Bu, tek şeritli bir makine için oldukça verimli bir çözümdür.

**5. Hata Ayıklama Hikayesi:**  
Geliştirme sırasında karşılaştığım en büyük bug, ikili sayının sola doğru büyümesi (örneğin `11` -> `100` olurken) sonucu unary diziden kalan `X`'leri üzerine yazarak yok etmesiydi. Şeritteki boşluğun 0'a indiği anları yakalayamadığım için "1111" girdisinde makine "111" çıktısı üretiyordu. Bunu çözmek için `q_check_gap` ve `q_shift` alt yordamlarını yazdım: Kafa, ikili sayıya ulaşmadan hemen önce `B` yerine doğrudan `1` okursa, çarpışma olacağını anlar ve tüm ikili sayıyı bir hücre sağa kaydırarak kendisine yeni bir `B` boşluğu açar. Bu sayede makine O(n) uzunluktaki girdilerde bile kusursuz çalışır hale geldi.


## TM-2: Binary Compare (binary_compare.yaml)

**1. Strateji:**  
Makine üç ana aşamadan oluşur:
- **Aşama 0 (Leading Zeros):** Sayıların başındaki anlamsız '0'lar (leading zeros) tespit edilip özel 'L' sembolüyle maskelenir. Bu sayede '0010' ile '10' aynı uzunlukta kabul edilir.
- **Aşama 1 (Length Compare):** İki sayının uzunlukları (L ile maskelenmemiş bit sayıları) karşılıklı olarak işaretlenerek (A_0, B_1 vb.) karşılaştırılır. A daha uzunsa anında kabul (A > B), B daha uzunsa anında ret durumuna geçilir.
- **Aşama 2 (Value Compare):** Eğer uzunluklar eşitse, en soldaki en anlamlı bitten (MSB) başlanarak işaretler teker teker kaldırılır ve bitler kıyaslanır. İlk farklılıkta (1 vs 0) karar verilir.

**2. Durum Sayısı:**  
Yaklaşık 21 durum kullanıldı. Problemin doğası gereği üç farklı faz var (önden sıfır atma, uzunluk sayma, bit bit değer kıyaslama). Bu aşamaların her biri sağa git, sola dön, karakterleri hatırla (remember_0, remember_1) gibi durumları içerdiği için durum sayısı artmıştır.

**3. Şerit Alfabesi Seçimi:**  
Girdi alfabesine ek olarak maskelenmiş bitler için 'L' (Leading Zero) ve geçildiğini hatırlamak için 'A_0', 'A_1', 'B_0', 'B_1' sembolleri kullanıldı. Bu semboller fazlar arasında sayının orijinal değerini kaybetmeden üzerinden geçildiğini anlamak için hayati önem taşır.

**4. Karmaşıklık:**  
Her bir bit için tüm şerit baştan sona taranır. Bu nedenle algoritmanın zaman karmaşıklığı O(N^2) düzeyindedir (N = şerit uzunluğu). Tek şeritli bir TM'de bu işlem mecburi bir zigzag (ping-pong) mekanizması gerektirdiği için O(N^2) alt sınır kabul edilebilir.

**5. Hata Ayıklama Hikayesi:**  
Geliştirme sırasında ilk testlerde makinenin '1101#1011' testinde A tarafındaki işlenmiş (0 ve 1) sayıları B'nin sayıları sanarak yanlış yere B_1 yazması sorunuyla karşılaştım. '# ' sembolünü net bir 'sınır kapısı' (boundary) olarak kullanmam gerektiğini anladım ve 'q_phase_1_go_B' durumunu ikiye böldüm: Önce A'nın bitlerini atlayıp '#' karakterine ulaşan, ardından '#' karakterini geçtikten sonra B'nin bitlerini arayan iki durum tasarlandı.


## TM-3: String Copy (string_copy.yaml)

**1. Strateji:**  
Makine, kopyalama işlemine başlamadan önce orijinal stringin sonuna '#' ayıracını koyar. Ardından soldan sağa doğru her bir karakteri okur, okuduğu 'a' veya 'b' karakterini sırasıyla 'X' veya 'Y' olarak işaretler. Kafa, boş şeridin sonuna kadar sağa gidip ilgili karakteri yazar. Sonra tekrar sola dönerek orijinal string içindeki ilk işaretlenmemiş (X/Y olmayan) karaktere gelir. Bu ping-pong işlemi '#' sembolüne gelene kadar devam eder. Son aşamada makine sola doğru tarama yaparak tüm 'X' ve 'Y' işaretlerini tekrar 'a' ve 'b'ye dönüştürür (cleanup).

**2. Durum Sayısı:**  
8 durum kullanıldı. Problem son derece düzenli ve standart bir örüntüye sahip olduğundan, kopyalama (q_copy), sağa gitme (q_go_end_a, q_go_end_b), sola dönme (q_return) ve temizleme (q_cleanup) aşamaları yeterli oldu. 

**3. Şerit Alfabesi Seçimi:**  
Girdi alfabesi {a, b} ve ayıraç # haricinde kopyalanan karakterlerin takibi için {X, Y} kullanıldı.

**4. Karmaşıklık:**  
N uzunluğunda bir string için, her bir karakterin kopyalanması şeridin sonuna gidip dönmeyi gerektirir. Birinci karakter için yaklaşık 2 adım, ikinci karakter için 4 adım... N'inci karakter için 2N adım yol katedilir. Toplam zaman karmaşıklığı aritmetik dizinin toplamı gibi hesaplanır ve O(N^2) bulunur.

**5. Hata Ayıklama Hikayesi:**  
Bu makinenin tasarımı en sorunsuz geçen aşamalardan biriydi. Sadece boş string ("") girdisinde nasıl davranacağı kafa karıştırıcı olabilirdi; q_start durumunda şerit boşsa doğrudan sola '#' yazıp temizleme işlemine geçerek çıktının başarılı bir şekilde '#' olmasını sağladım.
