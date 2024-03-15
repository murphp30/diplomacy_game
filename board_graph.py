#!/usr/bin/env python
import re
import string

import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.patches as patches
import numpy as np

from matplotlib.path import Path
from PIL import Image
from shapely.geometry import GeometryCollection, LineString, Polygon
from xml.dom import minidom

def svg_parse(path):
      """
      Stolen from https://gis.stackexchange.com/a/301682
      """
      commands = { 'M' : (Path.MOVETO,),   'L' : (Path.LINETO,),
                   'Q' : (Path.CURVE3,)*2, 'C' : (Path.CURVE4,)*3,
                   'Z' : (Path.CLOSEPOLY,) }
      path_re = re.compile(r'([MLHVCSQTAZ])([^MLHVCSQTAZ]+)', re.IGNORECASE)
      float_re = re.compile(r'(?:[\s,]*)([+-]?\d+(?:\.\d+)?)')
      vertices = []
      codes = []
      last = (0,0)
      for cmd, values in path_re.findall(path):
          points = [float(v) for v in float_re.findall(values)]
          points = np.array(points).reshape((len(points)//2,2))
          if cmd in string.ascii_lowercase:
              points += last
          cmd = cmd.capitalize()
          last = points[-1]
          codes.extend( commands[cmd] )
          vertices.extend( points.tolist() )
      return codes, vertices

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
province_positions = {
    'Boh': (566.3279569892474, 595.459595959596),
    'Bud': (662.7795698924732, 679.8751803751804),
    'Gal': (700.5215053763442, 608.446608946609),
    'Tri': (581.704301075269, 715.2287157287158),
    'Tyr': (531.3817204301076, 646.6861471861472),
    'Vie': (604.0698924731183, 635.8636363636364),
    'Cly': (314.7150537634409, 347.9848484848485),
    'Edi': (335.6827956989248, 381.8953823953824),
    'Lvp': (323.80107526881727, 441.0584415584416),
    'Lon': (343.3709677419356, 494.4494949494949),
    'Wal': (308.42473118279577, 477.1334776334776),
    'Yor': (346.16666666666674, 436.0079365079365),
    'Bre': (258.80107526881727, 561.5490620490621),
    'Bur': (400.6827956989248, 636.5851370851371),
    'Gas': (297.241935483871, 678.4321789321789),
    'Mar': (371.32795698924735, 714.507215007215),
    'Par': (367.13440860215064, 597.6240981240982),
    'Pic': (364.3387096774194, 562.2705627705628),
    'Ber': (546.7580645161291, 500.94300144300144),
    'Kie': (497.83333333333337, 482.90548340548344),
    'Mun': (504.1236559139786, 614.9401154401155),
    'Pru': (615.951612903226, 492.2849927849928),
    'Ruh': (449.60752688172056, 562.9920634920635),
    'Sil': (587.9946236559141, 543.5115440115441),
    'Apu': (561.4354838709678, 807.5808080808081),
    'Nap': (553.0483870967743, 831.3903318903319),
    'Pie': (445.41397849462373, 699.3556998556999),
    'Rom': (505.5215053763442, 793.8722943722944),
    'Tus': (484.5537634408603, 760.6832611832613),
    'Ven': (502.72580645161304, 695.0266955266956),
    'Lvn': (710.3064516129033, 434.56493506493507),
    'Mos': (927.6720430107529, 433.8434343434343),
    'Sev': (871.7580645161291, 632.2561327561327),
    'StP': (786.4892473118281, 327.0613275613275),
    'Ukr': (787.8870967741937, 578.1435786435786),
    'War': (655.0913978494625, 534.1320346320347),
    'Ank': (936.7580645161291, 816.9603174603175),
    'Arm': (1127.5645161290322, 824.8968253968254),
    'Con': (798.3709677419356, 809.7453102453103),
    'Smy': (799.7688172043012, 902.0974025974026),
    'Syr': (1146.4354838709678, 942.501443001443),
    'Alb': (644.6075268817206, 822.0108225108225),
    'Bel': (395.79032258064524, 531.9675324675325),
    'Bul': (707.5107526881721, 775.8347763347763),
    'Den': (532.0806451612904, 440.3369408369408),
    'Fin': (708.209677419355, 258.51875901875906),
    'Gre': (713.1021505376345, 897.0468975468975),
    'Hol': (414.6612903225807, 508.8795093795094),
    'Nwy': (532.0806451612904, 304.6948051948052),
    'NAf': (188.2096774193549, 951.1594516594516),
    'Por': (77.77956989247318, 749.8607503607504),
    'Rum': (753.6397849462367, 730.3802308802309),
    'Ser': (656.4892473118281, 753.468253968254),
    'Spa': (179.8225806451613, 756.3542568542568),
    'Swe': (620.8440860215055, 324.17532467532465),
    'Tun': (430.7365591397851, 928.0714285714286),
    'Adr': (571.220430107527, 774.391774891775),
    'Aeg': (747.3494623655915, 898.4898989898991),
    'Bal': (613.8548387096776, 439.61544011544015),
    'Bar': (835.4139784946238, 36.296536796536884),
    'Bla': (892.725806451613, 737.5952380952381),
    'Eas': (861.97311827957, 974.9689754689755),
    'Eng': (283.9623655913979, 526.1955266955267),
    'Bot': (651.5967741935485, 337.1623376623377),
    'GoL': (359.44623655913983, 777.2777777777778),
    'Hel': (459.39247311827967, 453.32395382395384),
    'Ion': (596.3817204301076, 943.9444444444445),
    'Iri': (220.36021505376348, 482.90548340548344),
    'Mid': (65.19892473118281, 617.8261183261184),
    'NAt': (97.34946236559145, 267.17676767676767),
    'Nth': (400.6827956989248, 391.2748917748918),
    'Nrg': (453.10215053763454, 136.58513708513703),
    'Ska': (509.715053763441, 362.41486291486297),
    'Tyn': (479.6612903225807, 837.8838383838383),
    'Wes': (303.5322580645162, 854.478354978355),
    'Swi': (450.3064516129033, 653.9011544011544)
}
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
# game_map = minidom.parse("standard.svg")

# province_svg_paths = [
#     path.getAttribute('d') for path in game_map.getElementsByTagName('path')
# ]
# path_ids = [
#     path.getAttribute('id') for path in game_map.getElementsByTagName('path')
# ]
# game_map.unlink()
# polys = []
# for i, province_svg_path in enumerate(province_svg_paths):
#     codes, verts = svg_parse(province_svg_path)
#     mpl_path = Path(verts, codes)
#     poly = mpl_path.to_polygons()
#     if len(poly) == 0:
#         print(f"{path_ids[i]} is a line")
#         polys.append(LineString(mpl_path.vertices))
#     else:
#         polys.append(Polygon(poly[0]))
# multi_poly = GeometryCollection(polys)

img = Image.open("map.png")
game_map = np.array(img)
game_map[np.where(game_map <= 1)] = 0
game_map[np.logical_and((game_map > 1), (game_map < 59))] = 1
game_map[np.where(game_map >= 59)] = 2

fig = plt.figure(1, frameon=False, figsize=(1300/100, 1000/100), dpi=100)
ax = fig.add_axes([0, 0, 1, 1])
ax.axis('off')
# plt.figure(figsize=(1300/100, 1000/100), dpi=100, frameon=False)
ax.imshow(game_map, cmap="magma", aspect="auto")
# plt.gca().set_axis_off()
# plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
#             hspace = 0, wspace = 0)
# plt.axis("off")
# plt.margins(0,0)
# plt.gca().xaxis.set_major_locator(plt.NullLocator())
# plt.gca().yaxis.set_major_locator(plt.NullLocator())
# plt.tight_layout()
fig.savefig("map_recolour.png", transparent=True, bbox_inches = 'tight', pad_inches = 0, dpi=100)
G = nx.Graph()

G.add_nodes_from([(key, provinces[key]) for key in provinces])
G.add_edges_from(province_borders)
pos = nx.spring_layout(G, seed=6942069)
# pos = {province: (pos_coord[0], -pos_coord[1]) for province, pos_coord in province_positions.items()}
for province, pos_coord in province_positions.items():
    pos[province] = (pos_coord[0], -pos_coord[1])
# pos['Mun'] = np.array([0,0])
fig, ax = plt.subplots(figsize=(16, 9))
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

# p = gpd.GeoSeries(polys)
# p.plot(facecolor="w", edgecolor='k')
# plt.close("all")
plt.show()
# fig = plt.figure(figsize=(12,9))
# ax = fig.add_subplot(111)
# ax.imshow(game_map, origin="upper", cmap="magma", aspect="auto")

# coords = []

# def onclick(event):
#     global ix, iy
#     ix, iy = event.xdata, event.ydata
#     print (f'x = {ix}, y = {iy}')

#     global coords
#     coords.append((ix, iy))
    
#     if len(coords) == len(provinces):
#         fig.canvas.mpl_disconnect(cid)

#     return coords
# cid = fig.canvas.mpl_connect('button_press_event', onclick)
# plt.show()