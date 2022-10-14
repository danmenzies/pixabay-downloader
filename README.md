# Pixabay mass-image downloader

Pulls images from Pixabay based on a search term, then saves them to a local folder (along with credits).



## Setup

1. Install Python 3.6 or higher
2. Run `pip install -r requirements.txt`
3. Copy the `./config/.env.example` file to `./config/.env`
4. Add your [Pixabay API key](https://pixabay.com/api/docs/) to the `PIXABAY_API_KEY` variable in `./config/.env`

## Usage

### `search.py`

Get an idea of how many images a download will pull, for a specific search term. Note the maximum number of images returned 
via the API is 500 (even if there are thousands of results on the site).

```bash
python search.py

"Image search term: " landcapes at night
"Image orientation > [a]ll, [h]orizontal, [v]ertical:" h
"Narrow by image category (optional):" nature
"Minimum image width (optional):" 1920
"Minimum image height (optional):" 1080 
"Image type > [a]ll, [p]hoto, [i]llustration, [v]ector:" p
```

Result:

```text
Found 162 images
```

### `download.py`

Downloads images from Pixabay and saves them to the `./data/{search-term}` folder (eg, `./data/landcapes-at-night`).

```bash
python download.py

"Image search term: " landcapes at night
"Image orientation > [a]ll, [h]orizontal, [v]ertical:" h
"Narrow by image category (optional):" nature
"Minimum image width (optional):" 1920
"Minimum image height (optional):" 1080 
"Image type > [a]ll, [p]hoto, [i]llustration, [v]ector:" p
```

Result

```text
Collecting image data from Pixabay...
 - Page 1 collected
 - Page 2 collected
 - Page 3 collected

Downloading individual images...
 - Saved hd-wallpaper-nature-wallpaper-ocean-3605547.jpg
 - Saved aurora-northern-lights-1197753.jpg
 - Saved wolf-moon-tree-silhouettes-howl-647528.jpg
 - Saved forest-fog-woods-trees-mystical-3394066.jpg
 - Saved night-forest-glowworm-light-3078326.jpg 
 [...]
 - Saved birds-little-birds-animals-2037456.png
 - Saved nebula-milky-way-night-sky-stars-2785204.jpg
 - Saved halloween-witch-spell-bats-2033906.png
 - Saved hd-wallpaper-nature-wallpaper-tree-1551106.jpg

Downloads completed
```

Along with the images, a `__credits.csv` file is also saved to the folder, containing the image credits; and a 
`__results.json` file, containing the raw API image information.

## Categories

The following categories are available via the Pixabay API:

* `backgrounds`
* `fashion`
* `nature`
* `science`
* `education`
* `feelings`
* `health`
* `people`
* `religion`
* `places`
* `animals`
* `industry`
* `computer`
* `food`
* `sports`
* `transportation`
* `travel`
* `buildings`
* `business`
* `music`

## Personal Notes

This is a personal tool that I thought might be helpful. It's not meant to be a full-featured application, but rather a 
simple script that can be used to download images from Pixabay. **Pull requests are welcome**, but I'm not actively 
maintaining this project.

Please also note, that while I am a Software Engineer, I'm not a *Python-focused* Software Engineer in any way (most of
what I do is [focused around WordPress](https://profiles.wordpress.org/psdtofinal/#content-plugins). I'm sure there are 
better ways to do things, and constructive feedback is welcome (especially when it comes to structuring the project).

Thanks for checking it out :)