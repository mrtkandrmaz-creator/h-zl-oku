"""Tüm içerik burada: okuma metinleri, sorular ve kademeler.

Yeni metin eklemek için PASSAGES listesine yeni bir sözlük ekle.
Yeni kademe eklemek için LEVELS listesine yeni bir sözlük ekle.
"""

PASSAGES = [
    {
        "title": "Arıların Dansı",
        "text": (
            "Bal arıları, buldukları çiçek tarlasını kovandaki arkadaşlarına bir dansla anlatır. "
            "Bu dansa sallanma dansı denir. Arı sekiz şeklinde bir yol izler ve ortadaki düz çizgide "
            "gövdesini sallar. Çizginin güneşe göre açısı, çiçeklerin yönünü gösterir. Sallanma süresi "
            "ise mesafeyi belirtir; ne kadar uzun sallanırsa tarla o kadar uzaktadır. Kovandaki diğer "
            "arılar dansı karanlıkta antenleriyle takip eder ve aldıkları bilgiyle doğrudan hedefe uçar. "
            "Bu sayede koloni, yiyecek kaynaklarını çok kısa sürede keşfeder. Bilim insanları bu davranışı "
            "ayrıntılı biçimde incelemiş ve hayvanlar arasındaki en karmaşık iletişim biçimlerinden biri "
            "olarak kabul etmiştir."
        ),
        "questions": [
            {"q": "Tarlanın mesafesini ne gösterir?", "options": ["Sallanma süresi", "Dansın hızı", "Kanat sesi", "Sekizin büyüklüğü"], "answer": "Sallanma süresi"},
            {"q": "Çiçeklerin yönü neye göre belirlenir?", "options": ["Rüzgârın yönüne", "Çizginin güneşe göre açısına", "Kovanın konumuna", "Havanın sıcaklığına"], "answer": "Çizginin güneşe göre açısına"},
            {"q": "Diğer arılar dansı nasıl takip eder?", "options": ["Gözleriyle", "Kanatlarıyla", "Antenleriyle", "Ayaklarıyla"], "answer": "Antenleriyle"},
        ],
    },
    {
        "title": "Uyku ve Hafıza",
        "text": (
            "Uyku sırasında beyin dinlenmiyor, tam tersine yoğun bir temizlik ve düzenleme yapıyor. "
            "Gün boyunca öğrenilen bilgiler önce hipokampüs adı verilen bölgede geçici olarak saklanır. "
            "Derin uyku evresinde bu bilgiler uzun süreli hafızaya aktarılır. Aynı zamanda beyin, gün "
            "içinde biriken zararlı atıkları sıvı akışıyla dışarı atar. Araştırmalar, sınavdan önce "
            "yeterince uyuyan öğrencilerin, geceyi uykusuz geçirenlere göre daha çok bilgiyi hatırladığını "
            "gösteriyor. Bu yüzden ezber yapmak kadar iyi uyumak da öğrenmenin ayrılmaz bir parçasıdır. "
            "Yetişkinler için ortalama yedi ila dokuz saat uyku önerilir."
        ),
        "questions": [
            {"q": "Öğrenilen bilgiler önce nerede geçici olarak saklanır?", "options": ["Hipokampüs", "Kalp", "Omurilik", "Beyincik"], "answer": "Hipokampüs"},
            {"q": "Bilgiler hangi evrede uzun süreli hafızaya aktarılır?", "options": ["Uykuya dalarken", "Derin uyku evresinde", "Uyanırken", "Gün boyunca"], "answer": "Derin uyku evresinde"},
            {"q": "Yetişkinler için önerilen uyku süresi nedir?", "options": ["4-5 saat", "5-6 saat", "7-9 saat", "10-12 saat"], "answer": "7-9 saat"},
        ],
    },
    {
        "title": "Kâğıdın Yolculuğu",
        "text": (
            "Kâğıdın ilk kez Çin'de, yaklaşık iki bin yıl önce yapıldığı kabul edilir. Çinliler kâğıt "
            "yapımını yüzyıllar boyunca sır olarak sakladı. Sekizinci yüzyılda Orta Asya'da yaşanan bir "
            "savaştan sonra bu bilgi İslam dünyasına ulaştı. Semerkant'ta kurulan atölyeler kısa sürede "
            "Bağdat, Şam ve Kahire'ye yayıldı. Kâğıt, parşömene göre hem çok daha ucuzdu hem de üretimi "
            "kolaydı. Bu sayede kitaplar daha fazla kişiye ulaştı, kütüphaneler büyüdü. Kâğıt yapımı "
            "Avrupa'ya ise ancak on ikinci yüzyıldan itibaren İspanya üzerinden girdi. Matbaanın "
            "yaygınlaşması da bu ucuz malzeme sayesinde mümkün oldu."
        ),
        "questions": [
            {"q": "Kâğıt ilk olarak nerede yapıldı?", "options": ["Mısır", "Çin", "Hindistan", "Yunanistan"], "answer": "Çin"},
            {"q": "İslam dünyasında kâğıt atölyeleri ilk hangi şehirde kuruldu?", "options": ["Bağdat", "Şam", "Kahire", "Semerkant"], "answer": "Semerkant"},
            {"q": "Kâğıdın parşömene göre avantajı neydi?", "options": ["Daha dayanıklıydı", "Daha ucuz ve üretimi kolaydı", "Daha renkliydi", "Suya dayanıklıydı"], "answer": "Daha ucuz ve üretimi kolaydı"},
        ],
    },
    {
        "title": "Okyanusun Derinlikleri",
        "text": (
            "Okyanuslar Dünya yüzeyinin yaklaşık yüzde yetmişini kaplar, ama keşfedilen kısmı çok "
            "küçüktür. Güneş ışığı en fazla bin metre derinliğe kadar inebilir; bunun altı tamamen "
            "karanlıktır. En derin nokta olan Mariana Çukuru yaklaşık on bir kilometre derinliktedir. "
            "Orada basınç, deniz seviyesindekinin bin katından fazladır. Buna rağmen çukurun dibinde bile "
            "canlılar yaşar. Birçok derin deniz hayvanı karanlıkta kendi ışığını üretir ve bu özelliğe "
            "biyolüminesans denir. Bilim insanları, derin okyanusun yeni türlerle dolu olduğunu ve her "
            "keşif seferinde daha önce bilinmeyen canlılar bulunduğunu söylüyor."
        ),
        "questions": [
            {"q": "Okyanuslar Dünya yüzeyinin yaklaşık ne kadarını kaplar?", "options": ["Yüzde otuz", "Yüzde elli", "Yüzde yetmiş", "Yüzde doksan"], "answer": "Yüzde yetmiş"},
            {"q": "Güneş ışığı en fazla ne kadar derine inebilir?", "options": ["Yüz metre", "Bin metre", "Beş bin metre", "On bin metre"], "answer": "Bin metre"},
            {"q": "Karanlıkta ışık üretme özelliğinin adı nedir?", "options": ["Fotosentez", "Biyolüminesans", "Yansıma", "Floresan"], "answer": "Biyolüminesans"},
        ],
    },
    {
        "title": "Kahvenin Hikâyesi",
        "text": (
            "Kahvenin anavatanı Etiyopya olarak kabul edilir. Rivayete göre keçi çobanı Kaldi, "
            "keçilerinin bir çalının meyvelerini yedikten sonra uykusuz kaldığını fark etti. Kahve on "
            "beşinci yüzyılda Yemen'de içecek olarak hazırlanmaya başlandı. Oradan Mekke ve Kahire'ye, "
            "ardından Osmanlı topraklarına yayıldı. İstanbul'da ilk kahvehaneler on altıncı yüzyılın "
            "ortalarında açıldı ve kısa sürede insanların sohbet ettiği, satranç oynadığı, haberleri "
            "konuştuğu buluşma yerleri haline geldi. Avrupa'ya ise on yedinci yüzyılda Venedik "
            "tüccarları aracılığıyla girdi."
        ),
        "questions": [
            {"q": "Kahvenin anavatanı neresi kabul edilir?", "options": ["Yemen", "Brezilya", "Etiyopya", "Hindistan"], "answer": "Etiyopya"},
            {"q": "Kahve Yemen'de ne zaman içecek olarak hazırlanmaya başladı?", "options": ["On beşinci yüzyıl", "On altıncı yüzyıl", "On yedinci yüzyıl", "Sekizinci yüzyıl"], "answer": "On beşinci yüzyıl"},
            {"q": "Kahve Avrupa'ya kimler aracılığıyla girdi?", "options": ["Osmanlı askerleri", "Venedik tüccarları", "Çinli gezginler", "Haçlılar"], "answer": "Venedik tüccarları"},
        ],
    },
    {
        "title": "Işığın Hızı",
        "text": (
            "Işık boşlukta saniyede yaklaşık üç yüz bin kilometre hızla yol alır. Güneş'ten çıkan ışık "
            "Dünya'ya yaklaşık sekiz dakikada ulaşır; yani Güneş'e her baktığınızda onu sekiz dakika "
            "öncesinde olduğu gibi görürsünüz. Gökbilimciler uzaktaki yıldızları incelerken aslında "
            "geçmişe bakar. Bir ışık yılı, ışığın bir yılda aldığı yoldur ve bu bir zaman değil mesafe "
            "birimidir. Bize en yakın yıldız sistemi olan Proxima Centauri yaklaşık dört ışık yılı "
            "uzaktadır. Bugünkü en hızlı uzay araçlarıyla oraya gitmek on binlerce yıl sürerdi."
        ),
        "questions": [
            {"q": "Güneş'ten çıkan ışık Dünya'ya yaklaşık kaç dakikada ulaşır?", "options": ["Bir", "Sekiz", "Yirmi", "Altmış"], "answer": "Sekiz"},
            {"q": "Işık yılı neyin birimidir?", "options": ["Zamanın", "Hızın", "Mesafenin", "Parlaklığın"], "answer": "Mesafenin"},
            {"q": "Bize en yakın yıldız sistemi hangisidir?", "options": ["Sirius", "Proxima Centauri", "Betelgeuse", "Vega"], "answer": "Proxima Centauri"},
        ],
    },
    {
        "title": "Karıncaların Toplumu",
        "text": (
            "Karıncalar, binlerce hatta milyonlarca bireyden oluşan koloniler halinde yaşar. Her "
            "kolonide görev paylaşımı vardır: kraliçe yumurta bırakır, işçiler yiyecek toplar ve yuvayı "
            "onarır, askerler ise koloniyi korur. Karıncalar birbirleriyle koku bırakarak iletişim kurar. "
            "Yiyecek bulan bir işçi, dönüş yolunda yere özel bir kimyasal izi sürer ve diğerleri bu izi "
            "takip ederek aynı yere ulaşır. Bazı türler yaprakları kesip yuvaya taşır ve bunlarla mantar "
            "yetiştirir. Karıncalar bu yönleriyle doğadaki en düzenli toplumlardan biri olarak "
            "gösterilir."
        ),
        "questions": [
            {"q": "Kolonide yumurta bırakmaktan kim sorumludur?", "options": ["İşçiler", "Askerler", "Kraliçe", "Tüm karıncalar"], "answer": "Kraliçe"},
            {"q": "Karıncalar birbirleriyle nasıl iletişim kurar?", "options": ["Ses çıkararak", "Koku bırakarak", "Dans ederek", "Işık yayarak"], "answer": "Koku bırakarak"},
            {"q": "Bazı türler yaprakları ne için kullanır?", "options": ["Mantar yetiştirmek", "Yuvayı süslemek", "Yağmurdan korunmak", "Yavrularını beslemek"], "answer": "Mantar yetiştirmek"},
        ],
    },
    {
        "title": "Dil Öğrenmenin Sırrı",
        "text": (
            "Yeni bir dil öğrenmenin en etkili yolu, her gün kısa süre ama düzenli pratik yapmaktır. "
            "Araştırmalar, haftada bir kez üç saat çalışmanın, her gün yirmi dakika çalışmaktan daha az "
            "verimli olduğunu gösteriyor. Çünkü beyin bilgiyi tekrar ettikçe ve aralıklarla hatırladıkça "
            "güçlendirir. Bu yönteme aralıklı tekrar denir. Bir diğer önemli unsur ise konuşmaktan "
            "çekinmemektir. Hata yapmak öğrenme sürecinin doğal bir parçasıdır ve her hata, doğrusunu "
            "daha kalıcı biçimde öğrenmeyi sağlar. Müzik dinlemek, dizi izlemek ve kitap okumak da "
            "kelime dağarcığını sessizce genişletir."
        ),
        "questions": [
            {"q": "Metne göre hangisi daha verimlidir?", "options": ["Haftada bir kez üç saat", "Her gün yirmi dakika", "Ayda bir kez bir gün", "Sadece sınav öncesi"], "answer": "Her gün yirmi dakika"},
            {"q": "Bilgiyi aralıklarla hatırlama yönteminin adı nedir?", "options": ["Hızlı tekrar", "Aralıklı tekrar", "Sessiz okuma", "Toplu çalışma"], "answer": "Aralıklı tekrar"},
            {"q": "Metne göre hata yapmak nedir?", "options": ["Utanılacak bir durum", "Öğrenmenin doğal bir parçası", "Bırakma sebebi", "Zaman kaybı"], "answer": "Öğrenmenin doğal bir parçası"},
        ],
    },
]


