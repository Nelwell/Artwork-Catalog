from menu import Menu
import ui


def main():
    menu = create_menu()

    while True:
        choice = ui.display_menu_get_choice(menu)
        action = menu.get_action(choice)
        action()
        if choice == 'Q':
            break


def create_menu():
    menu = Menu()
    menu.add_option('1', 'Add Artist', add_artist)
    # menu.add_option('2', 'Search For Book', search_book)
    # menu.add_option('3', 'Show Unread Books', show_unread_books)
    # menu.add_option('4', 'Show Read Books', show_read_books)
    # menu.add_option('5', 'Show All Books', show_all_books)
    # menu.add_option('6', 'Change Book Read Status', change_read)
    # menu.add_option('7', 'Delete Book', delete_book)
    menu.add_option('Q', 'Quit', quit_program)

    return menu


def add_artist():
    new_artist = ui.get_artist_info()
    try:
        new_artist.insert_artist()
    except:
        print('This artist is already in the database.')


def quit_program():
    ui.message('Thanks and bye!')


if __name__ == '__main__':
    main()
