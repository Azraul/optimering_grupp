"""
# Orginal function
## https://stackoverflow.com/a/54153818

Vi använde en pmx function från stackoverflow och satte våra huvuden ihop
för att på bästa sätt förklara den så att så många som möjligt skulle förstå hur
det faktiskt fungerar

Johan & Kristoffer

"""

import numpy as np

# skriv in föräldrarna, tagna från lektionen
parent1 = None
parent2 = None

# skapa skärningspunkter per lektion
#
#          3            7
# [1,2,3,  |  4,5,6,7,  |  8,9]

firstCrossPoint = None
secondCrossPoint = None

# ta ut delarna som används
parent1MiddleCross = None
parent2MiddleCross = None
# parent1MiddleCross:  [4, 5, 6, 7]
# parent2MiddleCross:  [8, 2, 6, 5]


# gör temporära barn, de är temporära eftersom de har en möjlighet för dubbletter
# något vi måste fixa, som att ha 2st 2: or (eller 2st 8: or)
#
# temp_child1:  [1, 2, 3, 8, 2, 6, 5, 8, 9] 
#                   ^        ^
#
# temp_child2:  [9, 3, 7, 4, 5, 6, 7, 1, 4]


# kolla vilka relationer varje siffra har i mitt delarna
# detta används för att fixa dubbletter senare, VIKTIGA!
relations = []


# print(relations)
# [[8, 4], [2, 5], [6, 6], [5, 7]]


# recursion1 och 2 skiljer sig endast i ordningen för relationer mellan föräldrarna (p1 -> p2 vs p2 -> p1)
# ** vi ser på relation[0] när barn1 skapas
def recursion1 (temp_child , firstCrossPoint , secondCrossPoint , parent1MiddleCross , parent2MiddleCross) :
    child = np.array([0 for i in range(len(parent1))]) # tomt barn
    # kolla om de första siffrorna finns i mitten redan, i så fall prova byt siffran mote den relaterade siffran
    # p1 [1,2,3]
    # 1 finns inte i crosssection [8,2,6,5]
    # men 2 finns! Vad är p1 relationen 2 i p2?
    # [2,5], okej 5, vi provar det!, nu har vi alltså [1,5,3]
    # nu kan vi gå till 3 som inte finns i vår cross-section
    # den observanta ser att vi har 5:or på 2 ställen nu
    # vi kommer tillbaka hit senare i function och gör samma sak som med siffran 2
    # d.v.s. relationen [5,7], vi sätter en 7:a istället för 5:an
    # alltså kommer vi sluta vid [1,7,3] innan första cross point
    for i,j in enumerate(temp_child[:firstCrossPoint]): 
        c=0
        for x in relations:
            if j == x[0]: # **
                child[i]=x[1]
                c=1
                break
        if c==0:
            child[i]=j
    
    j=0 # återanvändning av variable

    # Nu sätter vi in crosssection i vårt barn
    # parent2middlecross - [8,2,6,5]
    # child[3] = parent2middlecross[0]
    # child[4] = parent2middlecross[1]
    # osv...
    for i in range(firstCrossPoint,secondCrossPoint):
        child[i]=parent2MiddleCross[j]
        j+=1

    # Nu gör vi samma som förut, men på de sista siffrorna
    # alltså om p1 [8,9] finns i crosssection [8,2,6,5]
    # så kollar vi relationen och provar byta, precis som tidigare
    for i,j in enumerate(temp_child[secondCrossPoint:]):
        c=0
        for x in relations:
            if j == x[0]: # **
                child[i+secondCrossPoint]=x[1] #+secondcross eftersom i räknar från 0 och vi är ju någonstanns mitt i arrayen
                c=1
                break
        if c==0:
            child[i+secondCrossPoint]=j

    # som nämndes tidigare byts en relation endast 1 gång, denna logic kollar att den nya relationen
    # inte skapade en ny dubblet, genom att ta alla unique values och kolla att de mindre än barnet i längde
    # i.e barn [1,2,2], unique [1,2] - barnet är längre än unique, alltså måste vi köra om functionen och prova byta fler relationer
    child_unique=np.unique(child)
    #print(child)
    if len(child)>len(child_unique):
        child=recursion1(child,firstCrossPoint,secondCrossPoint,parent1MiddleCross,parent2MiddleCross)
    return(child)

