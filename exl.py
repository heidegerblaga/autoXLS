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




def count_commission(z,stawki):


    teams = z.drop_duplicates("ID Teamu")["ID Teamu"].size

    S = lambda wynik, stawka, potracenia, dodatki: wynik * stawka - potracenia + dodatki
    T1 = lambda wynik, stawka, potracenia, dodatki: wynik * stawka - potracenia + dodatki
    T2 = lambda wynik, stawka, potracenia, dodatki: (wynik * stawka) * 0.82 - potracenia + dodatki
    T3 = lambda wynik, stawka, potracenia, dodatki, koszty: (wynik - koszty) * stawka - potracenia + dodatki
    p=1
    for i in range(1, teams+1):


        for j in range(0, z[z["ID Teamu"] == i]["ID Teamu"].size):
            prow = list(z[z["ID Teamu"] == i]["Prowizja"])[j]
            prog = list(stawki[stawki.index == list(z[z["ID Teamu"] == i]["ID Spedytora"])[j]]["Próg PLN"])
            print(stawki[stawki.index == list(z[z["ID Teamu"] == i]["ID Spedytora"])[j]]["Próg PLN"])
            wyplata = 0
            stopa = 0

            if ("S" in list(z[z["ID Teamu"] == i]["ID kalkulacji"])[j]):
                for k in range(0, len(prog)):

                    if (prog[k] - prow) < 0:

                        stopa = list(stawki[stawki.index == list(z[z["ID Teamu"] == i]["ID Spedytora"])[j]]["Stawka %"])[k]


                wyplata = S(prow, stopa, 0, 0)


            if ("T" in list(z[z["ID Teamu"] == i]["ID kalkulacji"])[j]):

                prow = z[z["ID Teamu"] == i]["Prowizja"].sum()

                print(list(z[z["ID Teamu"] == i]["ID Spedytora"])[j])
                for k in range(0, len(prog)):

                    if (prog[k] - prow) < 0:

                        stopa = list(stawki[stawki.index == list(z[z["ID Teamu"] == i]["ID Spedytora"])[j]]["Stawka %"])[k]
                        print(stopa)
                        print("*****")

                if ("T1" in list(z[z["ID Teamu"] == i]["ID kalkulacji"])[j]):
                    wyplata = T1(prow, stopa, 0, 0)
                if ("T2" in list(z[z["ID Teamu"] == i]["ID kalkulacji"])[j]):
                    wyplata = T2(prow, stopa, 0, 0)
                if ("T3" in list(z[z["ID Teamu"] == i]["ID kalkulacji"])[j]):
                    wyplata = T3(prow, stopa, 0, 0,0)

            d = {'ID teamu': [list(z[z["ID Teamu"] == i]["ID Teamu"])[j]],'ID': [list(z[z["ID Teamu"] == i]["ID Spedytora"])[j]],'id kalkulacji': [list(z[z["ID Teamu"] == i]["ID kalkulacji"])[j]],'procent': stopa ,'wynik': prow, 'wyplata': [wyplata]}
            df = pd.DataFrame(data=d).set_index('ID')



            with pd.ExcelWriter("Draft.xlsx", mode="a",engine="openpyxl",if_sheet_exists="overlay") as writer :
                df.to_excel(writer,sheet_name="wyplaty",startrow=(p))
                p+=2

            #print(z[z["ID Teamu"] == i])

