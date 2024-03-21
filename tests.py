import json
import unittest

import networkx as nx

from orders import order_is_valid
from game_state import GameStateFromInputs
from units import Army, Fleet

class TestOrderValidator(unittest.TestCase):

    def test_army_movement(self):
        with open("map_state_turn_000.json", "r") as f:
            g_data = json.load(f)
        G = nx.node_link_graph(g_data)
        army = Army("France", "Par")
        game_state = GameStateFromInputs(G, [army])
        self.assertTrue(order_is_valid(army.move("Bre"), game_state))
        self.assertFalse(order_is_valid(army.move("Mar"), game_state))
        self.assertFalse(order_is_valid(army.move("Eng"), game_state))

    def test_fleet_movement(self):
        with open("map_state_turn_000.json", "r") as f:
            g_data = json.load(f)
        G = nx.node_link_graph(g_data)
        fleets = [Fleet("England", "Eng"), Fleet("Italy", "Rom"), Fleet("Austria", "Tri")]
        game_state = GameStateFromInputs(G, fleets)
    
        self.assertTrue(order_is_valid(fleets[0].move("Bre"), game_state))
        self.assertTrue(order_is_valid(fleets[0].move("Iri"), game_state))
        self.assertFalse(order_is_valid(fleets[0].move("NAt"), game_state))

        self.assertTrue(order_is_valid(fleets[1].move("Tus"), game_state))
        self.assertTrue(order_is_valid(fleets[1].move("Tyn"), game_state))
        self.assertFalse(order_is_valid(fleets[1].move("Ven"), game_state))
        self.assertFalse(order_is_valid(fleets[1].move("Apu"), game_state))

        self.assertFalse(order_is_valid(fleets[2].move("Vie"), game_state))

    def test_support(self):
        with open("map_state_turn_000.json", "r") as f:
            g_data = json.load(f)
        G = nx.node_link_graph(g_data)
        units = [Army("France", "Gas"),
                 Army("France", "Mar"),
                 Army("Germany", "Sil"),
                 Fleet("Germany", "Bal")]
        game_state = GameStateFromInputs(G, units)
        self.assertTrue(order_is_valid(units[0].support(units[1].move("Bur")), game_state))
        self.assertFalse(order_is_valid(units[0].support(units[1].move("Pie")), game_state))
        self.assertTrue(order_is_valid(units[3].support(units[2].move("Pru")), game_state))

if __name__ == "__main__":
    unittest.main()