# precis samma funktion som ovan, men looparna är omvända så vi kollar p2 relation till p1
# ** vi ser på relation[1] isället för relation[0] när barn2 skapas
def recursion2(temp_child,firstCrossPoint,secondCrossPoint,parent1MiddleCross,parent2MiddleCross):
    child = np.array([0 for i in range(len(parent1))])
    for i,j in enumerate(temp_child[:firstCrossPoint]):
        c=0
        for x in relations:
            if j == x[1]: # **
                child[i]=x[0]
                c=1
                break
        if c==0:
            child[i]=j
    j=0
    for i in range(firstCrossPoint,secondCrossPoint):
        child[i]=parent1MiddleCross[j]
        j+=1

    for i,j in enumerate(temp_child[secondCrossPoint:]):
        c=0
        for x in relations:
            if j == x[1]: # **
                child[i+secondCrossPoint]=x[0]
                c=1
                break
        if c==0:
            child[i+secondCrossPoint]=j
    child_unique=np.unique(child)
    if len(child)>len(child_unique):
        child=recursion2(child,firstCrossPoint,secondCrossPoint,parent1MiddleCross,parent2MiddleCross)
    return(child)



def pmx(p1, p2, cross1, cross2):
    global parent1,parent2, firstCrossPoint, secondCrossPoint, parent1MiddleCross, parent2MiddleCross, relations, n
    parent1 = p1
    parent2 = p2
    firstCrossPoint = cross1
    secondCrossPoint = cross2
    parent1MiddleCross = parent1[firstCrossPoint:secondCrossPoint]
    parent2MiddleCross = parent2[firstCrossPoint:secondCrossPoint]

    # Concatenating numpy arrays is fucking slower than: converting them to a list() first and then just letting python + them together D:
    # np way: 2.25-2.30 seconds, list(): 2.11-2.16
    #temp_child1 = np.concatenate((parent1[:firstCrossPoint], parent2MiddleCross, parent1[secondCrossPoint:]))
    #temp_child2 = np.concatenate((parent2[:firstCrossPoint], parent1MiddleCross, parent2[secondCrossPoint:]))
    temp_child1 = parent1[:firstCrossPoint] + parent2MiddleCross + parent1[secondCrossPoint:]
    temp_child2 = parent2[:firstCrossPoint] + parent1MiddleCross + parent2[secondCrossPoint:]
    for i in range(len(parent1MiddleCross)):
        relations.append([parent2MiddleCross[i], parent1MiddleCross[i]])

    # kör functionerna
    child1=recursion1(temp_child1,firstCrossPoint,secondCrossPoint,parent1MiddleCross,parent2MiddleCross)
    child2=recursion2(temp_child2,firstCrossPoint,secondCrossPoint,parent1MiddleCross,parent2MiddleCross)
    relations = []
    return child1, child2

# child1: [1 7 3 8 2 6 5 4 9] <- det andra barnet på lösningen
# child2: [9 3 2 4 5 6 7 1 8] <- samma som lektions materialet
# 
# 
# [1, 7, 3,                         # Precis som relationerna sa, börjar barnet på
#           8, 2, 6, 5,             # Sen kommer vår crosssection
#                       4, 9]       # Sen de sista siffrorna
#
# [1, 7, 3, 8, 2, 6, 5, 4, 9]

# Något som inte talades om, men som kan vara viktigt att poängtera är att
# om samma barn gör en ny generation hamnar vi tillbaka till föräldrarna


