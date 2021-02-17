from artist import Artist
from artwork import Artwork


def display_menu_get_choice(menu):
    """ Displays all of the menu options, checks that the user enters a valid choice and returns the choice.
     :param menu: the menu to display
     :returns: the user's choice """
    while True:
        print(menu)
        choice = input('Enter choice? ').upper() # makes the quit option case insensitive
        if menu.is_valid(choice):
            return choice
        else:
            print('Not a valid choice, try again.')


def message(msg):
    """ Prints a message for the user
     :param msg: the message to print"""
    print(msg)


def show_artworks_by_artist(artworks):
    """ Display all artworks in a list of Artworks, or a 'No artworks' message
     :param artworks: the artwork list """

    if artworks:
        print()  # puts blank line before list of artworks
        for art in artworks:
            print(art)
        print()  # puts blank line after list of artworks
    else:
        print('\nNo artworks to display\n')  # \n's add blank line before and after message


def get_artist_name():
    """ Gets name of Artist from user
     :returns: an Artist name based on given input. """
    name = input('Enter artist\'s name: ')
    return name


def get_artwork_name():
    """ Gets name of Artwork from user
     :returns: an Artwork name based on given input. """
    artwork_name = input('Enter name of artwork: ')
    return artwork_name


def get_artist_info():
    """ Create a new Artist from name and email provided by user
     :returns: an Artist created from the name and email. """
    name = input('Enter artist\'s name: ')
    email = input('Enter artist\'s email: ')
    return Artist(name, email)


def get_artwork_info(artist_id):
    """ Create a new Artwork from artwork name and price provided by user
     :returns: an Artwork created from the artwork name and price. """
    artwork = input('Enter name of artwork: ').title()
    price = float(input('Enter price of artwork: '))
    return Artwork(artwork, price, artist_id)


def get_artwork_availability():
    while True:
        availability = input('Enter \'yes\' if artwork is for sale or \'no\' if it\'s not: ')
        if availability.lower() in ['yes', 'no']:
            return availability.lower() == 'yes'
        else:
            print('Type \'yes\' or \'no\'')


def ask_question(question):
    """ Ask user question
    :param: the question to ask
    :returns: user's response """
    return input(question)
