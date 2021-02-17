#%%
prog = {
    "band" : ["Arte1", "BandSports", "BandNews", "Sex Privé", "Terra Viva"],
    "bloomberg" : ["bloomberg"],
    "box_brasil" : ["box_brasil"],
    "CNN" : ["CNN BRASIL"],
    "DISCOVERY" : ["Discovery Channel", "Discovery Kids", "DHH"],
    "ESPN" : ["ESPN+", "ESPN", "ESPN BRASIL", "ESPN EXTRA"],
    "Disney" : ["DISNEY XD", "DISNEY JR.", "DISNEY CHANNEL"],
    "Fox" : ["FOX", "FOX SPORTS", "BABY TV", "NAT GEO KIDS", "FOX NEWS","FOX", "NAT GEO", "FOX LIFE", "FOX Premium", "FOX Premimum 2"],
    "Globosat" : ["Telecine Action", "Telecine Pipoca", "Telecine Premium", "Telecine Fun", "Telecine Pipoca", "Telecine Cult",
    "GNT", "SPORTV", "MULTISHOW", "BIS", "VIVA", "OFF", "GLOOB", "GLOBINHO", "GLOBO NEWS", "globo", "MEGAPIX", "CANAL BRASIL"],
    "HBO" : ["A&E", "AXN", "E!", "Entertainment Television", "Sony Entertainment", "Lifetime", "H2", "History Channel", "Warner Channel",
    "HBO", "HBO2", "HBO Plus", "HBO Famil", "HBO Signature", "HBO Mundi", "HBO Pop", "HBO Extreme"],
    "SHOPTIME" : ["SHOPTIME"],
    "TUNER" : ["CNNI", "CNNE", "CARTOON", "TNT", "BOOM","TCM", "GLITZ", "TOONCAST", "TRUTV", "SPACE", "ISAT", "TBS"],
    "Viacom" : ["MTV", "Nickelodeon", "Nick Jr", "Paramount", "Comedy Central", "VH1 Mega Hits"],
}

