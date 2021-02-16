from artwork_store import ArtworkStore
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
    # menu.add_option('2', 'See All Artist\'s Artwork', see_all_artist_artwork)
    # menu.add_option('3', 'See Artist\'s Available Artwork', see_artist_available_artwork)
    menu.add_option('4', 'Add Artist\'s Artwork', add_artwork)
    # menu.add_option('5', 'Delete Artwork', delete_artwork)LilLilL000
    menu.add_option('6', 'Change Artwork Availability Status', change_availability)
    menu.add_option('Q', 'Quit', quit_program)

    return menu


def add_artist():
    new_artist = ui.get_artist_info()
    try:
        new_artist.insert_artist()
    except:
        print('This artist is already in the database.')


def add_artwork():
    artist_name = ui.get_artist_by_name()
    get_artist_id = ArtworkStore()._get_artist_id(artist_name)
    new_artwork = ui.get_artwork_info(get_artist_id)
    new_artwork.insert_artwork()


def change_availability():
    pass
    ##TODO


def quit_program():
    ui.message('Thanks for checking out the store!')


if __name__ == '__main__':
    main()
