import requests
import itertools

NRDB = 'http://netrunnerdb.com/'

def get_cards():
    '''
    Pull a list of all cards from nrdb.
    '''
    return requests.get("{}/api/cards/".format(NRDB)).json()

def get_attribute_list(cards):
    '''
    List all keys (attributes) belonging to any card in the JSON card
    list (e.g. cost, strength, memory units, ancur links, artist, etc.)
    '''

if __name__ == '__main__':
    pass
