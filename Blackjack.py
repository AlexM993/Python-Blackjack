import random


# citirea listei de participanti
def participanti():
    listaJucatori = []
    with open('ListaParticipanți.txt', 'r') as f:
        line = f.read()
        line = line.split('\n')
        jucatori = [x.split() for x in line]

    for jucator in jucatori:
        jucator = Jucator(jucator[0], jucator[1], jucator[2], jucator[3], int(jucator[4]))
        listaJucatori.append(jucator)
    return listaJucatori


# clasa Carte, pentru a crea o carte de joc (valoarea + tipul cartii)
class Carte():
    """
        Carte = valoarea + tipul cartii
    """

    def __init__(self, valoare, tip):
        self.valoare = valoare
        self.tip = tip

    def arataCarte(self):
        if self.valoare == 1: self.valoare = "A"
        if self.valoare == 11: self.valoare = "J"
        if self.valoare == 12: self.valoare = "Q"
        if self.valoare == 13: self.valoare = "K"
        return "{} de {}".format(self.valoare, self.tip)

#clasa de creare a pachetului
class Pachet():
    def __init__(self):
        self.listaCarti = []
        self.pachetFull()

    # metoda pentru construirea si afisarea pachetului, cu ajutorul clasei Carte
    def pachetFull(self):
        for t in ["Inima", "Romb", "Trefla", "Pica"]:
            for n in range(1, 14):
                self.listaCarti.append(Carte(n, t))

    # metoda pentru afisarea pachetului
    def arataPachet(self):
        for c in self.listaCarti:
            c.arataCarte()

    # metoda pentru amestecare
    def shufflePachet(self):
        for i in range(len(self.listaCarti)):
            r = random.randint(0, i)
            self.listaCarti[i], self.listaCarti[r] = self.listaCarti[r], self.listaCarti[i]

    #metoda pentru a trage o carte
    def trageCarte(self):
        return self.listaCarti.pop()

#clasa care tine evidenta scorului final si a punctajului (ia in considerare si cazurile in care AS = 10, sau AS = 1)
class Blackjack():
    def __init__(self):
        self.mana = []
        self.manaDealer = []

    def score(self, mana, manaDealer):
        manaJucator = self.punctaj(mana)
        manaD = self.punctaj(manaDealer)
        print("Mana Dealer:  {}".format(manaD))
        print("Mana Jucator:  {}".format(manaJucator))
        rc = 0
        if manaJucator == 21:
            print("Felicitari! Ai facut Blackjack!")
        elif manaD == 21:
            print("Ai pierdut. Dealer-ul are blackjack.")
            rc = 1
        elif manaJucator > 21:
            print("Ai pierdut. Ai peste 21.")
            rc = 1
        elif manaD > 21:
            print("Felicitari! Ai castigat! Dealer-ul are peste 21.")
        elif manaJucator < manaD:
            print("Ai pierdut. Scorul tau este mai mic decat al dealer-ului.")
            rc = 1
        elif manaJucator > manaD:
            print("Felicitari!. Ai castigat! Scorul tau este mai mare decat al dealer-ului.")
        return rc

    # punctajul in functie de valoarea As-ului
    def punctaj(self, mana):
        total = 0
        total2 = 0

        for i in mana:
            if i.valoare == "J" or i.valoare == "Q" or i.valoare == "K":  # J Q K
                total += 10
                total2 += 10
            elif i.valoare == 'A':
                total += 11
                total2 += 1
            else:
                total += int(i.valoare)
                total2 += int(i.valoare)

        if total2 > 21:
            return total
        else:
            return total2


