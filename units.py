#!/usr/bin/env python

import functools

class Unit:
    """
    Base class for game units. 
    Need to know: 
        - who it belongs to: `home_power`
        - where it is: `current_province`
        - what it should do:  `order`

    example order outputs:
    Hold: F London Holds
    Move: A Paris-Burgundy
        (Army Paris move to Burgundy)
    Support: A Par S A Mar-Bur
        (Army Paris support army Marseille to Burgundy)
    Convoy: F Bla C A Ank-Sev 
        (Fleet Black Sea convoy army Ankara to Sevastopol)
    """
    def __init__(self, home_power, current_province):
        self.home_power = home_power
        self.current_province = current_province
    
    def __repr__(self):
        return f"Unit at {self.current_province}"

    def to_output(self):
        return {"type":self.type, 
                "home_power":self.home_power,
                "current_province": self.current_province}

    def base_order(order):
        @functools.wraps(order)
        def wrapper(*args, **kwargs):
            self = args[0]
            order_prefix = f"{self.type} {self.current_province}"
            return order_prefix + order(*args)
        return wrapper

    @base_order
    def hold(self):
        order_string = " Holds"
        return order_string

    @base_order
    def move(self, to_province, retreat=False):
        # retreat is a special case of move
        order_string = f"-{to_province}"
        return order_string

    @base_order
    def support(self, order):
        # some sort of wrapper for hold and move orders
        order_to_support = order
        order_string = f" S " + order_to_support 
        return order_string

    @base_order
    def convoy(self, movement):
        order_string = f" C " + movement
        return order_string

class Army(Unit):
    def __init__(self, home_power, current_province):
        Unit.__init__(self, home_power, current_province)
        self.type = "A"
        self.allowed_province_types = ["inland", "coastal"]
    
    def __repr__(self):
        return f"Army at {self.current_province}"

class Fleet(Unit):
    def __init__(self, home_power, current_province, coast=None):
        Unit.__init__(self, home_power, current_province)
        self.type = "F"
        # self.coast = coast
        if coast == "south":
            self.current_province = current_province + " SC"
        elif coast == "north":
            self.current_province = current_province + " NC"
        else:
            pass
        self.allowed_province_types = ["water", "coastal"]
    
    def __repr__(self):
        return f"Fleet at {self.current_province}"
    
def unit_from_gamestate(unit_dict):
    if unit_dict["type"] == "A":
        return Army(unit_dict["home_power"], unit_dict["current_province"])
    if unit_dict["type"] == "F":
        province = unit_dict["current_province"].split(" ")
        if len(province) == 2:
            coast = province[1][0]
            if coast == "S":
                coast = "south"
            elif coast == "N":
                coast = "north"
            else:
                coast = None
            return Fleet(unit_dict["home_power"], province[0], coast=coast)
        return Fleet(unit_dict["home_power"], unit_dict["current_province"])