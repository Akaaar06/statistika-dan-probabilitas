import pandas as pd
import os

# Alamat file lengkap
file_path = "d:/Araaav/OneDrive - Universitas Tadulako/Documents/VSCode-2026/UAS Stapro/steam.csv"

if not os.path.exists(file_path):
    print(f"Error: File tidak ditemukan di {file_path}")
    exit()

df = pd.read_csv(file_path)

# Fungsi konversi rentang owners jadi angka tunggal
def parse_owners(owner_str):
    try:
        low, high = [int(x.replace(',', '')) for x in owner_str.split('-')]
        return (low + high) / 2
    except:
        return 0

# Proses pembersihan & penambahan fitur
df["Jumlah yang Membeli Game"] = df["owners"].apply(parse_owners)
df["Harga (Rp)"] = df["price"] * 17830 # Conversi ke Rupiah (Data 2 Juni 2026:1 USD = 17830 IDR)

# Rename kolom ke bahasa Indonesia
df_clean = df.rename(columns={
    "name": "Nama Game",
    "median_playtime": "Waktu Bermain",
    "positive_ratings": "Rating Positif",
    "negative_ratings": "Rating Negatif",
    "achievements": "Pencapaian (Achievements)",
    "required_age": "Batas Usia",
    "english": "Mendukung Bahasa Inggris"
})

# Mengambil parameter numerik yang relevan untuk analisis regresi
cols = [
    "Nama Game",
    "Waktu Bermain", 
    "Rating Positif", 
    "Rating Negatif", 
    "Pencapaian (Achievements)", 
    "Harga (Rp)", 
    "Jumlah yang Membeli Game",
    "Batas Usia",
    "Mendukung Bahasa Inggris"
]

# Pastikan semua kolom ada dan hapus data kosong
df_final = df_clean[cols].dropna()

# Simpan ke file baru
output_path = "d:/Araaav/OneDrive - Universitas Tadulako/Documents/VSCode-2026/UAS Stapro/final_data_steam.csv"
df_final.to_csv(output_path, index=False)
print(f"Sukses! Data bersih tersimpan di: {output_path}")