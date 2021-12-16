"""
Aplikasi untuk menggambarkan statistik produksi minyak di berbagai Negara

Dibuat dengan tujuan memenuhi kriteria penilaian UAS Prokom 
##Semoga hasilnya bisa memuaskan##
"""

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import json as js
from matplotlib import cm
import streamlit as st
from PIL import Image

#>>>>>>>>>>>> title <<<<<<<<<<<<#
st.set_page_config(layout="wide")  # this needs to be the first Streamlit command called
st.title("Statistik Produksi Minyak Berbagai Negara")
st.image('Oil industry.jpg')
#>>>>>>>>>>>> title <<<<<<<<<<<<#

#>>>>>>>>>>>> sidebar <<<<<<<<<<<<#
gambar = Image.open('Logo_oil.jpg')
st.sidebar.image(gambar)
col_1 , col_2 = st.columns(2)

st.sidebar.title("Pengaturan")
st.sidebar.subheader("Pengaturan konfigurasi tampilan")

#Input Data
with open("kode_negara_lengkap.json") as f:
    kode_negara = js.load(f)
df = pd.read_csv("produksi_minyak_mentah.csv", decimal='.')

#Mensortir kode negara yang unik
kode_unik = list(df['kode_negara'].unique())

#Mensortir tahun unik
tahun_unik = list(df['tahun'].unique())

#Mengambil nama lengkap negara dari file json
Nama_negara = []
kode_negara_fix = []
for i in range(len(kode_unik)):
    for code in kode_negara:
        if kode_unik[i] == code["alpha-3"] :
            kode_negara_fix.append(kode_unik[i])
            Nama_negara.append(code['name'])
    i = i + 1       

#Menghapus data organisasi pada file csv
list_organisasi = []
for i in range (len(df)) :
    if df['kode_negara'].iloc[i] not in kode_negara_fix :
        list_organisasi.append(df['kode_negara'].iloc[i])

for i in list_organisasi :
    df = df[df.kode_negara != i]
df['tahun'] = df['tahun'].astype(str)

#Input User 
Negara = st.sidebar.selectbox("Pilih Negara", Nama_negara)
B_terbesar = st.sidebar.number_input("Input jumlah N Negara Terbesar (max = 137)", min_value=1, max_value=137, value=10)
Thn = st.sidebar.selectbox("Pilih Tahun", tahun_unik)
Tahun = str(Thn)
#>>>>>>>>>>>> sidebar <<<<<<<<<<<<#

#>>>>>>>>>>>> Left Column upper <<<<<<<<<<<<#
col_1.subheader("Grafik Produksi Minyak Mentah")
#Mengkonversi nama lengkap menjadi kode negara
for code in kode_negara:
    if Negara == code["name"] :
        kode = code["alpha-3"]

#Memasukkan list tahun dan produksi sesuai negara yang dipilih
list_tahun = []
list_produksi = []
for i in range (len(df)) :
    if df['kode_negara'].iloc[i] == kode :
        list_tahun.append(df['tahun'].iloc[i])
        list_produksi.append(df['produksi'].iloc[i])

cmap_name = 'tab20'
cmap = cm.get_cmap(cmap_name)
colors = cmap.colors[:len(list_tahun)]
Tahun_1 = np.arange(len(list_tahun))
fig, ax = plt.subplots(figsize = (15,8))
ax.bar(Tahun_1, list_produksi, color=colors,)
ax.set_title("Total Produksi per Tahun Negara {}".format(Negara), fontsize=25)
ax.set_ylabel("TotalProduksi", fontsize=20)
ax.set_xlabel("Tahun", fontsize = 20)
ax.set_xticklabels(list_tahun)
plt.xticks(Tahun_1, list_tahun, rotation= 45)
plt.tight_layout()

col_1.pyplot(fig)
#>>>>>>>>>>>> Left Column upper <<<<<<<<<<<<#

#>>>>>>>>>>>> Right Column upper <<<<<<<<<<<<#
col_2.subheader("Grafik Produksi Terbesar")

list_kode_negara = []
list_produksi_2 = []

