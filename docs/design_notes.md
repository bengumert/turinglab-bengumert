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
