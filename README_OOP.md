# Kuaför / Berber Otomasyon Sistemi — OOP Raporu

## 🎯 Proje Konsepti
Bu proje, nesneye dayalı programlama (OOP) ilkeleri kullanılarak bir **Kuaför/Berber Otomasyon Sistemi** geliştirmeyi amaçlamaktadır. Django framework’ü üzerinde inşa edilen sistem, hem tek bir salon hem de çoklu salon desteği sunar. Proje, ödevde belirtilen gereksinimleri karşılamak üzere salon tanımları, çalışan yönetimi, randevu sistemi ve kullanıcı rolleri gibi modülleri içerir.

---

## 🚀 Ödev Gereksinimlerinin Karşılanması
- **Salon Tanımlamaları**: Salon bilgileri, çalışma saatleri ve hizmetler (ör. saç kesimi, boya, tıraş) tanımlanmıştır. Her hizmetin süresi ve ücreti model alanlarıyla saklanır.  
- **Çalışan Yönetimi**: Personel kayıtları tutulur. Çalışanların uzmanlık alanları (`specialties`) ve uygunluk zaman dilimleri (`Availability`) modellerde yer alır.  
- **Randevu Sistemi**: Randevu oluşturma, çakışma kontrolü ve onay mekanizması vardır. Randevu detayları (işlem, süre, ücret, çalışan, tarih/saat) kaydedilir.  
- **Kullanıcı Rolleri**: `Person` modeli üzerinden müşteri, çalışan ve admin rolleri tanımlanmıştır. Proxy modeller (`Customer`, `Employee`) ile ayrı görünümler sağlanır.  

---

## 🛠️ OOP İlkeleri ve Projede Kullanımı
- **Sınıf Yapısı**: `Salon`, `Service`, `Person`, `Appointment` gibi sınıflar ayrı sorumluluklarla tanımlanmıştır. Bu, **Single Responsibility Principle**’a uygundur.  
- **Kalıtım (Inheritance)**: `Person` sınıfından `Customer` ve `Employee` proxy modelleri türetilmiştir. Ortak özellikler üst sınıfta, özel davranışlar alt sınıflarda yer alır.  
- **Çok Biçimlilik (Polymorphism)**: `is_customer` ve `is_employee` gibi property’ler, aynı `Person` nesnesinin farklı rollerde davranmasını sağlar.  
- **Kapsülleme (Encapsulation)**: Çalışanların uygunluk bilgileri (`Availability`) doğrudan erişilemez, doğrulama (`clean`) metoduyla kontrol edilir. Bu veri bütünlüğünü sağlar.  

---

## 📐 Tasarım Desenleri ve Mimari
- **MVT**: Django’nun model, view ve template yapısı kullanılarak MVT mimarisi uygulanmıştır.  
- **Observer Pattern**: Randevu onay mekanizmasında müşteri ve çalışan bilgilendirmesi için kullanılabilir.  
- **Factory Pattern**: Yeni hizmet veya kullanıcı oluşturma sürecinde nesne üretimini kolaylaştırır.  

---

## 📊 UML Diyagramı (Metinsel)
Salon
├── name 
├── address 
├── opening_time 
├── closing_time 
└── services[]

Service 
├── name 
├── duration 
├── price 
└── salon

Person 
├── username 
├── phone_number 
├── role 
└── salon

Customer(Person) 
Employee(Person) 

Appointment 
├── customer 
├── employee 
├── service 
├── date_time 
└── status


---

## 📌 Sonuç
Bu proje, ödevde belirtilen gereksinimleri karşılamakta ve OOP’nin temel ilkelerini somut bir yazılım ürününe dönüştürmektedir. Sınıf yapısı, kalıtım, çok biçimlilik ve kapsülleme ilkeleri uygulanmış; MVT gibi tasarım desenleri kullanılmıştır. Sistem hem tek salon hem de çoklu salon desteği sunarak gerçek hayata uyarlanabilir bir çözüm haline gelmiştir.
