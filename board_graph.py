#!/usr/bin/env python

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

province_types = ["inland", "water", "coastal"]
provinces = {
    "Boh": {
        "long_name": "Bohemia",
        "type": "inland",
        "home_power": "Austria",
        "supply_centre": False
    },
    "Bud": {
        "long_name": "Budapest",
        "type": "inland",
        "home_power": "Austria",
        "supply_centre": True
    },
    "Gal": {
        "long_name": "Galicia",
        "type": "inland",
        "home_power": "Austria",
        "supply_centre": False
    },
    "Tri": {
        "long_name": "Trieste",
        "type": "coastal",
        "home_power": "Austria",
        "supply_centre": True
    },
    "Tyr": {
        "long_name": "Tyrolia",
        "type": "inland",
        "home_power": "Austria",
        "supply_centre": False
    },
    "Vie": {
        "long_name": "Vienna",
        "type": "inland",
        "home_power": "Austria",
        "supply_centre": True
    },
    "Cly": {
        "long_name": "Clyde",
        "type": "coastal",
        "home_power": "England",
        "supply_centre": False
    },
    "Edi": {
        "long_name": "Edinburgh",
        "type": "coastal",
        "home_power": "England",
        "supply_centre": True
    },
    "Lvp": {
        "long_name": "Liverpool",
        "type": "coastal",
        "home_power": "England",
        "supply_centre": True
    },
    "Lon": {
        "long_name": "London",
        "type": "coastal",
        "home_power": "England",
        "supply_centre": True
    },
    "Wal": {
        "long_name": "Wales",
        "type": "coastal",
        "home_power": "England",
        "supply_centre": False
    },
    "Yor": {
        "long_name": "Yorkshire",
        "type": "coastal",
        "home_power": "England",
        "supply_centre": False
    },
    "Bre": {
        "long_name": "Brest",
        "type": "coastal",
        "home_power": "France",
        "supply_centre": True
    },
    "Bur": {
        "long_name": "Burgundy",
        "type": "inland",
        "home_power": "France",
        "supply_centre": False
    },
    "Gas": {
        "long_name": "Gascony",
        "type": "coastal",
        "home_power": "France",
        "supply_centre": False
    },
    "Mar": {
        "long_name": "Marseilles",
        "type": "coastal",
        "home_power": "France",
        "supply_centre": True
    },
    "Par": {
        "long_name": "Paris",
        "type": "inland",
        "home_power": "France",
        "supply_centre": True
    },
    "Pic": {
        "long_name": "Picardy",
        "type": "coastal",
        "home_power": "France",
        "supply_centre": False
    },
    "Ber": {
        "long_name": "Berlin",
        "type": "coastal",
        "home_power": "Germany",
        "supply_centre": True
    },
    "Kie": {
        "long_name": "Kiel",
        "type": "coastal",
        "home_power": "Germany",
        "supply_centre": True
    },
    "Mun": {
        "long_name": "Munich",
        "type": "inland",
        "home_power": "Germany",
        "supply_centre": True
    },
    "Pru": {
        "long_name": "Prussia",
        "type": "coastal",
        "home_power": "Germany",
        "supply_centre": False
    },
    "Ruh": {
        "long_name": "Ruhr",
        "type": "inland",
        "home_power": "Germany",
        "supply_centre": False
    },
    "Sil": {
        "long_name": "Silesia",
        "type": "inland",
        "home_power": "Germany",
        "supply_centre": False
    },
    "Apu": {
        "long_name": "Apuila",
        "type": "coastal",
        "home_power": "Italy",
        "supply_centre": False
    },
    "Nap": {
        "long_name": "Naples",
        "type": "coastal",
        "home_power": "Italy",
        "supply_centre": True
    },
    "Pie": {
        "long_name": "Piedmont",
        "type": "coastal",
        "home_power": "Italy",
        "supply_centre": False
    },
    "Rom": {
        "long_name": "Rome",
        "type": "coastal",
        "home_power": "Italy",
        "supply_centre": True
    },
    "Tus": {
        "long_name": "Tuscany",
        "type": "coastal",
        "home_power": "Italy",
        "supply_centre": False
    },
    "Ven": {
        "long_name": "Venice",
        "type": "coastal",
        "home_power": "Italy",
        "supply_centre": True
    },
    "Lvn": {
        "long_name": "Livonia",
        "type": "coastal",
        "home_power": "Russia",
        "supply_centre": False
    },
    "Mos": {
        "long_name": "Moscow",
        "type": "inland",
        "home_power": "Russia",
        "supply_centre": True
    },
    "Sev": {
        "long_name": "Sevastopol",
        "type": "coastal",
        "home_power": "Russia",
        "supply_centre": True
    },
    "StP": {
        "long_name": "St. Petersburg",
        "type": "coastal",
        "home_power": "Russia",
        "supply_centre": True
    },
    "Ukr": {
        "long_name": "Ukraine",
        "type": "inland",
        "home_power": "Russia",
        "supply_centre": False
    },
    "War":{
        "long_name": "Warsaw",
        "type": "inland",
        "home_power": "Russia",
        "supply_centre": True
    },
    "Ank": {
        "long_name": "Ankara",
        "type": "coastal",
        "home_power": "Turkey",
        "supply_centre": True
    },
    "Arm": {
        "long_name": "Armenia",
        "type": "coastal",
        "home_power": "Turkey",
        "supply_centre": False
    },
    "Con": {
        "long_name": "Constantinople",
        "type": "coastal",
        "home_power": "Turkey",
        "supply_centre": True
    },
    "Smy": {
        "long_name": "Smyrna",
        "type": "coastal",
        "home_power": "Turkey",
        "supply_centre": True
    },
    "Syr": {
        "long_name": "Syria",
        "type": "coastal",
        "home_power": "Turkey",
        "supply_centre": False
    },
    "Alb": {
        "long_name": "Albania",
        "type": "coastal",
        "home_power": "Neutral",
        "supply_centre": False
    },
    "Bel": {
        "long_name": "Belgium",
        "type": "coastal",
        "home_power": "Neutral",
        "supply_centre": True
    },
    "Bul": {
        "long_name": "Bulgaria",
        "type": "coastal",
        "home_power": "Neutral",
        "supply_centre": True
    },
    "Den": {
        "long_name": "Denmark",
        "type": "coastal",
        "home_power": "Neutral",
        "supply_centre": True
    },
    "Fin": {
        "long_name": "Finland",
        "type": "coastal",
        "home_power": "Neutral",
        "supply_centre": False
    },
    "Gre": {
        "long_name": "Greece",
        "type": "coastal",
        "home_power": "Neutral",
        "supply_centre": True
    },
    "Hol": {
        "long_name": "Holland",
        "type": "coastal",
        "home_power": "Neutral",
        "supply_centre": True
    },
    "Nwy": {
        "long_name": "Norway",
        "type": "coastal",
        "home_power": "Neutral",
        "supply_centre": True
    },
    "NAf": {
        "long_name": "North Africa",
        "type": "coastal",
        "home_power": "Neutral",
        "supply_centre": False
    },
    "Por": {
        "long_name": "Portugal",
        "type": "coastal",
        "home_power": "Neutral",
        "supply_centre": True
    },
    "Rum": {
        "long_name": "Rumania",
        "type": "coastal",
        "home_power": "Neutral",
        "supply_centre": True
    },
    "Ser": {
        "long_name": "Serbia",
        "type": "inland",
        "home_power": "Neutral",
        "supply_centre": True
    },
    "Spa": {
        "long_name": "Spain",
        "type": "coastal",
        "home_power": "Neutral",
        "supply_centre": True
    },
    "Swe": {
        "long_name": "Sweden",
        "type": "coastal",
        "home_power": "Neutral",
        "supply_centre": True
    },
    "Tun": {
        "long_name": "Tunis",
        "type": "coastal",
        "home_power": "Neutral",
        "supply_centre": True
    },
    "Adr": {
        "long_name": "Adriatic Sea",
        "type": "water",
        "home_power": "sea",
        "supply_centre": False
    },
    "Aeg": {
        "long_name": "Aegean Sea",
        "type": "water",
        "home_power": "sea",
        "supply_centre": False
    },
    "Bal": {
        "long_name": "Baltic Sea",
        "type": "water",
        "home_power": "sea",
        "supply_centre": False
    },
    "Bar": {
        "long_name": "Barents Sea",
        "type": "water",
        "home_power": "sea",
        "supply_centre": False
    },
    "Bla": {
        "long_name": "Black Sea",
        "type": "water",
        "home_power": "sea",
        "supply_centre": False
    },
    "Eas": {
        "long_name": "Eastern Mediterranean",
        "type": "water",
        "home_power": "sea",
        "supply_centre": False
    },
    "Eng": {
        "long_name": "English Channel",
        "type": "water",
        "home_power": "sea",
        "supply_centre": False
    },
    "Bot": {
        "long_name": "Gulf of Bothnia",
        "type": "water",
        "home_power": "sea",
        "supply_centre": False
    },
    "GoL": {
        "long_name": "Gulf of Lyon",
        "type": "water",
        "home_power": "sea",
        "supply_centre": False
    },
    "Hel": {
        "long_name": "Helgoland Bight",
        "type": "water",
        "home_power": "sea",
        "supply_centre": False
    },
    "Ion": {
        "long_name": "Ionian Sea",
        "type": "water",
        "home_power": "sea",
        "supply_centre": False
    },
    "Iri": {
        "long_name": "Irish Sea",
        "type": "water",
        "home_power": "sea",
        "supply_centre": False
    },
    "Mid": {
        "long_name": "Mid-Atlantic Ocean",
        "type": "water",
        "home_power": "sea",
        "supply_centre": False
    },
    "NAt": {
        "long_name": "North Atlantic Ocean",
        "type": "water",
        "home_power": "sea",
        "supply_centre": False
    },
    "Nth": {
        "long_name": "North Sea",
        "type": "water",
        "home_power": "sea",
        "supply_centre": False
    },
    "Nrg": {
        "long_name": "Norwegian Sea",
        "type": "water",
        "home_power": "sea",
        "supply_centre": False
    },
    "Ska": {
        "long_name": "Skagerrak",
        "type": "water",
        "home_power": "sea",
        "supply_centre": False
    },
    "Tyn": {
        "long_name": "Tyrrhenian Sea",
        "type": "water",
        "home_power": "sea",
        "supply_centre": False
    },
    "Wes": {
        "long_name": "Western Mediterranean",
        "type": "water",
        "home_power": "sea",
        "supply_centre": False
    },
    "Swi": {
        "long_name": "Switzerland",
        "type": "impassible",
        "home_power": "none",
        "supply_centre": False
    }
}
province_borders = [
    ("Boh", "Mun"),
    ("Boh", "Sil"),
    ("Boh", "Gal"),
    ("Boh", "Vie"),
    ("Boh", "Tyr"),
    ("Bud", "Tri"),
    ("Bud", "Vie"),
    ("Bud", "Gal"),
    ("Bud", "Rum"),
    ("Bud", "Ser"),
    ("Gal", "Sil"),
    ("Gal", "War"),
    ("Gal", "Ukr"),
    ("Gal", "Rum"),
    ("Tri", "Adr"),
    ("Tri", "Ven"),
    ("Tri", "Tyr"),
    ("Tri", "Vie"),
    ("Tri", "Ser"),
    ("Tri", "Alb"),
    ("Tyr", "Ven"),
    ("Tyr", "Pie"),
    ("Tyr", "Mun"),
    ("Tyr", "Vie"),
    ("Cly", "NAt"),
    ("Cly", "Nrg"),
    ("Cly", "Edi"),
    ("Cly", "Lvp"),
    ("Edi", "Nrg"),
    ("Edi", "Nth"),
    ("Edi", "Yor"),
    ("Edi", "Lvp"),
    ("Lvp", "Iri"),
    ("Lvp", "NAt"),
    ("Lvp", "Yor"),
    ("Lvp", "Wal"),
    ("Lon", "Eng"),
    ("Lon", "Wal"),
    ("Lon", "Yor"),
    ("Lon", "Nth"),
    ("Wal", "Iri"),
    ("Wal", "Yor"),
    ("Wal", "Eng"),
    ("Yor", "Nth"),
    ("Bre", "Mid"),
    ("Bre", "Eng"),
    ("Bre", "Pic"),
    ("Bre", "Par"),
    ("Bre", "Gas"),
    ("Bur", "Gas"),
    ("Bur", "Par"),
    ("Bur", "Pic"),
    ("Bur", "Bel"),
    ("Bur", "Ruh"),
    ("Bur", "Mun"),
    ("Bur", "Mar"),
    ("Gas", "Mid"),
    ("Gas", "Par"),
    ("Gas", "Mar"),
    ("Gas", "Spa"),
    ("Mar", "Spa"),
    ("Mar", "Pie"),
    ("Mar", "GoL"),
    ("Par", "Pic"),
    ("Pic", "Eng"),
    ("Pic", "Bel"),
    ("Ber", "Kie"),
    ("Ber", "Bal"),
    ("Ber", "Pru"),
    ("Ber", "Sil"),
    ("Ber", "Mun"),
    ("Kie", "Hol"),
    ("Kie", "Hel"),
    ("Kie", "Den"),
    ("Kie", "Mun"),
    ("Kie", "Ruh"),
    ("Mun", "Ruh"),
    ("Mun", "Sil"),
    ("Pru", "Bal"),
    ("Pru", "Lvn"),
    ("Pru", "War"),
    ("Pru", "Sil"),
    ("Ruh", "Bel"),
    ("Ruh", "Hol"),
    ("Sil", "War"),
    ("Apu", "Nap"),
    ("Apu", "Rom"),
    ("Apu", "Ven"),
    ("Apu", "Adr"),
    ("Nap", "Tyn"),
    ("Nap", "Rom"),
    ("Nap", "Ion"),
    ("Pie", "GoL"),
    ("Pie", "Ven"),
    ("Pie", "Tus"),
    ("Rom", "Tyn"),
    ("Rom", "Tus"),
    ("Rom", "Ven"),
    ("Tus", "Tyn"),
    ("Tus", "GoL"),
    ("Tus", "Ven"),
    ("Ven", "Adr"),
    ("Lvn", "Bal"),
    ("Lvn", "Bot"),
    ("Lvn", "StP"),
    ("Lvn", "Mos"),
    ("Lvn", "War"),
    ("Mos", "War"),
    ("Mos", "StP"),
    ("Mos", "Sev"),
    ("Mos", "Ukr"),
    ("Sev", "Rum"),
    ("Sev", "Ukr"),
    ("Sev", "Arm"),
    ("Sev", "Bla"),
    ("StP", "Bot"),
    ("StP", "Fin"),
    ("StP", "Nwy"),
    ("StP", "Bar"),
    ("Ukr", "War"),
    ("Ukr", "Rum"),
    ("Ank", "Con"),
    ("Ank", "Bla"),
    ("Ank", "Arm"),
    ("Ank", "Smy"),
    ("Arm", "Bla"),
    ("Arm", "Syr"),
    ("Arm", "Smy"),
    ("Con", "Aeg"),
    ("Con", "Bul"),
    ("Con", "Bla"),
    ("Con", "Smy"),
    ("Smy", "Aeg"),
    ("Smy", "Syr"),
    ("Smy", "Eas"),
    ("Syr", "Eas"),
    ("Alb", "Adr"),
    ("Alb", "Ser"),
    ("Alb", "Gre"),
    ("Alb", "Ion"),
    ("Bel", "Eng"),
    ("Bel", "Nth"),
    ("Bel", "Hol"),
    ("Bul", "Ser"),
    ("Bul", "Rum"),
    ("Bul", "Bla"),
    ("Bul", "Aeg"),
    ("Bul", "Gre"),
    ("Den", "Hel"),
    ("Den", "Nth"),
    ("Den", "Ska"),
    ("Den", "Swe"),
    ("Den", "Bal"),
    ("Fin", "Bot"),
    ("Fin", "Swe"),
    ("Fin", "Nwy"),
    ("Gre", "Ion"),
    ("Gre", "Ser"),
    ("Gre", "Aeg"),
    ("Hol", "Nth"),
    ("Hol", "Hel"),
    ("Nwy", "Nth"),
    ("Nwy", "Nrg"),
    ("Nwy", "Bar"),
    ("Nwy", "Swe"),
    ("Nwy", "Ska"),
    ("NAf", "Mid"),
    ("NAf", "Wes"),
    ("NAf", "Tun"),
    ("Por", "Mid"),
    ("Por", "Spa"),
    ("Rum", "Bla"),
    ("Rum", "Bul"),
    ("Rum", "Ser"),
    ("Spa", "Mid"),
    ("Spa", "GoL"),
    ("Spa", "Wes"),
    ("Swe", "Ska"),
    ("Swe", "Bot"),
    ("Swe", "Bal"),
    ("Tun", "Wes"),
    ("Tun", "Tyn"),
    ("Tun", "Ion"),
    ("Adr", "Ion"),
    ("Aeg", "Ion"),
    ("Aeg", "Bla"),
    ("Aeg", "Eas"),
    ("Bal", "Bot"),
    ("Bar", "Nrg"),
    ("Eas", "Ion"),
    ("Eng", "Mid"),
    ("Eng", "Iri"),
    ("Eng", "Nth"),
    ("GoL", "Wes"),
    ("GoL", "Tyn"),   
    ("Hel", "Nth"),
    ("Ion", "Tyn"),
    ("Iri", "Mid"),
    ("Iri", "NAt"),
    ("Mid", "NAt"),
    ("Mid", "Wes"),
    ("NAt", "Nrg"),
    ("Nth", "Nrg"),
    ("Nth", "Ska"),
    ("Tyn", "Wes"),
    ("Swi", "Mar"),
    ("Swi", "Bur"),
    ("Swi", "Mun"),
    ("Swi", "Tyr"),
    ("Swi", "Pie"),
]
country_colours ={
    "Austria": "red", #tuple(c/255 for c in (200,143,134)),
    "England": "royalblue", #tuple(c/255 for c in (242,196,227)),
    "France": tuple(c/255 for c in (113,175,196)),#"lightblue",
    "Germany": tuple(c/255 for c in (162,138,118)),#"black",
    "Italy": "green", # tuple(c/255 for c in (161,196,155)),#"
    "Russia": tuple(c/255 for c in (171,126,158)),#"white",
    "Turkey": "yellow", #tuple(c/255 for c in (235,234,179)),#
    "Neutral": tuple(c/255 for c in (229,198,161)),#"navajowhite",
    "sea": tuple(c/255 for c in (194,223,233)),#"aqua",
    "none": tuple(c/255 for c in (0,0,0)),#"dimgrey"

}
G = nx.Graph()

G.add_nodes_from([(key, provinces[key]) for key in provinces])
G.add_edges_from(province_borders)
pos = nx.spring_layout(G, seed=6942069)
# pos['Mun'] = np.array([0,0])
fig, ax =plt.subplots(figsize=(16, 9))
for country in country_colours:
    nodelist = []
    for province in provinces:
        if provinces[province]["home_power"] == country:
            nodelist.append(province)
    nx.draw_networkx_nodes(G, pos, 
                           nodelist=nodelist,
                           node_color=country_colours[country],
                           node_size=2000,
                           edgecolors="black",
                           ax=ax)
 
nx.draw_networkx_edges(G, pos, ax=ax)
# labels_dict= {province: provinces[province]["long_name"] for province in provinces}
nx.draw_networkx_labels(G, pos, ax=ax)
nx.draw_networkx_labels(G, pos, labels={"Swi": "Swi"}, font_color="w", ax=ax)
plt.tight_layout()
ax.axis("off")
plt.savefig("Diplomacy_map_graph.png")
plt.show()