ags = """1º – Globo: 12,37
2º – Record: 3,97
3º – SBT: 3,94
4º – Band: 1,12
5º – RedeTV!: 0,51
6º – Viva: 0,33
7º – Cultura: 0,23
8º – TNT: 0,23
9º – Cartoon Network: 0,21
10º – TV Brasil: 0,21
11º – Discovery Kids: 0,21
12º – Globo News: 0,20
13º – Discovery: 0,20
14º – SporTV: 0,18
15º – Rede Vida: 0,18
16º – Universal TV: 0,17
17º – Megapix: 0,16
18º – Discovery H&H: 0,15
19º – Aparecida: 0,15
20º – Gloob: 0,15
21º – AXN: 0,14
22º – Nick: 0,14
23º – Record News: 0,14
24º – Fox: 0,13
25º – Multishow: 0,11
26º – Space: 0,10
27º – Warner: 0,10
28º – ID: 0,09
29º – TNT Séries: 0,08
30º – Telecine Pipoca: 0,08
31º – TLC: 0,08
32º – GNT: 0,08
33º – NatGeo: 0,08
34º – Nick Jr: 0,08
35º – Animal Planet: 0,08
36º – Boomerang: 0,08
37º – Telecine Action: 0,07
38º – Fox Sports: 0,07
39º – Comedy Central: 0,07
40º – Cinemax: 0,07
41º – History: 0,07
42º – Telecine Premium: 0,07
43º – FX: 0,07
44º – Disney: 0,06
45º – SporTV 2: 0,06
46º – Gazeta: 0,06
47º – CNN Brasil: 0,06
48º – Sony: 0,05
49º – CNT: 0,05
50º – Paramount: 0,05
51º – Fox Life: 0,05
52º – Telecine Fun: 0,04
53º – Canal Brasil: 0,04
54º – Discovery Turbo: 0,04
55º – Studio Universal: 0,04
56º – NatGeo Wild: 0,04
57º – Novo Tempo: 0,04
58º – MTV: 0,03
59º – RIT: 0,03
60º – ESPN Brasil: 0,03
61º – SporTV 3: 0,03
62º – A&E: 0,03
63º – Telecine Touch: 0,03
64º – Disney XD: 0,03
65º – Food Network: 0,03
66º – ESPN: 0,02
67º – TV Escola; 0,02
68º – AMC: 0,02
69º – Disney Jr: 0,02
70º – BandNews: 0,02
71º – E!: 0,02
72º – HBO: 0,02
73º – HBO2: 0,02
74º – H2: 0,02
75º – Telecine Cult: 0,02
76º – Lifetime: 0,02
77º – TBS: 0,01
78º – TCM: 0,01
79º – Fox Sports 2: 0,01
80º – TV Senado: 0,01
81º – TV Câmara: 0,01
82º – BandSports: 0,01
83º – Futura: 0,01
84º – SyFy: 0,01
85º – NatGeo Kids: 0,00
86º – Travel Box: 0,00
87º – Shoptime: 0,00
88º – WooHoo: 0,00
89º – Film&Arts: 0,00
90º – ESPN2: 0,00
91º – TV Justiça: 0,00"""
stb = """1º – Globo 12,06
2º – Record 4,26
3º – SBT 4,01
4º – Band 1,18
5º – RedeTV! 0,52
6º – Viva 0,28
7º – Cultura 0,25
8º – Cartoon Network 0,21
9º – TV Brasil 0,19
10º – Discovery Kids 0,19
11º – Globo News 0,19
12º – SporTV 0,18
13º – Discovery Channel 0,18
14º – Rede Vida 0,17
15º – Gloob 0,17
16º – Universal TV 0,16
17º – Megapix 0,16
18º – AXN 0,16
19º – Nickelodeon 0,14
20º – Record News 0,14
21º – TV Aparecida 0,14
22º – Discovery H&H 0,13
23º – Fox Sports 0,13
24º – TNT 0,13
25º – Multishow 0,11
26º – Space 0,11
27º – Fox Channel 0,11
28º – Warner Channel 0,10
29º – ID 0,09
30º – TNT Séries 0,08
31º – Boomerang 0,08
32º – Nick Jr 0,07
33º – TLC 0,07
34º – Telecine Action 0,07
35º – GNT 0,07
36º – Animal Planet 0,07
37º – NatGeo 0,07
38º – Disney Channel 0,07
39º – Comedy Central 0,07
40º – Gazeta 0,07
41º – Telecine Pipoca 0,07
42º – SporTV 2 0,06
43º – FX 0,06
44º – History 0,06
45º – Cinemax 0,06
46º – CNN Brasil 0,06
47º – Telecine Premium 0,06
48º – ESPN Brasil 0,06
49º – Paramount Network 0,05
50º – SporTV 3 0,05
51º – Discovery Turbo 0,04
52º – Telecine Fun 0,04
53º – Canal Brasil 0,04
54º – Sony Channel 0,04
55º – Studio Universal 0,04
56º – Fox Life 0,04
57º – CNT 0,04
58º – TV Novo Tempo 0,04
59º – RIT 0,04
60º – NatGeo Wild 0,04
61º – ESPN 0,03
62º – A&E 0,03
63º – Telecine Touch 0,03
64º – Disney XD 0,03
65º – Disney Jr 0,03
66º – AMC 0,03
67º – Food Network 0,03
68º – BandNews 0,02
69º – MTV 0,02
70º – HBO 0,02
71º – H2 0,02
72º – HBO2 0,02
73º – E! 0,02
74º – Lifetime 0,02
75º – Telecine Cult 0,02
76º – TBS 0,01
77º – Fox Sports 2 0,01
78º – TV Escola 0,01
79º – TCM 0,01
80º – TV Câmara 0,01
81º – TV Senado 0,01
82º – ESPN2 0,01
83º – BandSports 0,01
84º – SyFy 0,01
85º – Futura 0,01
86º – Shoptime 0,01
87º – NatGeo Kids 0,00
88º – Film&Arts 0,00
89º – Travel Box Brazil 0,00
90º – WooHoo 0,00
91º – TV Justiça 0,00"""
out = """1º Globo – 11,36
2º Record – 4,60
3º SBT – 4,01
4º Band – 1,08
5º RedeTV! – 0,48
6º Viva – 0,27
7º Cultura – 0,27
8º SporTV – 0,22
9º Cartoon Network – 0,21
10º TV Brasil – 0,21
11º Discovery Kids – 0,20
12º Globo News – 0,18
13º AXN – 0,18
14º Rede Vida – 0,17
15º Discovery Channel – 0,17
16º Gloob – 0,17
17º Universal TV – 0,15
18º Megapix – 0,15
19º TV Aparecida – 0,15
20º Record News – 0,14
21º TNT – 0,14
22º Discovery Home & Health – 0,13
23º Nickelodeon – 0,12
24º Fox Channel – 0,11
25º Space – 0,11
26º Multishow – 0,10
27º Fox Sports – 0,09
28º Discovery ID – 0,09
29º Warner – 0,08
30º Telecine Action – 0,08
31º NatGeo – 0,07
32º ESPN Brasil – 0,07
33º TLC – 0,07
34º TNT Séries – 0,07
35º Telecine Premium – 0,07
36º GNT – 0,07
37º Comedy Central – 0,07
38º Telecine Pipoca – 0,07
39º Animal Planet – 0,07
40º FX – 0,07
41º TV Gazeta – 0,07
42º Boomerang – 0,07
43º Nick Jr – 0,06
44º SporTV 2 – 0,06
45º History – 0,06
46º Cinemax – 0,05
47º CNN Brasil – 0,05
48º Disney Channel – 0,05
49º Studio Universal – 0,04
50º Sony – 0,04
51º Paramount Network – 0,04
52º Telecine Fun – 0,04
53º Fox Life – 0,04
54º CNT – 0,04
55º Canal Brasil – 0,04
56º SporTV 3 – 0,04
57º Telecine Touch – 0,04
58º Discovery Turbo – 0,04
59º TV Novo Tempo – 0,04
60º NatGeo Wild – 0,04
61º A&E – 0,03
62º RIT – 0,03
63º BandNews TV – 0,03
64º ESPN – 0,03
65º Disney XD – 0,03
66º HBO – 0,02
67º Food Network – 0,02
68º AMC – 0,02
69º Disney Jr – 0,02
70º HBO2 – 0,02
71º E! – 0,02
72º TBS – 0,02
73º H2 – 0,02
74º Telecine Cult – 0,02
75º MTV – 0,02
76º Fox Sports 2 – 0,02
77º Lifetime – 0,02
78º TV Escola – 0,01
79º TV Câmara – 0,01
80º BandSports – 0,01
81º TCM – 0,01
82º TV Senado – 0,01
83º ESPN2 – 0,01
84º Futura – 0,01
85º SyFy – 0,01
86º Shoptime – 0,01
87º WooHoo – 0,00
88º Travel Box Brazil – 0,00
89º Film&Arts – 0,00
90º NatGeo Kids – 0,00
91º TV Justiça – 0,00"""
nov = """1º – Globo 11,74
2º – Record 4,77
3º – SBT 3,99
4º – Band 1,07
5º – RedeTV! 0,47
6º – Viva 0,28
7º – Globo News 0,26
8º – Cultura 0,24
9º – SporTV 0,24
10º – TV Brasil 0,22
11º – Cartoon Network 0,22
12º – Discovery Kids 0,21
13º – Discovery Channel 0,17
14º – Gloob 0,16
15º – Universal TV 0,15
16º – Rede Vida 0,15
17º – Megapix 0,15
18º – Record News 0,14
19º – AXN 0,13
20º – TV Aparecida 0,13
21º – Discovery Home & Health 0,13
22º – TNT 0,12
23º – Nickelodeon 0,12
24º – Multishow 0,10
25º – Fox Channel 0,10
26º – Space 0,09
27º – CNN Brasil 0,09
28º – ID 0,09
29º – Fox Sports 0,09
30º – Warner Channel 0,08
31º – Comedy Central 0,08
32º – TNT Séries 0,08
33º – Telecine Action 0,07
34º – Telecine Pipoca 0,07
35º – Telecine Premium 0,07
36º – Studio Universal 0,07
37º – Gazeta 0,07
38º – Animal Planet 0,07
39º – ESPN Brasil 0,07
40º – GNT 0,07
41º – Boomerang 0,06
42º – TLC 0,06
43º – FX 0,06
44º – NatGeo 0,06
45º – SporTV 2 0,06
46º – Cinemax 0,06
47º – Nick Jr. 0,05
48º – History 0,05
49º – Disney Channel 0,05
50º – Sony 0,04
51º – Telecine Fun 0,04
52º – Discovery Turbo 0,04
53º – Paramount Network 0,04
54º – Fox Life 0,04
55º – NatGeo Wild 0,04
56º – CNT 0,04
57º – BandNews TV 0,03
58º – Telecine Touch 0,03
59º – Canal Brasil 0,03
60º – TV Novo Tempo 0,03
61º – SporTV 3 0,03
62º – A&E 0,03
63º – RIT 0,03
64º – HBO 0,03
65º – Food Network 0,03
66º – AMC 0,03
67º – E! 0,02
68º – MTV 0,02
69º – Disney Júnior 0,02
70º – HBO2 0,02
71º – Telecine Cult 0,02
72º – Disney XD 0,02
73º – H2 0,02
74º – ESPN 0,02
75º – TBS 0,02
76º – Lifetime 0,01
77º – TV Escola 0,01
78º – TV Câmara 0,01
79º – Fox Sports 2 0,01
80º – TCM 0,01
81º – TV Senado 0,01
82º – Futura 0,01
83º – BandSports 0,01
84º – Shoptime 0,01
85º – SyFy 0,01
86º – ESPN2 0,00
87º – Travel Box Brazil 0,00
88º – Film & Arts 0,00
89º – WooHoo 0,00
90º – NatGeo Kids 0,00
91º – TV Justiça 0,00"""

