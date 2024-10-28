import pandas as pd

paths = ["Aalto yliopisto", "Helsingin yliopisto", "Turun yliopisto", "Oulun yliopisto", "Itä-Suomen yliopisto", 
         "Lapin yliopisto", "Tampereen yliopisto", "Åbo akademi", "Jyväskylän yliopisto", "Vaasan yliopisto", 
         "Lappeenrannan-Lahden teknillinen yliopisto LUT", "Svenska handelshögskolan"]
final_data = pd.DataFrame()

for reitti in paths:
    path1 = f"C:/Users/tinka/Documents/OPISKELU/IDS (introduction to data science)/IDS PROJECT/Yliopistot pisterajat csv/{reitti} csv.csv"
    data1 = pd.read_csv(path1, encoding='UTF-8', header=1)
    data1.reset_index(drop=True)

    vuosi1 = 2014
    yliopisto = reitti

    # DATA 1 
    for i in range(2,len(data1)): 

        if data1.iloc[i, 1]=='2015':
             continue

        if pd.isna(data1.iloc[i, 1]):
            vuosi1+=1
            continue

        rivi = data1.iloc[i].to_frame(name="Välitilasto")
        rivi_tyhjennetty = rivi[rivi["Välitilasto"] != "0"]

        for rivi in range(len(rivi_tyhjennetty)): 

                if rivi%2:
                    # tää 2014 vaan hakutapa vuosilukuna
                    hakutapa = rivi_tyhjennetty.iloc[0,0]
                    ala = rivi_tyhjennetty.index[rivi]
                    alinpistemaara = rivi_tyhjennetty.iloc[rivi][0]
                    ylinpistemaara = rivi_tyhjennetty.iloc[rivi+1][0]


                    # luodaan rivi alimmalle
                    new_data = pd.DataFrame({
                            'Yliopisto': [yliopisto],
                            'Vuosi': [vuosi1],
                            'Ala': [ala],
                            'Hakutapa': [hakutapa],
                            'Alin pistemäärä': [alinpistemaara],
                            'Ylin pistemäärä': [ylinpistemaara]
                            })
                    
                    # lisätään rivi dataan
                    final_data = pd.concat([final_data, new_data], ignore_index=True)


years_to_remove = ['2014', '2015', '2016']
indices_to_drop = final_data[final_data['Hakutapa'].isin(years_to_remove)].index
final_data = final_data.drop(indices_to_drop)


final_data['Aloituspaikat'] = 0
final_data['Ensisijaiset hakijat'] = 0
final_data['Kaikki hakijat'] = 0
final_data['Valitut'] = 0
final_data['Paikan vastaanottaneet'] = 0

# DATA 2 
for reitti in paths: 
    path2 = f"C:/Users/tinka/Documents/OPISKELU/IDS (introduction to data science)/IDS PROJECT/Yliopistot hakijat csv/{reitti} csv.csv"
    data2 = pd.read_csv(path2, encoding='UTF-8', sep=";", header=1)
    data2.drop(['Yhteensä Aloituspaikat', 'Yhteensä Ensisijaiset hakijat', 'Yhteensä Kaikki hakijat', 'Yhteensä Valitut', 'Yhteensä Paikan vastaanottaneet'], axis=1, inplace=True)
    data2.reset_index(drop=True)
    data2.drop([1], inplace=True)

    vuosi2 = 2021
    yliopisto = reitti

    for i in range(1,data2.shape[0]): 

        mm = data2.iloc[i, 0]
        if vuosi2==2025:
            break
        
        if mm=='2021' or mm=='2022' or mm=='2023' or mm=='2024' or mm=='2025':
            ala = ""
            for j in range(1,data2.shape[1]):
                        nn=data2.iloc[i,j]

                        if nn=='1-4':
                            nn=4

                        if j%5==1:
                            ala = data2.columns[j]

                        z = ''
                        if not pd.isna(nn): 
                            if j%5==0:
                                z = 'Paikan vastaanottaneet'
                            if j%5==1:
                                z = 'Aloituspaikat'
                            if j%5==2:
                                z = 'Ensisijaiset hakijat'
                            if j%5==3:
                                z = 'Kaikki hakijat'
                            if j%5==4:
                                z = 'Valitut'
                            # löytyi numeroarvo, sijoitetaan se taulukkoon
                            try: 
                                final_data.loc[final_data['Ala'] == ala, z] = nn
                            except:
                                # ei oteta ollenkaan mukaan niitä aloja, joista ei jo löydy pisterajatietoo
                                pass                 

json_path = f"C:/Users/tinka/Documents/Opiskelu/IDS (introduction to data science)/IDS PROJECT/Yliopistot pisterajat json/Valmis data 2 json.json"
final_data.to_json(json_path, orient='records', lines=True, force_ascii=False)
