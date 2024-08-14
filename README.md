# Web-Trafik-Loglarina-Dayali-Yapay-Zeka-Destekli-Soru-Cevap-Sistemi


-- RAPOR --

Projeyi google colab üzerinden yürüttüm. Sistem: L4 GPU / sistem ram: 53gb / gpu ram: 22.5 / 



Aşama 1: Veri Hazırlığı ve Ön İşleme:

*(Ödevdeki tüm veri ödevin bir parçası olarak ödevi yapan tarafından üretilmelidir.)
Log formatını ve random kütüphanesini kullanarak veri seti ürettim.

* Log dosyasındaki gerekli verileri seçin, temizleyin ve yapılandırın (örneğin, IP adresleri, erişilen sayfalar, zaman damgaları gibi verileri ayıklayın) projeye bu noktayı entegre etmek için log formatında boş 2 sütun ayarladım. Boş sütunları .drop() ile kaldırdıktan sonra loga ait time kısmını yeniden yapılandırdım. Request kısımını veriyi daha detaylı ele alabilmek için 3 parçaya bölerek kendisini ve diğer parçalarda ortak olan kısımı(protocol) .drop() ile veri setinden sildim.

2000 adet log üretmek üzere kodun bu kısmını tamamladım.

* Bu log verilerini vektörlere dönüştürüp, uygun bir vektör veri tabanına (örneğin, FAISS, Pinecone) yükleyin.
Aşama-1 içinde elde ettiğimiz verilerin sayısal vektörlere dönüştürülmesini bu kısımda yapıyorum. Amacım, verileri  makinenin öğrenebileceği formata haline getirmek. Bunun için 'sentence-transformers/all-MiniLM-L6-v2' modelini kullanıyorum.

Son olarak elde ettiğim vektörleri FAISS kullanarak indexliyorum.



Aşama 2: RAG Modelinin Kurulumu:

* Bilgi Alma: Vektör veri tabanını kullanarak, kullanıcı sorusuna en uygun log kayıtlarını bulun.
Bu kısım için FAISS index kullanıyorum.

* Jeneratif Model: Bulduğunuz log kayıtlarını kullanarak, kullanıcının sorusuna uygun bir yanıt oluşturmak için bir dil modeli (örneğin, GPT, T5) kullanın.
  Log kayıtlarına dayanarak anlamlı output üretmek için Openai kütüphanesi install edip Gpt 3.5 kullanıyorum fakat memnun kalmadığım için gpt 4 / 3.5 turbo deniyorum, ücretli API talebi sonrası T5 kullanımına karar kılıyorum. Burada işler karışıyor. Bunlara sonra değineceğim. İlk olarak "t5-small" kullanıyorum.



Aşama 4: Performans Değerlendirmesi:

* Geliştirdiğiniz sistemin doğruluğunu ve performansını değerlendirin.
* Sistemin cevaplarının kalitesini artırmak için hangi iyileştirmelerin yapılabileceğini düşünün ve bu konuda önerilerde bulunun.

Projenin bu kısımında ince ayarlar yaptım. Uzun bekleyiş sonrası T5(small) den mantıklı/anlamlı outputlar alamayınca en başta log ürettiğim yerdeki 2000 adet değerini 10.000 yapıyorum.  Model yetersiz kaldı uyarısından sonra "t5-large" modelini entegre ediyorum. Çalışma alanım sistemin yetersiz kalması nedeniyle çöküyor. "t5-base" modeline geçiş yapıyorum. Uzun bekleyiş sonrası mantıklı çıktı alamayınca 10.000 kısmını hızlı test yapmak için 100 e indiriyorum. Burada öncekilere kıyasla mantıklı çıktılar aldığım için verim amaçlı "t5-small" deniyorum. Aynı çıktılar sonucu son ayarlar olarak -100 adet log ve "t5-small"- kullanımı üstüne karar kılıyorum. 

Sistemin cevaplarının kalitesini artırmak için Gpt-4 AI kullanarak veri setine ait anahtar kelimeler ile inputu cevaba göre filtrelemek üzere kod yazdırıyorum. AI'dan gelen kodu projeye entegre sonrası cevap kalitesinde anlaşılabilir bir doğruluk oranı artışı yakalıyorum. 

Önerilen iyileştirmeler: Gelir/gider dengesi gözetilerek projenin verimi üzerinde artış için GPT-4 ücretli API alınabilir.



Projenin tüm adımlarında aktif bir şekilde ChatGPT kullandım. Saniyeler içerisinde AI dan alınabilecek ve denetlenebilecek kod parçaları için enerji harcamaya gerek duymuyorum. Yapay zekanın teknik işlerdeki verimi artırmak amacıyla kullanımına tamamıyla açığım. 2030 gibi halen daha AI kullanmayan bilişimcilerin ayakta kalamayacağı kanaatindeyim. AI = verim.