#clasa Jucator
class Jucator():
    def __init__(self, nume, prenume, varsta, nationalitate, jetoane=0):
        self.nume = nume
        self.prenume = prenume
        self.varsta = varsta
        self.nationalitate = nationalitate
        self.jetoane = jetoane
        self.jetoanePariate = 0
        self.mana = []

        # self.manaDealer = []

    # trage, sau Hit
    def trage(self, pachet):
        self.mana.append(pachet.trageCarte())

    #arata cartile din mana jucatorului
    def arataMana(self):
        x = []
        for carte in self.mana:
            x.append(carte.arataCarte())
        return x

    #metoda de adaugare a pariurilor / verifica validitatea lui in
    #functie de numarul de jetoane dispoinibile in functie de fiecare jucator
    def adaugaPariu(self):
        while True:
            try:
                x = int(input("{} care e suma pariata? (max {}): ".format(self.nume, self.jetoane)))
            except ValueError or TypeError:
                print("Valoare introdusa nu este valida. Mai incearca")
                continue
            else:
                break

        if 1 < x <= self.jetoane:
            print("Pariu acceptat")
            self.jetoanePariate += x
            self.jetoane -= x
        else:
            print("Pariul nu este acceptat. Mai sunt " + str(self.jetoane) + " ramase")
            self.adaugaPariu()

#functia prin care ruleaza tot flow-ul unei partide
def game():
    joc = Blackjack()
    listaJucatori = []
    listaJucatori = participanti()
    dealer = Jucator("Dealer", "Dealer", 10, "USA")
    pachet = Pachet()
    pachet.shufflePachet()
    # print(pachet.arataPachet())
    rc = 0

    for jucator in listaJucatori:
        print("Jucator:" + jucator.nume + " " + jucator.prenume)
        jucator.adaugaPariu()

    # dealerul primeste o carte
    dealer.trage(pachet)

    # fiecare jucator primeste 2 carti
    for i in range(len(listaJucatori)):
        print("\n")
        listaJucatori[i].trage(pachet)
        listaJucatori[i].trage(pachet)

        print("Dealer-ul are: {}".format(dealer.arataMana()) + "\nTotal: " + str(joc.punctaj(dealer.mana)) + "\n")

        punctaj = joc.punctaj(listaJucatori[i].mana)
        print("{} are: ".format(listaJucatori[i].nume) + "{}".format(listaJucatori[i].arataMana()))
        print("{} are scor total: ".format(listaJucatori[i].nume) + str(punctaj))

        while punctaj < 21:
            intrebare = input("Tragi o carte? Y/N").lower()
            nu = ("n", "no", "nu")
            da = ("y", "yes", "da")

            if intrebare in nu:
                break
            elif intrebare in da:
                listaJucatori[i].trage(pachet)
                print("{} are: ".format(listaJucatori[i].nume) + "{}".format(listaJucatori[i].arataMana()))
            else:
                print("Raspuns invalid. Mai incearca.")
            punctaj = joc.punctaj(listaJucatori[i].mana)
            print("{} areee: ".format(listaJucatori[i].nume) + str(punctaj))

    print("\n")
    punctajDealer = joc.punctaj(dealer.mana)
    while True:
        if punctajDealer >= 17:
            break
        else:
            dealer.trage(pachet)
            print("Dealer-ul are {} ".format(dealer.arataMana()))
        punctajDealer = joc.punctaj(dealer.mana)
        print("Dealer-ul mai trage o carte. \nDealer-ul are scor final", str(punctajDealer))
    print("\n")

    for i in range(len(listaJucatori)):
        punctaj = joc.punctaj(listaJucatori[i].mana)
        print("\nJucator {}: ".format(listaJucatori[i].nume))
        rc = joc.score(listaJucatori[i].mana, dealer.mana)

        if rc == 0:
            listaJucatori[i].jetoane += listaJucatori[i].jetoanePariate * 2
        print("Jucator {} mai are: ".format(listaJucatori[i].nume) + str(listaJucatori[i].jetoane))


if __name__ == '__main__':
    game()

    while True:
        question = input("Mai joci? Y/N").lower()
        nu = ("n", "no", "nu")
        da = ("y", "yes", "da")

        if question in nu:
            print("Game over!")
            break
        elif question in da:
                game()
        else:
            print("Raspuns invalid. Mai incearca!")