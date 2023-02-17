from youtube_transcript_api import YouTubeTranscriptApi
from youtubesearchpython import *
import random
import webbrowser
import time
import math
import multiprocessing as mp
import numpy
import json

from sys import argv, exit

#Own modules
import cache
import logger

pietsmiet_id = "UCqwGaUvq_l0RKszeHhZ5leA"
my_id = "UCSEo8hOjRRkbh549h4qfjGg"

yt_id_en = "3MOgiF_TIEI"
yt_id_de = "F7xygLAk2X0"

lg = logger.Logger()
lg.enabled = True


def get_video_ids(channel_id, depth):
    #Check if needed ids are already cached?
    if cache.id_cache_available(channel_id, depth) > 0:
        return cache.load_ids(channel_id, depth)

    counter = 0
    playlist = Playlist(playlist_from_channel_id(channel_id))

    lg.print_log(f'Videos Retrieved: {len(playlist.videos)}')

    while playlist.hasMoreVideos and counter <= depth:
        lg.print_log('Getting more videos...')
        playlist.getNextVideos()
        lg.print_log(f'Videos Retrieved: {len(playlist.videos)}')
        
        counter += 1

    lg.print_log('Found all the videos.')

    #Get list with ids
    ids = []

    for video in playlist.videos:
        ids.append(video["id"])
    
    #Cache ids
    cache.save_ids(ids, channel_id, depth)

    return ids



# ----
#Subtitles
# ----

def is_language_available(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        is_de = False
        for t in transcript_list:
            if t.language_code == "de":
                is_de = True
        
        return is_de
    except:
        return False


def get_subtitle(video_id):
    if cache.subtitle_cache_available(video_id):
        lg.print_log("Is cached!")
        return cache.load_subtitle(video_id)

    if not is_language_available(video_id):
        return
    
    subtitle = YouTubeTranscriptApi.get_transcript(video_id, languages=['de'])

    #Cache subtitle
    cache.save_subtitle(subtitle, video_id)

    return subtitle


def download_subtitles(channel_id, amount):
    lg.print_log("[Downloading subtitles]")

    ids = get_video_ids(channel_id, math.ceil(amount / 100))

    for i in range(amount):
        get_subtitle(ids[i])
        lg.print_log("Downloaded: " + str(i) + " / " + str(amount))
    
# ----
# Search
# ----

def search_words_video(words, video_id, exact = False):
    start_whole = time.time()

    start_sub = time.time()
    subtitle = get_subtitle(video_id)
    end_sub = time.time()

    occ = []

    if subtitle == None:
        return []
    
    if len(words.split()) > 1:
        exact = False

    start_search = time.time()
    for part in subtitle:
        if exact:
            if words in part["text"].split():
                occ.append(part)
        else:
            if words in part["text"]:
                occ.append(part)
    
    end_search = time.time()
    
    end_whole = time.time()

    lg.print_log("Getting subs took: " + str(end_sub - start_sub) + "s")
    lg.print_log("Searching took: " + str(end_search - start_search) + "s")
    lg.print_log(" ---> Everything took: " + str(end_whole - start_whole) + "s")
    return occ


def _search_words_videos(parameter_data):
    found_words = []
    cache.LOADED_SUBTITLES = parameter_data[2]

    for counter, video_id in enumerate(parameter_data[1]):
        lg.set_box(True)
        lg.print_log("   [" + str(counter) + "]   ")

        found = {"video_id": video_id, "keys": search_words_video(parameter_data[0], video_id, True)}

        if len(found["keys"]) != 0:
            found_words.append(found)

        lg.print_log(found)
        lg.set_box(False)
    
    return found_words

# ----
# Multiprocessing
# ----

def run_search_async(words, channel_id, depth, save = True):
    ids = get_video_ids(channel_id, depth)

    print("--------------")
    id_chunks = numpy.array_split(ids, mp.cpu_count())

    parameter_data = []
    for i in id_chunks:
        parameter_data.append([words, list(i), cache.LOADED_SUBTITLES])
    

    pool = mp.Pool(mp.cpu_count())
    result = pool.map(_search_words_videos, parameter_data)
    

    #Cleanup
    findings = []

    for item in result:
        if len(item) > 0:
            findings.append(item[0])

    #Save
    if save:
        with open("./results/search_" + channel_id + "_" + words + "_" + str(depth) + ".txt", "w") as f:
            json.dump(findings, f)
    
    return findings





# ----
# Misc
# ----

def get_random_video_id(channel_id, depth):
    ids = get_video_ids(channel_id, 32)
    return ids[random.randint(0, len(ids) - 1)]

def open_yt_clips(video_id, keys):
    if keys == None:
            return

    for key in keys:
        webbrowser.open("https://www.youtube.com/watch?v=" + video_id + "&t=" + str(int(key["start"])) + "s")



def main():
    if len(argv) != 4:
        print('Usage: python3 wordFinder.py "<WORD|PHRASE>" <YT-CHANNEL-ID> <DEPTH>')
        exit(1)
    
    try:
        startT = time.time()

        r = run_search_async(argv[1], argv[2], int(argv[3]))
        print(r)

        endT = time.time()
        print("Took: " + str(endT-startT) + "s")
    
    except Exception as e:
        print('Usage: python3 wordFinder.py "<WORD|PHRASE>" <YT-CHANNEL-ID> <DEPTH>')
        exit(1)


if __name__ == "__main__":
    main()