dez = """1º Globo 11,17
2º Record 4,41
3º SBT 3,72
4º Band 1,02
5º RedeTV! 0,42
6º Viva 0,26
7º TV Cultura 0,24
8º Discovery Kids 0,21
9º Globo News 0,21
10º Cartoon Network 0,18
11º SporTV 0,16
12º Megapix 0,16
13º Universal TV 0,15
14º TV Brasil 0,15
15º Rede Vida 0,14
16º Discovery Channel 0,14
17º Record News 0,14
18º TV Aparecida 0,14
19º Gloob 0,13
20º AXN 0,12
21º TNT 0,12
22º Nickelodeon 0,11
23º Discovery Home & Health 0,11
24º Fox Sports 0,10
25º Multishow 0,10
26º Space 0,09
27º Fox Channel 0,09
28º Studio Universal 0,09
29º Warner 0,07
30º ESPN Brasil 0,07
31º Discovery ID 0,07
32º Telecine Action 0,06
33º TLC 0,06
34º National Geographic 0,06
35º TV Gazeta 0,06
36º CNN Brasil 0,06
37º Animal Planet 0,06
38º FX 0,06
39º SporTV 2 0,06
40º GNT 0,06
41º Telecine Premium 0,06
42º Cinemax 0,06
43º Telecine Pipoca 0,05
44º Boomerang 0,05
45º Nick Jr 0,04
46º History 0,04
47º Sony 0,04
48º CNT 0,04
49º Paramount Network 0,04
50º Canal Brasil 0,04
51º Disney Channel 0,04
52º Nat Geo Wild 0,04
53º Fox Life 0,04
54º Telecine Fun 0,03
55º Discovery Turbo 0,03
56º TV Novo Tempo 0,03
57º Telecine Touch 0,03
58º Band News 0,03
59º Rit 0,03
60º A&E 0,03
61º HBO 0,02
62º MTV 0,02
63º AMC 0,02
64º ESPN 0,02
65º Food Network 0,02
66º Disney Jr 0,02
67º E! Entertainment 0,02
68º Disney XD 0,02
69º Lifetime 0,02
70º H2 0,02
71º Telecine Cult 0,02
72º TV Câmara 0,02
73º TBS 0,01
74º TV Escola 0,01
75º Fox Sports2 0,01
76º TV Senado 0,01
77º Futura 0,01
78º SyFy 0,01
79º Band Sports 0,01
80º Shop Time 0,00
81º ESPN2 Brasil 0,00
82º Film & Arts 0,00
83º WooHoo 0,00
84º Travel Box Brasil 0,00
85º Nat Geo Kids 0,00
86º TV Justiça 0,00
87º Max Prime 0,00
88º CNN Español 0,00
89º Sesc TV 0,00
90º ZooMoo 0,00"""

