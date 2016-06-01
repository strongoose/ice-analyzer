import requests
import itertools

NRDB = 'http://netrunnerdb.com/'

def get_ice_list():
    '''
    Pull a list of all cards from nrdb.
    '''
    return [
        card for card in requests.get("{}/api/cards/".format(NRDB)).json()
        if card["type"] == "ICE"
        ]

def get_attribute_list(cards):
    '''
    List all keys (attributes) belonging to any card in the JSON card
    list (e.g. cost, strength, memory units, ancur links, artist, etc.)
    '''
    return sorted(
        list(set(itertools.chain(*[card.keys() for card in cards]))))

def write_to_csv(cards, csv_file):
    pass

def get_subs(ice):
    '''
    Return the list of subroutines of a piece of ice.
    '''
    return [line for line in ice["text"].split("\n")
            if line.startswith("[Subroutine]")]

def get_on_encounter(ice):
    return [line for line in ice["text"].split("\n")
            if line.startswith("When the Runner encounters")]

def explode_subs(ice_list):
    '''
    Take a cards dictionary and adds the same number of subroutine
    attributes to all of them (equal to the max possible number of subs.
    Extra sub fields are blank. Modifies dictionary in place.
    '''
    most_subs = max([len(get_subs(ice)) for ice in ice_list])
    for ice in ice_list:
        subs = get_subs(ice)
        for index in range(0, most_subs):
            if index < len(subs):
                ice["subroutine{}".format(index + 1)] = subs[index]
            else:
                ice["subroutine{}".format(index + 1)] = ""

def explode_on_encounter(ice_list):
    '''
    Set an on_encounter_effect attribute on each ice in the list. This
    does assume that each ice only has one on encounter effect, which is
    true to date and seems likely to remain true (famous last words?).
    '''
    for ice in ice_list:
        on_encounter = get_on_encounter(ice)
        if on_encounter:
            ice["on_encounter_effect"] = on_encounter[0]
        else:
            ice["on_encounter_effect"] = ""


if __name__ == '__main__':

    ices = get_ice_list()

    explode_subs(ices)

    explode_on_encounter(ices)

    # write to csv file
