#!/usr/bin/env python

"""
Resolves orders for a given turn
"""
def get_edge(from_province, to_province):
    edge = []
    coast = None
    for province in [from_province, to_province]:
        # assume no provinces with split coast are adjacent
        # True for a standard game 
        
        if "_" in province:
            province, coast = province.split("_")
            if "S" in coast:
                coast = "south"
            elif "N" in caost:
                coast = "north"
        edge.append(province)
    return edge, coast

def move_is_valid(move_order, game_state):
    """
    Check that movement order is valid
    Steps:
        1. Check province is adjacent (include coasts)
        2. Check army (fleet) is not moving to water (inland)
    """
    move_order_split = move_order.split(" ")
    unit_type = move_order_split[0]
    from_province, to_province = move_order_split[1].split("-")
    edge, coast = get_edge(from_province, to_province)
   
    from_province, to_province = edge
    # check if provinces are adjacent
    if to_province not in game_state.G[from_province]:
        return False
    
    # check coasts match
            
    if game_state.G.edges[edge].get("coast") != coast:
        return False
    
    # check fleet not moving across land only border
    if unit_type == "F" and game_state.G.edges[edge].get("land_only"):
        return False

    # check unit not moving to forbidden province type
    if (unit_type == "A" and
        game_state.G.nodes[to_province]["type"] == "water") or\
    (unit_type == "F" and
     game_state.G.nodes[to_province]["type"] == "inland"):
        return False
    
    return True

def order_is_valid(order, game_state):
    """
    Check if order is legal.
    Orders are constructed per unit.
    This implies:
        unit always exists
        from_province is always correct
        Hold orders are always valid
       
    """

    if "Holds" in order:
        return True
    support_order = " S " in order
    convoy_order = " C " in order
    # can't have a support-convoy order
    if not support_order and not convoy_order:
        return move_is_valid(order, game_state)
    elif support_order:
        """
        1. Check province to which support is given is valid
        2. Check if support hold or support move
        If support move:
            1. Check move to support is valid
        """
        support_from, support_to =  order.split(" S ")
        support_unit_type, support_from_province = support_from.split(" ")
        support_to_province = support_to.split("-")[-1]

        if support_to_province not in game_state.G[support_from_province]:
            return False
        
        if not move_is_valid(support_to, game_state):
            return False
        
        edge, coast = get_edge(support_from_province, support_to_province)
        if support_unit_type == "F" and game_state.G.edges[edge].get("land_only"):
            return False
        if (support_unit_type == "A" and
            game_state.G.nodes[support_to_province]["type"] == "water") or\
        (support_unit_type == "F" and
         game_state.G.nodes[support_to_province]["type"] == "inland"):
            return False
        return True
    elif convoy_order:
        convoying_unit, convoyed_unit = order.split(" C ")
        convoying_unit_type, convoying_unit_province = convoying_unit.split(" ")
        if convoying_unit_type != "F":
            # only fleets can convoy
            return False
        if game_state.G.nodes[convoying_unit_province] != "water":
            # cannot convoy from coast
            return False
        convoyed_unit_type, convoyed_unit_order = convoyed_unit.split(" ")
        if convoyed_unit_type != "A":
            # only armies can be convoyed
            return False
        return True



def order_resolver(order_list):
    """
    Function to resolve list of orders.
    """

    pass