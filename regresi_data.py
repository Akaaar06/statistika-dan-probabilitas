import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Mengambil folder tempat file ini berada otomatis
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Jalur file pendek (Menyesuaikan folder UAS Stapro milikmu)
file_path = os.path.join(BASE_DIR, "final_data_steam.csv")

if not os.path.exists(file_path):
    print("Error: File 'final_data_steam.csv' belum ada. Jalankan proses pembersihan data Steam terlebih dahulu.")
    exit()

df = pd.read_csv(file_path)

# 1. Tentukan Y dan X
# Y adalah Waktu Bermain
y = df["Waktu Bermain"]

# PENTING: Kita hapus "Nama Game" dan "Waktu Bermain" HANYA untuk perhitungan model
X = df.drop(columns=["Nama Game", "Waktu Bermain"])

# 2. Split data (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Training model
model = LinearRegression()
model.fit(X_train, y_train)

# 4. Prediksi
pred = model.predict(X_test)

# 5. Tampilkan Hasil Teks di Terminal (Format bersih tanpa '_')
print("======================= ANALISIS REGRESI =======================")
print("Variabel Y: Waktu Bermain")
print(f"R² Score: {r2_score(y_test, pred):.4f}")
print("\nIntercept (Konstanta):", model.intercept_)

print("\nKoefisien Variabel X (Pengaruh tiap parameter):")
nama_fitur_bersih = []
for nama, coef in zip(X.columns, model.coef_):
    # Mengganti karakter '_' dengan spasi agar rapi saat dicetak
    nama_bersih = nama.replace("_", " ")
    nama_fitur_bersih.append(nama_bersih)
    print(f"- {nama_bersih}: {coef:.4f}")
print("================================================================")

# 6. Pembuatan Visualisasi Grafik (Kembar dengan Versi Kinerja Karyawan)
print("\n[Membuka jendela grafik visualisasi data Steam...]")

# Mengatur gaya tampilan grafik agar terlihat profesional
sns.set_theme(style="whitegrid")
plt.figure(figsize=(14, 6))

# SUBPLOT 1: Grafik Batang Koefisien (Pengaruh Parameter Game)
plt.subplot(1, 2, 1)
sns.barplot(x=model.coef_, y=nama_fitur_bersih, palette="magma")
plt.axvline(x=0, color='black', linestyle='--', linewidth=1)
plt.xlabel("Nilai Koefisien Regresi")
plt.ylabel("Parameter Game Steam")
plt.title("Tingkat Pengaruh Tiap Parameter terhadap Waktu Bermain")

# SUBPLOT 2: Scatter Plot Nilai Aktual vs Hasil Prediksi Waktu Bermain
plt.subplot(1, 2, 2)
sns.scatterplot(x=y_test, y=pred, color="purple", alpha=0.5, s=60)
# Garis diagonal merah sebagai acuan kecocokan sempurna
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color="red", linestyle="--", lw=2)
plt.xlabel("Waktu Bermain Aktual")
plt.ylabel("Waktu Bermain Prediksi")
plt.title("Perbandingan Waktu Bermain Aktual vs Prediksi")

# Menyesuaikan tata letak agar tidak saling bertumpuk
plt.tight_layout()

# Menampilkan grafik ke layar
plt.show()