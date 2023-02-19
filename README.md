# Youtube-Word-Finder

Searches a specific said word or phrase within all videos of a YouTube Channel.

Utilizes the auto-generated or written subtitles for that purpose.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.

```bash
pip install -r requirements.txt
```

## Usage
Run the script `wordFinder.py` using the following command line arguments.

`python3 wordFinder.py "<WORD|PHRASE>" <YT-CHANNEL-ID> <DEPTH>`

**Stores search result** in the `results` folder. Result files are JSON formatted.

**WORD | PHRASE**
>The said phrase or the word you want to search for in the subtitles.
>
>**Make sure** to put quotation marks "" around the word or phrase.

**YT CHANNEL ID**
> The channel ID of the YouTube channel you want to search in.
> 
> Can be obtained using sites like: 
> https://www.streamweasels.com/tools/youtube-channel-id-and-user-id-convertor/

**DEPTH**
>Defines how many videos should be scanned. The factor is x100.
>
>This means that with a DEPTH of 3 the 300 newest videos on the channel will be scanned for the WORD or PHRASE.


## How it works

1. Gathers all video IDs of the channel until the specified DEPTH and caches them in the `id_cache` folder for quicker access next time,
2. Divides the acquired video-id list into chunks for multiprocessing
3. Goes through every video and downloads the subtitles using the [YouTube-Transcript-API](https://github.com/jdepoix/youtube-transcript-api), also caches them into the `cache` folder.
4. Searches the transcript for the given WORD or PHRASE and returns the timestamp when found
5. Stores results in the `results` folder in the JSON format for further use.

## Credits

* [YouTube-Transcript-API](https://github.com/jdepoix/youtube-transcript-api) - Used for gathering the subtitles of the videos
* [YouTube-Search-Python](https://github.com/alexmercerind/youtube-search-python) - Used for gathering the video-ids
* [NumPy](https://numpy.org/) - Used for calculations for handling multiprocessing

## License

[GPL v3.0](https://github.com/oskarkraemer/youtubeWordFinder/blob/main/LICENSE)
