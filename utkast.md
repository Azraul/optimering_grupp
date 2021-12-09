# Introduktion

## Uppgift

Inlämningsuppgiften går ut på att hitta ett verkligt problem som kan lösas med metoderna presenterad i kursen. Problemet kan utgå från en problemställning från en annan kurs eller ett problem som uppstår i vardagen/samhället. Systemet som studeranden bestämmer sig för kan vara ett ekonomiskt eller tekniskt system som skall optimeras. Vikt sätts vid att problemet är relevant och kan lösas med en känd metod. Data använt för de beräkningar som görs skall vara riktiga data eller ifall det är svårt att få tag i riktiga data så kan data estimeras, dock så att det är rimliga siffror. Man kan också göra ett teoretiskt arbete av typen ”ett script som tar ett godtyckligt travelling salesman problem och löser det med linjär programmering, med vilket man testar hur stora tsp problem som kan lösas med lp-solve”. Detta är bara ett exempel och man kan med fördel konsultera föreläsaren gällande ämne.

Inlämningsuppgiftens rapport skall vara minst 6 sidor lång. Den skall innehålla en del som beskriver problem-formuleringen (i text form samt någon typ av flow-chart) samt problemets relevans samt sammanhang. Det skall finnas en del som beskriver problemet matematiskt samt data för det, och en del som beskriver lösningsmetoden samt lösningen (även illustrerad grafiskt) för det data som använts.
Studeranden skall också skriva en sammanfattning om hur metoderna funkade och nyttan med dem i lösandet av det specifika problemet. Man får fritt använda illustration/grafer får att få fram viktiga poänger.

Arbetet presenterar under lektion den 10.12.2020. Håll en 10 minuters presentation (med hjälp av pptx eller dylika program) om ert problem och er lösning. OBS PRESENTATIONEN BEDÖMS OCH PÅVERKAR SLUTPOÄNGEN AV GW!!

## Problemformulering

Vi har valt att söka sätt att lösa det logiska spelet sudoku med olika optimerings metoder. Vi vill skriva optimeringarna i Python och sedermera jämföra de olika metoderna i lösningsförmåga, hastighet och om möjligt komplexitet.

Vi väljer Python eftersom det är något vi arbetat med mycket tidigare och är bekanta med, samt att tiden är kort för projektet och alternativ som R därmed uteslöts eftersom det inte är bekant för oss.

LP Solve och pmx är direkta metoder från kursen vi kommer nyttja men även en form av rekursiv lösande (så kallad bakåtspårning/backtracking), samt biblioteket PuLP i Python, vårt valda programmeringsspråk.

### Sudoku definiering

Sudoku är ett numeriskt pussel som består av ett rutnät på 81 rutor som ska fyllas med siffrorna 1 till 9 utan att samma siffra får finnas i samma rad, kolumn eller låda, en låda består av de 9 3x3 rutnät som kan bildas inom sudokuns area, denna begränsning kallas även latinsk kvadrat.

Ett sudokuspel ska helst ha endast en lösning för att anses som bra eller äkta och fyllas med minst 17 siffror från början. Antalet förifyllda siffror avgör oftast svårighetsgraden för sudokupusslet. För närvarande kategoriseras oftast sudokun i fyra kategorier, lätta, mellansvåra, expert/svåra och djävulska (devilish).

Vi kommer välja sudokun i varierande svårighetsgrad med bias för första lämpliga alternativ som uppstår genom sökning på internet med Googles sökmotor, vilket leder oss till < https://sudoku.com/ \> . Sudokuna ska upplevas ha en sporadisk variation av slumpmässiga tal mellan 1 – 9 utplacerade på ett sådant sett att de inte anses manipulativa mot maskinkod, t.ex. ska de inte ha hela första raden eller kolumnen fyllda med resten av raderna tomma.

![sudoku example](/img/sudoku_good_bad.png)

Vi kommer välja en handfull med lämpliga sudokun och spara dem i en Python modul som vi enkelt kan importera och nyttja i samtliga lösningar för projektet.

# Lösningar

I följande kapitel kommer vi presentera våra olika metoder för att lösa sudoku.

<img src="/tmp/.mount_JoplinrXk1Ut/resources/app.asar/img/thinking_meme.jpg" alt="drawing" width="200" class="jop-noMdConv">