LEVELS = [
    {
        "id": "baseline",
        "kind": "timed",
        "role": "baseline",
        "emoji": "🎯",
        "title": "Başlangıç Testi",
        "summary": "Mevcut okuma hızını ölç.",
        "passage": 0,
        "instruction": "Metni her zamanki gibi, anlayarak oku. Bitirince **Bitirdim**'e bas.",
        "lesson": """
### Önce nerede olduğunu bilmelisin 📏

Hızlı okuma yolculuğunun ilk adımı **mevcut hızını ölçmek**. Yetişkinlerin çoğu, anlayarak dakikada yaklaşık **200–250 kelime** okur.

**Nasıl çalışacak?**
1. Hazır olduğunda metni göstereceğiz ve sayaç başlayacak.
2. Metni normal hızında, anlayarak oku.
3. Bitirince **Bitirdim**'e bas; ardından 3 soruluk bir anlama testi gelecek.

> 🎯 Amacımız sadece hızlı değil, **anlayarak hızlı** okumak. Skorun: `kelime/dk × doğru oranı` (etkili okuma hızı).
""",
    },
    {
        "id": "subvocal",
        "kind": "timed",
        "role": "practice",
        "emoji": "🤫",
        "title": "İç Sesi Sustur",
        "summary": "Okurken kafandaki sesi azalt.",
        "passage": 1,
        "instruction": "Okurken **masaya ritmik şekilde parmağınla vur** (tık-tık-tık) ya da kafandan **1-2-3** diye say. Bitirince butona bas.",
        "lesson": """
### İç ses (subvokalizasyon) 🗣️

Çoğumuz okurken kelimeleri kafamızda **seslendiririz**. Bu alışkanlık, okuma hızını konuşma hızına (yaklaşık 150 kelime/dk) yaklaştırır.

**İç sesi azaltmanın yolları:**
- Okurken **ritim tut** (parmakla masaya tık-tık).
- Kafanda **1-2-3** diye say; zihin seslendirmeye yer bulamaz.
- Kelimeleri tek tek değil, **anlam olarak** yakalamaya çalış.

> 💡 İç sesi tamamen kaldırmak şart değil. Hedef onu **azaltmak** ve gözün hızına yetişmesine izin vermek.

**Egzersiz:** Ritim tutarak oku ve anlamayı kaçırma!
""",
    },
    {
        "id": "pointer",
        "kind": "pacer",
        "role": "practice",
        "emoji": "👆",
        "title": "Rehber Tekniği",
        "summary": "Gözünü düzgün ve sabit hızda yönlendir.",
        "passage": 2,
        "instruction": "Vurgulanan kelimeyi **gözünle takip et**. Hızı kendine göre ayarla, **Başlat**'a bas.",
        "lesson": """
### Parmak, kalem ya da imleç 🖍️

Gözlerimiz okurken kayarak değil, **sıçrayarak** ilerler. Kontrolsüz sıçramalar ve geri dönüşler hızı düşürür.

Bir **rehber** (parmak ucu, kalem) gözü sabit bir hızda ve düz bir çizgide ilerletir:
- Gözün rehberi takip eder, ritim oluşur.
- Dikkatin dağılması azalır.
- Hızı rehberle **kendin belirlersin**.

**Egzersiz:** Ekranda vurgulanan kelime sabit hızla ilerleyecek. Gözünü onunla birlikte taşı.
""",
    },
    {
        "id": "chunking",
        "kind": "chunk",
        "role": "practice",
        "emoji": "👁️",
        "title": "Göz Alanını Genişlet",
        "summary": "Kelime öbeklerini tek bakışta yakala.",
        "passage": 3,
        "instruction": "Ekranın ortasında beliren **kelime öbeklerine** odaklan. Öbek boyutunu ve hızı seç, **Başlat**'a bas.",
        "lesson": """
### Kelime kelime değil, öbek öbek 🧩

Hızlı okuyucular kelimeleri tek tek okumaz; bir bakışta **2-4 kelimelik öbekler** yakalar.

**Neden işe yarar?**
- Göz sıçrama sayısı azalır.
- Anlam, kelime gruplarında daha doğal taşınır.
- Hız farkında olmadan artar.

**Egzersiz:** Kelimeler ekranın ortasında öbekler halinde parlayacak. Gözünü hareket ettirme, sadece odaklan ve anlamı yakala.
""",
    },
    {
        "id": "regression",
        "kind": "reveal",
        "role": "practice",
        "emoji": "🚫",
        "title": "Geri Dönme!",
        "summary": "Geri dönüp tekrar okuma alışkanlığını kır.",
        "passage": 4,
        "instruction": "Cümleler **tek tek** görünüp kaybolacak. Geri dönemezsin! Hızı seç ve **Başlat**'a bas.",
        "lesson": """
### Regresyon: gereksiz geri dönüşler ↩️

Çoğu okuyucu farkında olmadan **aynı satıra ya da cümleye geri döner**. Bu, hızı ciddi biçimde düşürür.

**Çözüm:**
- Cümle bitince **ilerle**, güven: anlam çoğu zaman devamında netleşir.
- Gerçekten kaçırdığın bir şey varsa, işaretle ve **bölümün sonunda** dön.

**Egzersiz:** Cümleler tek tek gösterilecek ve önceki cümle kaybolacak. Geri dönemezsin; güvenmeyi öğren!
""",
    },
    {
        "id": "speedramp",
        "kind": "ramp",
        "role": "practice",
        "emoji": "🚀",
        "title": "Hız Basamakları",
        "summary": "Hızını kademeli olarak zorla.",
        "passage": 5,
        "instruction": "Metin üç aşamada gelecek ve her aşamada **hız artacak**. Odaklan, **Başlat**'a bas.",
        "lesson": """
### Konfor alanının dışına çık 📈

Hız artışı **kademeli** olmalı. Hızı birden iki katına çıkarırsan anlama düşer.

**Strateji:**
1. Rahat hızında başla.
2. Hızı %15 artır, anlamayı koru.
3. Bir adım daha artır, nerede anlamanın bozulduğunu fark et.

> ⚖️ En iyi okuma hızı, **anlamanın hâlâ yüksek olduğu en yüksek hızdır.**

**Egzersiz:** Başlangıç hızına göre 3 aşamalı bir hız merdiveni çıkacaksın.
""",
    },
    {
        "id": "final",
        "kind": "timed",
        "role": "final",
        "emoji": "🏆",
        "title": "Final Sınavı",
        "summary": "Öğrendiklerini birleştir, gelişimini gör.",
        "passage": 6,
        "instruction": "Öğrendiğin tüm teknikleri kullan: **ritim**, **rehber**, **öbek okuma**, **geri dönme yok**. Bitirince butona bas.",
        "lesson": """
### Büyük final 🏁

Şimdi tüm tekniklerini bir araya getirme zamanı:

- 🤫 İç sesi azalt (ritim ya da sayma)
- 👆 Gözünü sabit bir rehberle ilerlet
- 👁️ Kelime öbekleri yakala
- 🚫 Geri dönme

Sonunda başlangıç hızınla karşılaştırılacaksın. Unutma: sayılan şey **etkili okuma hızı** (hız × anlama).

Başarılar! 🍀
""",
    },
]
