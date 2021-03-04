clear all

import_excel pub_date pub_type JEL_co_1 JEL_co_2 JEL_co_3 JEL_co_4 JEL_co_5 JEL_co_6 JEL_co_7 using data/data, sheet(Stata)


keep if pub_date>"2015"
drop if pub_date=="forthcoming"
drop if pub_type=="Editor's Introduction"
drop if pub_date>"2020"
drop if missing(JEL_co_1)


foreach var of varlist JEL_co_1-JEL_co_7 {
replace `var'=strtrim(`var')
}

gen str3 jelco1=substr(JEL_co_1,1,2)
gen str3 jelco2=substr(JEL_co_2,1,2)
gen str3 jelco3=substr(JEL_co_3,1,2)
gen str3 jelco4=substr(JEL_co_4,1,2)
gen str3 jelco5=substr(JEL_co_5,1,2)
gen str3 jelco6=substr(JEL_co_6,1,2)
gen str3 jelco7=substr(JEL_co_7,1,2)

list jelco* JEL_co_* pub_date

gen wei_ght =0

* qui assegna un peso a ciascun record in base al numero di jelcodes di ognuno

replace wei_ght=1/7  if jelco2~=""&jelco3~=""&jelco4~=""&jelco5~=""&jelco6~=""&jelco7~=""
replace wei_ght=1/6  if jelco2~=""&jelco3~=""&jelco4~=""&jelco5~=""&jelco6~=""&jelco7==""
replace wei_ght=0.2  if jelco2~=""&jelco3~=""&jelco4~=""&jelco5~=""&jelco6==""&jelco7==""
replace wei_ght=0.25 if jelco2~=""&jelco3~=""&jelco4~=""&jelco5==""&jelco6==""&jelco7==""
replace wei_ght=0.33 if jelco2~=""&jelco3~=""&jelco4==""&jelco5==""&jelco6==""&jelco7==""
replace wei_ght=0.5  if jelco2~=""&jelco3==""&jelco4==""&jelco5==""&jelco6==""&jelco7==""
replace wei_ght=1    if jelco2==""&jelco3==""&jelco4==""&jelco5==""&jelco6==""&jelco7==""

list jelco* wei_ght


* mette in riga data, jelcode e weight

stack pub_date jelco1 wei_ght pub_date jelco2 wei_ght pub_date jelco3 wei_ght pub_date jelco4 wei_ght pub_date jelco5 wei_ght pub_date jelco6 wei_ght pub_date jelco7 wei_ght, into (pdate jelc weig) clear
drop if jelc==""
*
drop _stack

* qui crea jel1 da jelc
encode jelc, gen (jel1)

* aggrega contando i record per data, jelc e peso

collapse (count) jel1 ,by(pdate jelc weig)

* molti e' la moltiplicazione del peso per quante volte e' presente (???)

gen molti=weig*jel1

tabulate jelc [iweight=molti]

* somma i contributi (molti) per data e jelcode

collapse (sum) molti ,by(pdate jelc)
*
list pdate jelc molti, clean
*
gen str3 jelc_1=substr(jelc,1,1)

*G                    mercati finanziari e banche
*F                    economia internazionale, commercio, cambi
*E3-E5                politica monetaria, prezzi, ciclo economico
*C                    econometria, metodi matematici
*D6,J,M               mercato del lavoro, salari, innovazione
*D1-D5,D7-D8,E1-E2,   consumo, risparmio, redditi, ricchezza
*E6,H                 politica fiscale
*K,L                  economia industriale
*O,I,N                educazione, salute, sviluppo, storia
*Q,R,Y,Z,P,D9,A,B     residui: economia regionale, energia, mercato immobiliare

*gen      temi_p =9
gen      temi_p =10
replace  temi_p =9 if jelc_1=="Q"|| jelc_1=="R"|| jelc_1=="Y"||jelc_1=="Z"||jelc_1=="P"||jelc_1=="A"||jelc_1=="B"||jelc=="D9"
replace  temi_p =0 if jelc_1=="G"
replace  temi_p =4 if jelc_1=="F"
replace  temi_p =1 if jelc=="E3"||jelc=="E4"||jelc=="E5"
replace  temi_p =8 if jelc_1=="C"
replace  temi_p =3 if jelc=="D6"||jelc_1=="J"||jelc_1=="M"
replace  temi_p =2 if jelc=="D1"||jelc=="D2"||jelc=="D3"||jelc=="D4"||jelc=="D5"||jelc=="D7"||jelc=="D8"||jelc=="E1"||jelc=="E2"
replace  temi_p =5 if jelc=="E6"||jelc_1=="H"
replace  temi_p =7 if jelc_1=="K"||jelc_1=="L"
replace  temi_p =6 if jelc_1=="O"||jelc_1=="I"



collapse (sum) molti ,by(pdate temi_p)
list,clean

export excel 