for i in range (len(df)) :
    if df['tahun'].iloc[i] == Tahun :
        list_kode_negara.append(df['kode_negara'].iloc[i])
        list_produksi_2.append(df['produksi'].iloc[i])

list_negara = [] 
for i in range(len(list_kode_negara)):
    for code in kode_negara:
        if list_kode_negara[i] == code["alpha-3"] :
            list_negara.append(code['name'])

data_negara_produksi = pd.DataFrame({'Negara':list_negara,'Produksi' : list_produksi_2 })
data_negara_produksi.sort_values(by = ['Produksi'],inplace=True,ascending=False)

fig, ax = plt.subplots(figsize = (15,8))
ax.barh(data_negara_produksi['Negara'].head(B_terbesar), data_negara_produksi['Produksi'].head(B_terbesar), color=colors)
ax.set_title("Grafik {} Negara dengan Jumlah Produksi Terbesar ({})".format(B_terbesar,Tahun), fontsize=25)
ax.set_ylabel("Negara", fontsize=20)
ax.set_xlabel("Total Produksi", fontsize = 20)
plt.tight_layout()

col_2.pyplot(fig)
#>>>>>>>>>>>> Right Column upper <<<<<<<<<<<<#

#>>>>>>>>>>>> Mid Column <<<<<<<<<<<<#
st.subheader("Grafik Jumlah Produksi Kumulatif")
Total_produksi = []
for kode in kode_negara_fix:
    Total_produksi.append(df[df['kode_negara'] == kode]['produksi'].sum())

data_produksi_kumulatif = pd.DataFrame({'Negara':Nama_negara,'Produksi' : Total_produksi })
data_produksi_kumulatif.sort_values(by = ['Produksi'],inplace=True,ascending=False)

fig, ax = plt.subplots(figsize = (15,8))
ax.barh(data_produksi_kumulatif['Negara'].head(B_terbesar), data_produksi_kumulatif['Produksi'].head(B_terbesar), color=colors)
ax.set_title("Grafik {} Negara dengan Jumlah Produksi Kumulatif Terbesar".format(B_terbesar), fontsize=30)
ax.set_ylabel("Negara", fontsize=23)
ax.set_xlabel("Total Produksi", fontsize = 23)
plt.tight_layout()
st.pyplot(fig)
#>>>>>>>>>>>> Mid Column <<<<<<<<<<<<#

#>>>>>>>>>>>> Mid Column 4 <<<<<<<<<<<<#
st.subheader("Summary")

#Data negara jumlah produksi terbesar pada tahun T
Nama_lengkap_negara = str(data_negara_produksi['Negara'].iloc[0])
for code in kode_negara:
    if Nama_lengkap_negara == code["name"] :
        code_negara = code['country-code']
        region = code['region']
        sub_region = code['sub-region']
Jumlah_produksi = data_negara_produksi['Produksi'].iloc[0]
st.markdown(f"**Negara dengan jumlah produksi terbesar pada tahun {str(Tahun)}: **")
st.text(f"Nama Negara    : {Nama_lengkap_negara}")
st.text(f"Kode Negara    : {code_negara}")
st.text(f"Region         : {region}")
st.text(f"Sub Region     : {sub_region}")
st.text(f"Total Produksi : {Jumlah_produksi}")

#Data negara jumlah produksi terbesar kumulatif
nm_negara = str(data_produksi_kumulatif['Negara'].iloc[0])
for code in kode_negara:
    if nm_negara == code["name"] :
        code_ngr = code['country-code']
        reg = code['region']
        sub_reg = code['sub-region']
Jumlah_prdks = data_produksi_kumulatif['Produksi'].iloc[0]
st.markdown(f"**Negara dengan jumlah produksi kumulatif terbesar : **")
st.text(f"Nama Negara    : {nm_negara}")
st.text(f"Kode Negara    : {code_ngr}")
st.text(f"Region         : {reg}")
st.text(f"Sub Region     : {sub_reg}")
st.text(f"Total Produksi : {Jumlah_prdks}")

