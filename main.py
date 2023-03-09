from exl import count_commission ,check,choice_path,add
import pandas as pd


if __name__ == '__main__':

    name = choice_path()
    stawki = pd.read_excel(name[0], sheet_name=name[3], index_col=1)
    x = pd.read_excel(name[0], sheet_name=name[2], skiprows=2)
    y = pd.read_excel(name[0], sheet_name=name[1], skiprows=2, index_col=0)
    table = pd.merge(stawki, y, left_on="ID Spedytora", right_index=True, how="left", sort=False)

    try:

        z = pd.read_excel(name[0], sheet_name="potracenia", skiprows=1, index_col=0)


    except ValueError:

        z = table[{"ID Teamu", "ID kalkulacji", "Prowizja", "ID kalkulacji",
                   "Spedytor"}].reset_index().drop_duplicates().reset_index().drop(['index'], axis=1)
        z["potracenia"]=0
        z["dodatki"]=0
        z["koszty"]=0

        with pd.ExcelWriter(name[0], mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
          z.to_excel(writer, sheet_name="potracenia", startrow=1)

        print('\n W pliku ' + name[0] + " został dodany nowy arkusz o nazwie potrącenia, uzupełnij go i uruchom program ponownie \n nacisnij dowolny klawisz \n")
        input()
        exit()

    ids = int(input("wprowadź ID spedytora z klientem specjalnym : "))
    special = input("wprowadź nazwe klienta specjalnego : ")
    print(z[z["ID Spedytora"] == ids]["Spedytor"])
    z.at[list(z[z["ID Spedytora"] == ids].index)[0] , "Prowizja"] = check(x, z, special, lambda a: a * (0.5))
    count_commission(z, stawki)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
