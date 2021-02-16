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


# def show_books(books):
#     """ Display all books in a list of Books, or a 'No books' message
#      :param books: the book list """
#
#     if books:
#         print()  # puts blank line before list of books
#         for book in books:
#             print(book)
#         print()  # puts blank line after list of books
#     else:
#         print('\nNo books to display\n')  # \n's add blank line before and after message


def get_artist_by_name():
    """ Create a new Book from title and author provided by user
     :returns: a Book created from the title and author. """
    name = input('Enter artist\'s name: ')
    return name


def get_artist_info():
    """ Create a new Artist from title and author provided by user
     :returns: a Book created from the title and author. """
    name = input('Enter artist\'s name: ')
    email = input('Enter artist\'s email: ')
    return Artist(name, email)


def get_artwork_info(artist_id):
    """ Create a new Book from title and author provided by user
     :returns: a Book created from the title and author. """
    artwork = input('Enter name of artwork: ')
    price = float(input('Enter price of artwork: '))
    # name = input('Who is the artist of this artwork? ')
    return Artwork(artwork, price, artist_id)


def get_artwork_availability():
    while True:
        availability = input('Enter \'yes\' if artwork is for sale or \'no\' if it\'s not: ')
        if availability.lower() in ['yes', 'no']:
            return availability.lower() == 'yes'
        else:
            print('Type \'yes\' or \'no\'')


# def get_book_id():
#     """ Ask for ID, validate to ensure is positive integer
#     :returns: the ID value """
#     while True:
#         try:
#             id = int(input('Enter book ID: '))
#             if id > 0:
#                 return id
#             else:
#                 print('Please enter a positive number.')
#
#         except ValueError:
#             print('Please enter a number.')


def ask_question(question):
    """ Ask user question
    :param: the question to ask
    :returns: user's response """
    return input(question)
