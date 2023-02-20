from exl import count_commission ,check,choice_path
import pandas as pd


if __name__ == '__main__':

    name = choice_path()
    stawki = pd.read_excel(name[0], sheet_name=name[3], index_col=1)
    x = pd.read_excel(name[0], sheet_name=name[2], skiprows=2)
    y = pd.read_excel(name[0], sheet_name=name[1], skiprows=2, index_col=0)
    table = pd.merge(stawki, y, left_on="ID Spedytora", right_index=True, how="left", sort=False)
    z = table[{"ID Teamu", "ID kalkulacji", "Prowizja", "ID kalkulacji",
               "Spedytor"}].reset_index().drop_duplicates().reset_index().drop(['index'], axis=1)

    z.at[ 6, "Prowizja"] = check(x,z,"plastik",lambda a: a*(0.5))
    count_commission(z,stawki)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
