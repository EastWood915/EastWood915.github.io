
import pandas as pd 
import tabula 
from datetime import date, timedelta


def fix_str(item):
    if isinstance(item, str):
        return ' '.join(item.replace('\r', ' ').replace('1)', '').replace('3)', '').split())

def fix_series(series):
    return series.apply(fix_str)

start_date = date.fromisoformat('2020-10-04')

for single_date in (start_date + timedelta(n) for n in range(95)):
    
    today = single_date
    df_data = pd.read_csv('Data/data.csv')
    df_data


    if(today.month >= 10):
        suffix = ''
        zero = ''
    else:
        suffix = '-MPWIS'
        zero = '0'

    link_list = [f"https://wsse.krakow.pl/page/wp-content/uploads/{today.year}/{zero}{today.month}/COVID-19-ogniska-stan-na-{today.day}.{zero}{today.month}.{today.year}-MPWIS.pdf",
            f"https://wsse.krakow.pl/page/wp-content/uploads/{today.year}/{zero}{today.month}/COVID-19-ogniska-stan-na-0{today.day}.{zero}{today.month}.{today.year}-MPWIS.pdf",
            f"https://wsse.krakow.pl/page/wp-content/uploads/{today.year}/{zero}{today.month}/COVID-19-ogniska-stan-na-{today.day}.{zero}{today.month}.{today.year}.pdf",
            f"https://wsse.krakow.pl/page/wp-content/uploads/{today.year}/{zero}{today.month}/COVID-19-ogniska-stan-na-0{today.day}.{zero}{today.month}.{today.year}.pdf",
            f"https://wsse.krakow.pl/page/wp-content/uploads/{today.year}/{zero}{today.month}/COVID-19-ogniska-stan-na-0{today.day}.{zero}{today.month}.{today.year}-.pdf",
            f"https://wsse.krakow.pl/page/wp-content/uploads/{today.year}/{zero}{today.month}/COVID-19-ogniska-stan-na-{today.day}.{zero}{today.month}.{today.year}-MPWIS-1.pdf",
            f"https://wsse.krakow.pl/page/wp-content/uploads/{today.year}/{zero}{today.month}/Covid-19-ogniska-stan-na-{today.day}.{zero}{today.month}.{today.year}.pdf",
            f"https://wsse.krakow.pl/page/wp-content/uploads/{today.year}/{zero}{today.month}/COVID-19-wskaźniki-i-ogniska-stan-na-{today.day}.{zero}{today.month}.{today.year}-MPWIS.pdf",
            f"https://wsse.krakow.pl/page/wp-content/uploads/{today.year}/{zero}{today.month}/COVID-19-ogniska-stan-na-{today.day}.{zero}{today.month}.{today.year}-.pdf",
            f"https://wsse.krakow.pl/page/wp-content/uploads/{today.year}/{zero}{today.month}/COVID-19-ogniska-0{today.day}.{zero}{today.month}.{today.year}.pdf",
            f"https://wsse.krakow.pl/page/wp-content/uploads/{today.year}/{zero}{today.month}/COVID-19-ogniska-stan-na-{today.day}.{zero}{today.month}.{today.year}-MPWIS-.pdf",]

    for link in link_list:
        try:
            df_tab = tabula.read_pdf(link)
        except:
            continue
        break

    try:
        df_tab = pd.DataFrame(df_tab[0])
    except KeyError:
        raise NameError(f"Parse failed on {today}")

    
    if today.month < 9:
        df_tab[df_tab['Unnamed: 0'] == 'Ogółem'] = df_tab[df_tab['Unnamed: 0'] == 'Ogółem'].shift(periods = 1, axis = 1)



    df_tab = df_tab.apply(fix_series, axis=0)


    df_tab.iloc[1,0] = df_tab.iloc[0,0]
    df_tab.iloc[1,1] = df_tab.iloc[0,1]

    df_tab.columns = df_tab.iloc[1]
    df_tab.drop(df_tab.index[1], inplace=True)
    df_tab.drop(df_tab.index[0], inplace=True)
    df_tab[df_tab['Lp.'] == 'Razem Małopolska'] = df_tab[df_tab['Lp.'] == 'Razem Małopolska'].shift(periods = 1, axis = 1)

    try:
        df_tab = df_tab[['Powiat', 'Ogółem', 'Ludność', 'Liczba aktywnych przypadków']]
    except:
        df_tab = df_tab[['Powiat', 'Ogółem', 'Liczba aktywnych przypadków']]
        df_tab['Ludność'] = 779115


    df_Krk = df_tab[df_tab['Powiat'] == 'm. Kraków']
    df_Krk.drop(columns = ['Powiat'], inplace = True)
    df_Krk.columns.name = ''


    df_Krk.loc[:, 'Ogółem'] = [int(str(val).replace(' ','')) for val in df_Krk['Ogółem'].values]
    df_Krk.loc[:, 'Ludność'] = [int(str(val).replace(' ','')) for val in df_Krk['Ludność'].values]
    df_Krk.loc[:, 'Liczba aktywnych przypadków'] = [int(str(val).replace(' ','')) for val in df_Krk.loc[:, 'Liczba aktywnych przypadków'].values]


    df_Krk.loc[:, 'Data'] = today
    df_Krk.loc[:, 'Aktywnych na 10tys mieszkańców'] = (df_Krk['Liczba aktywnych przypadków'] / df_Krk['Ludność']) * 10000
    df_Krk


    if str(today) not in df_data['Data'].values:
        df_data = df_data.append(df_Krk)


    df_data['Liczba nowych przypadków'] = df_data['Ogółem'].diff().astype(int, errors = 'ignore')


    df_data.set_index(df_data['Data'], inplace = True, drop = True)
    df_data.drop(columns = ['Data'], inplace = True)
    df_data.columns.name = None
    df_data

    df_data.to_csv('Data/data.csv')