**notis:**
[https://en.wikipedia.org/wiki/Sudoku\_solving\_algorithms](https://en.wikipedia.org/wiki/Sudoku_solving_algorithms)

## Linjär programmering i lpsolve

Programmet för linjär programmering med blandade heltal (engelska MILP) kan lösa sudokun med rätt begränsningar och variabler. För att logiskt kunna utesluta valde vi att bygga upp våra variabler på följande sätt:

Sudokuna vi valt att arbeta med har 81 celler, dessa 81 celler har alla 9 möjligheter, en för varje siffra mellan 1 - 9.

Därmed kommer vi definiera 729 (81 * 9) olika binära variabler. De binära variablerna beskrivs med x som generisk variabel term följt av numeriska värdet 1–9, därefter rad och kolumn även de med siffrorna 1–9, t.ex. en 3: a i första rutan, högst upp till vänster beskrivs med x311.

|     | Värde | Rad | Kolumn |
| --- | --- | --- | --- |
| x   | 3   | 1   | 1   |

Vi behöver sedan i huvudsak 4 generella begränsningar:

1.  Varje cell får endast innehåll ett värde
2.  Varje rad får endast innehåll ett av varje värde 1–9
3.  Varje kolumn får endast innehåll ett av varje värde 1–9
4.  Varje låda får endast innehåll ett av varje värde 1–9

För att begränsa varje cell till 1 värde adderar vi alla våra binänar värden för varje cell med begränsning att de tillsammans skall ha summan 1, t.ex. cellen i första raden, första kolumn:

x111 + x211 + x311 + x411 + x511 + x611 + x711 + x811 + x911 = 1

För att begränsa att en rad endast får ha ett av varje värde adderar vi samma värde för hela raden och begränsar det till 1, t.ex. endast ett värde 1 i den första raden:

x111 + x112 + x113 + x114 + x115 + x116 + x117 + x118 + x119 = 1

Samma logik gäller även för kolumner:

x111 + x121 + x131 + x141 + x151 + x161 + x171 + x181 + x191 = 1

Och för lådor:

x111 + x112 + x113 + x121 + x122 + x123 + x131 + x132 + x133 = 1

Varje huvudsaklig begränsning kommer därmed bestå av 81 begränsningar för totalt 324 begränsningar allt som allt.

Vi kan nu börja definiera ett sudoku, lyckligtvis är det relativt simpelt då ett sudoku kommer med färdiga celler ifyllda, vi behöver endast utesluta de cellerna från våra binära variabler och istället begränsa cellerna enligt sudokut, t.ex. är första radens första kolumn en 3: a sätter vi helt enkelt: x311 = 1.

Nu med all vår logik färdig gäller det bara att skriva in alla våra 1053 olika påståenden i lpsolve.
Vi valde att skriva ett Python program som skriver en lp-fil i stället, vi kombinerade det med våra färdiga sudokun.

Vi provade ett relativt enkelt sudoku, sudoku-easy 02:

### Grafisk layout av easy sudoku 02

<img src="/tmp/.mount_JoplinrXk1Ut/resources/app.asar/img/easy_02_sudoku.png" alt="drawing" width="400" class="jop-noMdConv">

Resultat från solvern:

```
-    In the total iteration count 342, 136 (39.8%) were bound flips.
-    There were 3 refactorizations, 0 triggered by time and 3 by density.
-    ... on average 68.7 major pivots per refactorization.
-    The largest [LUSOL v2.2.1.0] fact(B) had 1075 NZ entries, 1.0x largest basis.
-    The maximum B&B level was 1, 0.0x MIP order, 1 at the optimal solution.
-    The constraint matrix inf-norm is 1, with a dynamic range of 1.
-    Time to load data was 0.006 seconds, presolve used 0.005 seconds,
-    ... 0.023 seconds in simplex solver, in total 0.034 seconds.
-    34ms för lpsolve för ett enkelt sudoku. 
```

### Grafisk lösning easy sudoku 02

<img src="/tmp/.mount_JoplinrXk1Ut/resources/app.asar/img/easy_02_solution.png" alt="drawing" width="400" class="jop-noMdConv">

Vi provar ett svårare, sudoku-expert 04:

<img src="/tmp/.mount_JoplinrXk1Ut/resources/app.asar/img/expert_04_sudoku.png" alt="drawing" width="400" class="jop-noMdConv">

Dock efter över 8 timmar och nästan 800 miljoner iterationer stoppade vi solvern och gav upp på problemet.

<img src="/tmp/.mount_JoplinrXk1Ut/resources/app.asar/img/lpsolve_sudoku04_thisisfine_zoom.png" alt="drawing" width="400" class="jop-noMdConv">

Lpsolve har helt tydligt stött på en begränsning, vi antar att lpsolve försöker använda sina råa styrka (brute-force) för att linjärt helt enkelt prova alla kombinationer och även om problemet kanske är helt fullt ut möjligt att lösa finns det för många kombinationer i detta svårare sudokut för att lösa det inom en rimlig tid.

Första raden har 7 saknade celler med 7 olika siffror, det bör alltså finnas 181 440 permutationer (9*8*7*6*5*4*3). Multiplicera sedan detta med följande rad av samma kvantitet och vi kommer snabbt uppnå en storlek vi inte hinner lösa med lpsolve.

## Linjär programmering i Python med PuLP

Typ samma som lpsolve

asdasdasdasd

kommer inte bli mkt txt

asdasdasd

## Backtracking i Python

Asdasdasd

förklara backtracking

gif? img? omg?

asdasdasd

## Genetisk algorithm i Python

En genetisk algoritm (GA) tar inspiration från naturens egen evolution. Utav en mängd olika lösningar, kallad population, två lösningar som har urvalts som goda korsas ihop för att skapa två nya "barn" vilka adderas till den nästa populationen. Många GA:n implementerar en chans åt barnens värden att muteras. Detta steg upprepas tills tillräckligt många barn har skapats, varefter den nya populationen blir evaluerad och korsad ihop.
Nya populationer skapas ända tills en tillräckligt bra lösning har hittats eller mängden generationer överskrider programmets parametrar.

En GA består då av följande komponenter:

- En generator som skapar `n` mängd olika lösningar baserat på inputten
- En fitness evaluerare som rangordnar lösningarna
- Något som bestämmer vilka lösningar väljs för korsande
- En korsare för att kombinera två föräldrar till två barn
- En möjlighet för mutation
- Konditioner när GA ska sluta

Det sägs att GA är bra till att lösa TSP problem, vilket är huvudsakliga orsaken vi valt försöka lösa sudoku med GA är för att (enligt vår enkla uppfattning) sudoku kan ses som ett TSP där bara en nod("siffra") kan besökas ("placeras") utan att man besöker den noden igen (unik siffra per rad/kolumn/cell).

Och eftersom vi ser det som ett traveling salesman problem, använder vi PMX från tidigare hemuppgiften för att korsa lösningarnas x-axel rader.

### Implementation

#### Input

Programmet läser in pussel given som en NumPy array. Baserat på pusslet genereras `n_parents` mängd slumpmässiga lösningar där de tomma platserna fylls med en permutation av 1-9. Siffrorna fylls i radvis så att inga konflikter uppkommer längs med x axeln, detta betyder dock att cellerna och kolumnvis kommer ha duplikater. De förinfyllda siffrorna blir inte ändrade.

En större population ger större sannolikhet att GA:n konvergerar till en korrekt lösning, för en kostnad av minne och cpu-tid.
Till våra easy-level sudokun tycks det räcka med en population av 3000.

#### Fitness

Fitness evalueraren är baserad på Fendrich 2010 http://fendrich.se/blog/2010/05/05/solving-sudoku-with-genetic-algorithms/ , där fitness är bestämt på hur många konflikter(duplikater av siffror) lösningen har rad- kolumn- och cellvis. Lösningarna returneras sorterade med sina respektive poäng.

#### Val av lösningar

Den största utmaningen har varit hur man ska välja lösningar så att generationerna blir bättre, men inte fastna i lokala minimum med låg genetisk variation.

Vi började med att välja kandidater endast med sina vikter. Vikterna kalkylerades så att den bästa lösningen fick 1/2 vikt, den andrabästa 1/3, 1/4 osv.
Detta ledde till populationer som kom till cirka 15 konflikter men konvergerade aldrig till en lösning, inte äns till otroligt lätta pussel som skulle lösas med bruteforce på någon sekund.

Till nästa lät vi para ihop lösningarna i rangordning och så att en lösning bara paras en gång. Detta ledde till en helt homogen population som inte kunde förbättras.

https://nidragedd.github.io/sudoku-genetics/ väljer top % av populationen till att fortplanta med(=selection ratio). Vi implementerade detta också och använder top 25% av lösningarna. Från de här 25% av lösningarna genereras `n_parents` antal nya barn. En fördel med selection ratio är försnabbad beräkning av en nya generation. Med detta lyckas GA:n lösa easy\_02 vilket är en bra framgång, dock ännu en besvikelse då easy\_02 har 31 ofyllda platser, varav många rader har bara 2 stycken ofyllda platser. De andra easy pusslena vill inte än konvergera.

Om ingen förbättring har skett de senaste 500 generationerna, antas det att GA:n har hamnat i en lokal minimum, så populationen startas om. Det vill säga den gamla generationen kastas helt ut och `generate_solutions()` skapar en ny slumpmässig population.

Våran sista ändring av denna komponent var att ta bort viktande helt. Generationernas diversitet blev högre och gjorde det möjligt att lösa alla easy level sudokun vi har.

Som sammanfattning, använder vi:

- Top 25% av generationens lösningar
- Slumpmässigt val av föräldrar
- Föräldrar kan paras ihop många gånger
- Ny population genereras om vi hamnar i en lokal minimum

#### Fortplantning och mutation

Vi har implementerat både PMX och slumpmässig radbyten. Bara en av metoderna används åt gången.

##### PMX

Själva PMX:en är från tidigare hemuppgiften, bara modifierad att fungera åt andra moduler.
PMX körs en rad i gången på slumpmässigt valda crossover punkter. Två versioner av barn genereras enligt PMX reglerna. De förinfyllda siffrorna används inte i crossovern.

##### Radbyten

En slumpmässigt valt rad byts mellan föräldrarna. T.ex. rad `x` av förälder 1 och rad `x + 1` av förälder 2.

##### Mutation

Om `random.random()` har ett värde mindre än `mutation_rate` muteras barnet.
Två slumpmässiga platser på en slumpmässig rad byter plats på barnet.
Vi fann att 10% mutation chans ökar på genetiska diversiteten utan att göra lösningarna o-konvergerande.

### Resultat

#### Easy_02 (supereasy) - PMX
| Parameter     | Värde  |
|---            |---     |
|Korsare        |PMX     |
|Generationer   |3000    |
|Mutation rate  |10%     |
|Selection ratio|25%     |
```
Puzzle:
[[0 8 3 0 2 1 0 0 7]
 [9 6 0 3 0 5 8 2 1]
 [2 5 1 0 0 6 0 9 3]
 [0 4 8 1 0 2 0 7 0]
 [0 2 9 0 0 4 0 3 0]
 [0 3 0 7 0 8 0 4 0]
 [3 7 0 0 0 9 0 1 4]
 [8 1 0 2 5 3 0 6 9]
 [6 9 0 4 0 7 0 8 2]]
Running ga with: n_parents=3000 n_generations=10000 divisor=2 mutation_rate=0.1 selection_ratio=0.25
Start, best fitness: 16
Gen 0 Best fitness= 13
Sudoku solved in generation: 8
Finished, best fitnesses: [0, 0, 0, 0, 2, 2, 2, 2, 2, 2...]
Best solution:
[[4 8 3 9 2 1 6 5 7]
 [9 6 7 3 4 5 8 2 1]
 [2 5 1 8 7 6 4 9 3]
 [5 4 8 1 3 2 9 7 6]
 [7 2 9 5 6 4 1 3 8]
 [1 3 6 7 9 8 2 4 5]
 [3 7 2 6 8 9 5 1 4]
 [8 1 4 2 5 3 7 6 9]
 [6 9 5 4 1 7 3 8 2]]
Finished in  2.57
```

PMX lyckas lösa easy_02 i 2.57 sekunder på generation 8

# Jämförelser

## Lösningsförmåga

Asdasdasd

de är alla smartare än oss(inte sudoku GA)

## Hastighet

Asdasd

de är alla snabbare än oss

## Komplexitet

Asdasd

de är alla mindre komplexa än oss

## Reflektioner

asdasdasdasd

ai supreme, when do we get replaced?

# Källor

*arcada skriv guide iirc sätt att skriva källor*

Wikipedia, senast redigerad 2020, Sudoku, https://sv.wikipedia.org/, sedd 06 dec 2021, < https://sv.wikipedia.org/wiki/Sudoku>

Norvig, Peter, 2011, Solving Every Sudoku Puzzle, https://norvig.com/ , sedd 04 dec 2021, < https://norvig.com/sudoku.html >

Easybrain, senast redigerad 2021, https://easybrain.com/, sedd 04 dec 2021, < https://sudoku.com/ >