months = [ags, stb, out, nov, dez]

linhas = [m.split("\n") for m in months]
canais = {}
for lin in linhas:
    for linha in lin:
        canal = " ".join((linha.replace("–", "").split(" "))[1:-1])
        if canal.startswith(" "): canal = canal[1:]
        if canal.endswith(" "): canal = canal[:-1]
        if canal.endswith(":"): canal = canal[:-1]
        audiencia = linha.split(" ")[-1]
        canais[canal.lower()] = canais.get(canal.lower(), 0) + float(audiencia.replace(",","."))


def serach_op(canal):
    for pr in prog:
        l_prog = {p:[] for p in prog} 
        for p in prog:
            for i in prog[p]:
                l_prog[p].append(i.lower().replace(" ",""))
        if canal.replace(" ","") in l_prog[pr]: return pr
    return ""

p = {}

for canal in canais:
    pr = serach_op(canal)
    if canal == "globo":
        print(canais[canal])
    if not pr: continue
    p[pr] = p.get(pr, 0) + canais[canal]

dp = dict(sorted(p.items(), key=lambda item: item[1], reverse=True))
for i in dp:
    print(i.title(), "%.2f" % round(dp[i], 2))

print("\n")

d = dict(sorted(canais.items(), key=lambda item: item[1], reverse=True))
for canal in d:
    print(canal.title(), "%.2f" % round(d[canal], 2))

# %%
