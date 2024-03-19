#!/usr/bin/env python

import json

import networkx as nx

from orders import resolver
from units import Army, Fleet

class GameState:
    def __init__(self, game_id, turn) -> None:
        self.game_id = game_id
        self.turn = turn
        self.G, self.units = self.get_map_state()

    def get_map_state(self):
        if self.turn == 0:
            with open("map_state_turn_000.json", "r") as f:
                g_data = json.load(f)
            G = nx.node_link_graph(g_data)
            units = {
                "Austria":
                    [Army("Austria", "Vie"),
                    Army("Austria", "Bud"),
                    Fleet("Austria", "Tri")],
                "England": 
                    [Fleet("England", "Lon"),
                    Fleet("England", "Edi"),
                    Army("England", "Liv")],
                "France":
                    [Army("France", "Par"),
                    Army("France", "Mar"),
                    Fleet("France", "Bre")],
                "Germany":
                    [Army("Germany", "Ber"),
                    Army("Germany", "Mun"),
                    Fleet("Germany", "Kie")],
                "Italy":
                    [Army("Italy", "Rom"),
                    Army("Italy", "Ven"),
                    Fleet("Italy", "Nap")],
                "Russia":
                    [Army("Russia", "Mos"),
                    Fleet("Russia", "Sev"),
                    Army("Russia", "War"),
                    Fleet("Russia", "StP", coast="south")],
                "Turkey":
                    [Fleet("Turkey", "Ankara"),
                    Army("Turkey", "Con"),
                    Army("Turkey", "Smy"),]
            }
            return G, units
        else:
            with open(f"game_id_{self.game_id}_map_state_turn_"+f"{self.turn-1}".zfill(3)+".json", "r") as f:
                gamestate_data = json.load(f)
            g_data = gamestate_data["game_map"]
            G = nx.node_link_graph(g_data)
            units = gamestate_data["units"]

def get_orders(units):
    pass

if __name__ == "__main__":
    initial_game_state = GameState(0,0)
    order_list = get_orders(initial_game_state.units)
    new_positions = resolver(order_list)
