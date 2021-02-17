from artwork_store import ArtworkStore
from menu import Menu
import ui
from artwork import Artwork

artwork_store = ArtworkStore()
artist_artwork = Artwork(artwork='', price=float, artist_id=int, for_sale=True)


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
    menu.add_option('2', 'See All Artist\'s Artwork', show_all_artist_artwork)
    menu.add_option('3', 'See Artist\'s Available Artwork', show_artist_available_artwork)
    menu.add_option('4', 'Add Artist\'s Artwork', add_artwork)
    # menu.add_option('5', 'Delete Artwork', delete_artwork)
    menu.add_option('6', 'Change Artwork Availability Status', change_availability)
    menu.add_option('Q', 'Quit', quit_program)

    return menu


def add_artist():
    new_artist = ui.get_artist_info()
    try:
        new_artist.insert_artist()
    except:
        print('This artist is already in the database.')


def show_all_artist_artwork():
    artist_name = ui.get_artist_name()
    artist_id = artwork_store._get_artist_id(artist_name)
    artworks = artist_artwork.get_all_artist_artwork(artist_id)
    ui.show_artworks_by_artist(artworks)


def show_artist_available_artwork():
    artist_name = ui.get_artist_name()
    artist_id = artwork_store._get_artist_id(artist_name)
    artworks = artist_artwork.get_all_artist_available_artwork(artist_id)
    ui.show_artworks_by_artist(artworks)

def add_artwork():
    try:
        artist_name = ui.get_artist_name()
        artist_id = artwork_store._get_artist_id(artist_name)
        new_artwork = ui.get_artwork_info(artist_id)
        new_artwork.insert_artwork()
    except:
        print('\nNo artist found with that name in the Artwork Store database. Please add this artist first.\n')


def change_availability():
    artist_name = ui.get_artist_name()
    artist_id = artwork_store._get_artist_id(artist_name)
    # artworks = artist_artwork.get_all_artist_artwork(artist_id)
    # artwork_name = ui.get_artwork_name()
    artwork_object = artist_artwork.get_artwork_by_id(artist_id)
    if artwork_object:  # If artwork ID found in db
        availability_status = ui.get_artwork_availability()
        # if else statement to determine if for sale or not
        if not availability_status:
            sale_status = '"Sold"'
        else:
            sale_status = '"For Sale"'
        artwork_object.for_sale = availability_status
        artwork_object.update_artwork()
        print('Artwork status has changed to', sale_status)
    else:  # If artwork ID not found in db
        print('That artwork is not found.')
        option = input('Return to main menu? Y for main menu or Enter to quit. ').upper()
        if option == 'Y':
            print()
        else:
            quit_program()


def quit_program():
    ui.message('Thanks for checking out the store!')


if __name__ == '__main__':
    main()
