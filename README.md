# Kuaför / Berber Otomasyon Sistemi

## 🎯 Proje Konsepti
Bu proje, nesneye dayalı programlama (OOP) ilkeleri kullanılarak bir **Kuaför/Berber Otomasyon Sistemi** geliştirmeyi amaçlamaktadır. Sistem hem tek bir salon hem de çoklu salon desteği sunar. Amaç, OOP’nin temel prensiplerini (sınıf yapısı, kalıtım, çok biçimlilik, kapsülleme) somut bir yazılım ürününe dönüştürmektir.

## 🚀 Özellikler
- **Salon Yönetimi**
  - Salon tanımlama
  - Çalışma saatleri belirleme
  - Hizmetler (saç kesimi, boya, tıraş vb.) süre ve ücret bilgisiyle ekleme
- **Çalışan Yönetimi**
  - Personel kaydı
  - Uzmanlık alanları ve yapabildiği işlemler
  - Uygunluk zaman dilimleri
- **Randevu Sistemi**
  - Uygun çalışan ve hizmet seçerek randevu oluşturma
  - Çakışma kontrolü
  - Randevu detayları (işlem, süre, ücret, çalışan, tarih/saat)
  - Onay mekanizması
- **Kullanıcı Rolleri**
  - Müşteri
  - Çalışan (Personel)
  - Salon Yöneticisi / Admin

## 🛠️ Teknoloji
- Python & Django (örnek uygulama için)
- Bootstrap (UI için)
- SQLite / PostgreSQL (veritabanı)

## 📂 Kurulum
```bash
git clone <repo-url>
cd kuafor-otomasyon
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
