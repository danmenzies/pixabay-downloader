# Collects the required info for a Pixabay search, and prints
# the number of expected results

from slugify import slugify
from modules.Pixabay import Pixabay

def download_images():
    """
    Collects the required info for a Pixabay search, and prints
    the number of expected results
    :return:
    """

    # Collect the search term and parameters from the user
    term = input("Image search term: ")
    orientation = input("Image orientation > [a]ll, [h]orizontal, [v]ertical: ")
    search_type = input("Image type > [a]ll, [p]hoto, [i]llustration, [v]ector: ")
    colors = input("Colors (optional): ")
    category = input("Narrow by image category (optional): ")
    min_width = input("Minimum image width (optional): ")
    min_height = input("Minimum image height (optional): ")

    # Instantiate the Pixabay image grabber
    pixabay = Pixabay()

    # Collect a list of images
    pixabay.save_search_results(
        term=term,
        orientation=orientation,
        category=category,
        min_width=min_width,
        min_height=min_height,
        search_type=search_type,
        colors=colors
    )

    # Start downloading
    pixabay.download_results(
        slugified_term=slugify(str(term).strip())
    )


# Fire the main entry point
if __name__ == '__main__':
    download_images()