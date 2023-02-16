import pandas as pd
import openpyxl

# pobieranie arkusza spedytora i poprawnie podstawy do obliczenia prowizji jeżeli coś się nie zgadza

def Check(name,procedure):
    x = pd.read_excel("Draft.xlsx", sheet_name="Raport Spedytor - przyklad", skiprows=2)

    podstawa = 0

    for i in range(0, x["Klient"].size - 1):
        if name in x["Klient"][i]:
         podstawa += procedure(x["Prowizja"][i])
        else:
         podstawa += x["Prowizja"][i]




def count_commission():
    stawki = pd.read_excel("Draft.xlsx",sheet_name="Stawki prowizji",index_col = 1)
    y = pd.read_excel("Draft.xlsx",sheet_name="Raport Spedytorzy - przyklad",skiprows=2, index_col = 1)
    table = pd.merge(stawki, y, left_on="ID Spedytora", right_index=True, how="left", sort=False)
    z = table[{"ID Teamu","ID kalkulacji","Prowizja","ID kalkulacji"}].drop_duplicates(keep="first").sort_values(by=['ID Spedytora'])
    print(z)


    teams = z.drop_duplicates("ID Teamu")["ID Teamu"].size

    #tu mozna uzyc mapy
    S = lambda wynik, stawka, potracenia, dodatki: wynik * stawka - potracenia + dodatki
    T1 = lambda wynik, stawka, potracenia, dodatki: wynik * stawka - potracenia + dodatki
    T2 = lambda wynik, stawka, potracenia, dodatki: (wynik * stawka) * 0.82 - potracenia + dodatki
    T3 = lambda wynik, stawka, potracenia, dodatki, koszty: (wynik - koszty) * stawka - potracenia + dodatki
    print(teams)
    for i in range(1, teams):

        for j in range(0, z[z["ID Teamu"] == i]["ID Teamu"].size):

            prow = list(z[z["ID Teamu"] == i]["Prowizja"])[j]
            prog = list(stawki[(stawki.index == z[z["ID Teamu"] == i].index[j])]["Próg PLN"])
            stopa = list(stawki[(stawki.index == z[z["ID Teamu"] == i].index[j])]["Stawka %"])[0]

            if ("S" in list(z[z["ID Teamu"] == i]["ID kalkulacji"])[j]):



                for k in range(1, len(prog)):
                    if (prog[k] - prow) < 0:
                        stopa = list(stawki[(stawki.index == z[z["ID Teamu"] == i].index[j])]["Stawka %"])[k]

                # print(list(z[z["ID Teamu"]==i]["Prowizja"])[j])
                # print(list(stawki[(stawki.index==z[z["ID Teamu"]==i].index[j])]["Próg PLN"]))
                # print(stopa)
                # print(S(list(z[z["ID Teamu"]==i]["Prowizja"])[j],stopa,0,0))
                # print(z[z["ID Teamu"]==i].index[j])


            if ("T" in list(z[z["ID Teamu"] == i]["ID kalkulacji"])[j]):

                prow = z[z["ID Teamu"] == i]["Prowizja"].sum()


                for k in range(1, len(prog)):
                    if (prog[k] - prow) < 0:
                        stopa = list(stawki[(stawki.index == z[z["ID Teamu"] == i].index[j])]["Stawka %"])[k]

               # print("XXXXXXXXXXX")
               # print(stopa)
               # print(z[z["ID Teamu"] == i]["Prowizja"].sum())
               # print(S(z[z["ID Teamu"] == i]["Prowizja"].sum(), stopa, 0, 0))
               # print(z[z["ID Teamu"] == i].index[j])
               # print(z[z["ID Teamu"] == i]["ID Teamu"])

            d = {'ID teamu': [list(z[z["ID Teamu"] == i]["ID Teamu"])[j]],'ID': [z[z["ID Teamu"] == i].index[j]], 'wynik': [S(prow, stopa, 0, 0)] }
            df = pd.DataFrame(data=d)
            print(z[z["ID Teamu"] == i])

            with pd.ExcelWriter("Draft.xlsx", mode="a",engine="openpyxl",if_sheet_exists="overlay") as writer :
                df.to_excel(writer,sheet_name="nowa",startrow=(j+1)*2)

            #print(z[z["ID Teamu"] == i])

