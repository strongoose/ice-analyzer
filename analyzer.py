import sys
reload(sys)
sys.setdefaultencoding('utf8')

import requests
import itertools
import csv

NRDB = 'http://netrunnerdb.com/'


def get_cards_list():
    '''
    Pull a list of all cards from nrdb.
    '''
    return [card for card in
            requests.get("{}/api/cards/".format(NRDB)).json()]

def get_attribute_list(cards):
    '''
    List all keys (attributes) belonging to any card in the JSON card
    list (e.g. cost, strength, memory units, ancur links, artist, etc.)
    '''
    return sorted(
        list(set(itertools.chain(*[card.keys() for card in cards]))))

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
    Take a cards dictionary and adds a seperate attribute for each
    subroutine, leaving the original 'text' attribute intact. No return
    value; modifies the dictionary in place.
    '''
    for ice in ice_list:
        subs = get_subs(ice)
        for index in range(0, len(subs)):
            ice["subroutine{}".format(index + 1)] = subs[index]

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

def write_to_csv(ice_list, output):
    '''
    Write ice_list to output as a table with a column for each possible
    attribute (as agglomerated by get_attrubute_list(ice_list).

    If the attribute doesn't exist for a given ice, write an empty
    string.
    '''

    def attr_or_blank(dictionary, attribute):
        '''
        Return the value corresponding to attribute in dictionary, or a
        blank string if it doesn't exist.
        '''
        if attribute in dictionary:
            return dictionary[attribute]
        else:
            return ""

    with open(output, 'w') as csv_output:
        writer = csv.writer(csv_output)

        attributes = get_attribute_list(ice_list)
        writer.writerow(attributes)

        for ice in ice_list:
            writer.writerow([
                attr_or_blank(ice, attribute)
                for attribute in attributes
                ])


if __name__ == '__main__':

    cards = get_cards_list()

    explode_subs(cards)

    explode_on_encounter(cards)

    write_to_csv(cards, "output.csv")
