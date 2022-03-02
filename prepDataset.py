import pandas as pd

def load_data(filename):
    df = pd.read_csv(filename, header=0, delimiter=',')
    return df

df_raw = pd.DataFrame()
for idxMonth in range(7,13):
    print('./rawData/JT_SHP_SALES_VARTION_LIST_2021%02d.csv'%idxMonth)
    df_temp = load_data('./rawData/JT_SHP_SALES_VARTION_LIST_2021%02d.csv'%idxMonth)
    df_raw = df_raw.append(df_temp)


df_data = df_raw[['CMPNM_NM', 'SIGNGU_NM', 'ADSTRD_NM', 'AREA_NM', 'MLSFC_NM',
       'SCLAS_NM', 'JJINHBT_SALES_PRICE_RATE', 'OTSD_SALES_PRICE_RATE', 'ALL_SALES_PRICE_RATE' ]]
print(df_data)
exit()

aa = df_data.groupby(['CMPNM_NM'], as_index=False)[['JJINHBT_SALES_PRICE_RATE','OTSD_SALES_PRICE_RATE','ALL_SALES_PRICE_RATE']].mean()

aa["SIGNGU_NM"] = ""
aa["ADSTRD_NM"] = ""
aa["AREA_NM"] = ""
aa["MLSFC_NM"] = ""
aa["SCLAS_NM"] = ""

lists = ["SIGNGU_NM","ADSTRD_NM","AREA_NM","MLSFC_NM","SCLAS_NM"]

for i in range(len(aa)):
    name = aa["CMPNM_NM"].iloc[i]
    print(i, "/", len(aa),"\t",name)
    target = df_data[df_data["CMPNM_NM"] == name]

    for idxList in range(len(lists)):
        fieldName = lists[idxList]
        aa.at[i, fieldName] = target[fieldName].iloc[0]




#aa.to_csv('./data_janToDec2021.csv')
#aa.sort_values(by=["ALL_SALES_PRICE_RATE"], ascending=False).head(100).to_csv('./data_janToDec2021_top100.csv')

aa.to_csv('./data_julyToDec2021.csv')
aa.sort_values(by=["ALL_SALES_PRICE_RATE"], ascending=False).head(100).to_csv('./data_julyToDec2021_top100.csv')