#Data negara jumlah produksi terkecil pada tahun T
prdksi_trkcl = None
for i in range (len(data_negara_produksi)) :
    if prdksi_trkcl == None :
        prdksi_trkcl = data_negara_produksi['Produksi'].iloc[i]
    elif data_negara_produksi['Produksi'].iloc[i] != 0 :
        if data_negara_produksi['Produksi'].iloc[i] < prdksi_trkcl :
            prdksi_trkcl = data_negara_produksi['Produksi'].iloc[i]
            nmlngkp_negara = data_negara_produksi['Negara'].iloc[i]
for code in kode_negara:
    if nmlngkp_negara == code["name"] :
        cod_ngr = code['country-code']
        regi = code['region']
        sub_regi = code['sub-region']
st.markdown(f"**Negara dengan jumlah produksi terkecil pada tahun {str(Tahun)} : **")
st.text(f"Nama Negara    : {nmlngkp_negara}")
st.text(f"Kode Negara    : {cod_ngr}")
st.text(f"Region         : {regi}")
st.text(f"Sub Region     : {sub_regi}")
st.text(f"Total Produksi : {prdksi_trkcl}")

#Data negara jumlah produksi terkecil kumulatif
prediksi = None
for i in range (len(data_produksi_kumulatif)) :
    if prediksi == None :
        prediksi = data_produksi_kumulatif['Produksi'].iloc[i]
    elif data_produksi_kumulatif['Produksi'].iloc[i] != 0 :
        if data_produksi_kumulatif['Produksi'].iloc[i] < prediksi :
            prediksi = data_produksi_kumulatif['Produksi'].iloc[i]
            nmlngkp_ngr = data_produksi_kumulatif['Negara'].iloc[i]
for code in kode_negara:
    if nmlngkp_ngr == code["name"] :
        cod = code['country-code']
        reg_ = code['region']
        sub_re = code['sub-region']
st.markdown(f"**Negara dengan jumlah produksi terkecil kumulatif : **")
st.text(f"Nama Negara    : {nmlngkp_ngr}")
st.text(f"Kode Negara    : {cod}")
st.text(f"Region         : {reg_}")
st.text(f"Sub Region     : {sub_re}")
st.text(f"Total Produksi : {prediksi}")

#Data negara jumlah produksi sama dengan nol pada tahun T
lst_nm_ngr = []
for i in range (len(data_negara_produksi)) :
    if data_negara_produksi['Produksi'].iloc[i] == 0 :
        lst_nm_ngr.append(data_negara_produksi['Negara'].iloc[i])
lst_code_ngr = []
lst_region = []
lst_sub_region = []
for i in range (len(lst_nm_ngr)):
    for code in kode_negara:
        if lst_nm_ngr[i] == code["name"] :
            lst_code_ngr.append(code['country-code'])
            lst_region.append(code['region'])
            lst_sub_region.append(code['sub-region'])

jmlproduksi0 = pd.DataFrame {"Negara": lst_code_ngr , "Kode Negara" : lst_code_ngr, "Region" : lst_region , "Sub Region" : lst_sub_region}
st.markdown(f"**Negara dengan jumlah produksi 0 pada tahun {str(Tahun)} : **")
st.text ("")
st.dataframe (jmlproduksi0)

#Data negara jumlah produksi sama dengan nol data kumulatif
list_nm_ngr = []
for i in range (len(data_produksi_kumulatif)) :
    if data_produksi_kumulatif['Produksi'].iloc[i] == 0 :
        list_nm_ngr.append(data_produksi_kumulatif['Negara'].iloc[i])
list_code_ngr = []
list_region = []
list_sub_region = []
for i in range (len(list_nm_ngr)):
    for code in kode_negara:
        if list_nm_ngr[i] == code["name"] :
            list_code_ngr.append(code['country-code'])
            list_region.append(code['region'])
            list_sub_region.append(code['sub-region'])

jmlproduksikum = pd.DataFrame {"Negara": list_code_ngr , "Kode Negara" : list_code_ngr, "Region" : list_region , "Sub Region" : list_sub_region}
st.markdown(f"**Negara dengan jumlah produksi kumulatif = 0 :**")
st.text ("")
st.dataframe (jmlproduksikum)
#>>>>>>>>>>>> Mid Column 4 <<<<<<<<<<<<#
