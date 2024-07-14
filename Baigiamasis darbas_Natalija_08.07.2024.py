# Sukurti Python programą, kuri:


# !!! Sukurtų duomenų bazę ir atliktų nurodytus veiksmus su ja, pasirinktu duomenų bazės apdorojimo principu, naudojant užklausas (sqlite3), arba Pandas dataframe.

# 1. Sukurtų lentelę Saldainiai su stulpeliais: Pavadinimas, Tipas, Kaina/kg, Perkamas kiekis, Kaina.
# 2. Užpildytu saldainių duomenų bazę duomenimis iš tekstinio failo saldainiai.txt (jei norite galite pasiversti ir į csv). Ps. (Kainą apskaičiuosime ir įtrauksime)
# 3. Užpildykite stulpelį Kaina įtraukdami apskaičiuotas sumos vertes prie atitinkamo saldainio.
# 4. Atspausdintų tik tuos saldainius kurių tipas įvedamas klaviatūra pvz. "Šokoladinis" ir kaina > 5 eur - įvedama klaviatūra.
# 5. Panaikintų input pagalba įvesto saldainio pavadinimo duomenis - ištrintų visą eilutę lentelėje apie tą saldainį.
# 6. Naudodamiesi Seaborn arba Matplotlib Python bibliotekomis, atvaizduokite bent du grafikus (skirtingų tipų - linijinių, stulpelinių, taškinių ar kt. ). Pasitelkite fantaziją ir kūrybą kaip norite ką norite atvaizduokite.  
# Pakaitaliokite grafikų parametrus, pvz. spalvų paletė. Grafikai turi turėti ašių pavadinimus, vertes ant ašių, pavadinimą. Dar gali turėti legendą ar kt. pasirinktą info.

# PASTABA:
# Spausdinkite tarpinius rezultatus kiekvieną eilutę atskirai. Pvz.
# "Miglė", "Šokoladinis", 6, 2
# "Vilnius", "Šokoladinis", 7, 1

import sqlite3
from csv import reader
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

with open('./Baigiamasis darbas/saldainiai.csv', encoding='utf8') as failas:
  csv_reader = reader(failas)
  saldainiai = list(csv_reader)
print(saldainiai)

# for saldainis in saldainiai:
#    kaina = int(saldainis[2]) * int(saldainis[3])
#    saldainis.append(kaina)

# conn = sqlite3.connect("duomenu_baze.db")
# c = conn.cursor()

# c.execute("""CREATE TABLE IF NOT EXISTS saldainiai (
#             Pavadinimas text,
#             Tipas text,
#             Kaina_už_kg integer,
#             Perkamas_kiekis integer,
#             Kaina integer
#             )""")    
# c.executemany('INSERT OR REPLACE INTO saldainiai (Pavadinimas, Tipas, Kaina_už_kg, Perkamas_kiekis, Kaina) VALUES (?, ?, ?, ?, ?)', saldainiai)
# conn.commit()

# c.execute("SELECT * FROM saldainiai") # tarpiniai spausdinimai
# duomenys = c.fetchall()
# print(duomenys)
# for eilute in duomenys:
#    print(eilute)

from sqlalchemy import create_engine

engine = create_engine('sqlite:///duomenu_baze.db') # duomenu baze turi egzistuoti kaip failas ir buti uzpildytais duomenimis
df = pd.read_sql_table("saldainiai", engine)

print(df)
print(df.loc[df['Kaina_už_kg'] > 5])
tipas = input(f'Įveskite saldainių tipą: ')
kaina_kg = int(input('Įveskite skaičių 5: '))
while tipas not in list(df['Tipas']):
    print('Klaidingai įvedėte saldainių tipą! - KARTOKITE!')
    tipas = input(f'Įveskite saldainių tipą: ')
while kaina_kg != 5:
    print('Klaidingai įvedėte skaičių! - KARTOKITE!')
    kaina_kg = int(input(f'Įveskite skaičių 5: '))
if tipas in list(df['Tipas']):
    ats = df.loc[(df['Tipas'].str.contains(tipas)) & (df['Kaina_už_kg'] > kaina_kg)]
    print(ats)

istrinti = input('Kurį įrašą ištrinti? (Nurodykite saldainio pavadinimą): ')
eilutes_trinimui = df[df['Pavadinimas'] == istrinti]
print(eilutes_trinimui) # paziureti ka randa
if eilutes_trinimui.empty:
    print('Pagal pasirinktą saldainio pavadinimą duomenų nėra')
else:
    df = df.drop(eilutes_trinimui.index)
print('------------------------')
print(df)
print(len(df.Tipas))

sns.set_style('white')
df1 = df.sort_values('Tipas')
grafikas = sns.barplot(x='Tipas', y='Kaina', data=df1, hue = 'Tipas', estimator=sum, palette = 'plasma', legend = False, errorbar = None)
for container in grafikas.containers:
    grafikas.bar_label(container)
grafikas.set(title = 'Pardavimai pagal tipą', xlabel = 'Saldainių tipas', ylabel = 'Kaina, eur')
df.sort_values('Tipas')
sns.despine()
plt.xticks(rotation=90)
plt.show()

sns.set_style('white')
df2 = df.sort_values('Pavadinimas')
grafikas = sns.barplot(x='Perkamas_kiekis', y='Pavadinimas', data=df.loc[df['Tipas'].str.contains('Šokoladinis')], hue = 'Pavadinimas', palette = 'viridis', legend = False, errorbar = None)
for container in grafikas.containers:
    grafikas.bar_label(container)
grafikas.set(title = 'Perkami kiekiai šokoladinių saldainių', xlabel = 'Perkamas kiekis')
sns.despine()
plt.show()

sns.set_style('dark')
df_unikalus = df.groupby(['Pavadinimas', 'Tipas']).mean().reset_index()
grafikas = sns.scatterplot(x='Kaina_už_kg', y='Perkamas_kiekis', data=df_unikalus, hue = 'Pavadinimas', palette = 'plasma', legend = False)
sns.despine()
grafikas.set(title = 'Perkamas kiekis vs kaina už kg', xlabel = 'Kaina už kg, eur', ylabel ='Perkamas kiekis')
plt.show()