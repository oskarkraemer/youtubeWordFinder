from os import listdir
from os.path import isfile, join
import time

import pickle

#Own modules
import logger

CACHE_DIR = "./cache/"
ID_CACHE_DIR = "./id_cache/"


#Logging
lg = logger.Logger()

LOADED_SUBTITLES = {}

# ----
# ID Caching
# ----

def id_cache_available(channel_id, depth):
    files = [f for f in listdir(ID_CACHE_DIR) if isfile(join(ID_CACHE_DIR, f))]

    highest_depth = 0
    for fl in files:
        split_name = fl.split("-")
        if split_name[0] == "videoIDs" and split_name[2] == channel_id + ".pkl":
            if int(split_name[1]) >= depth and int(split_name[1]) > highest_depth:
                highest_depth = int(split_name[1])
    
    return highest_depth



def save_ids(video_ids, channel_id, depth):
    #Save in file
    with open(ID_CACHE_DIR + "videoIDs-" + str(depth) + "-" + channel_id + ".pkl", "wb") as f:
        pickle.dump(video_ids, f)


def load_ids(channel_id, depth):
    #Load file
    highest_depth = id_cache_available(channel_id, depth)
    if highest_depth == 0:
        return []

    tmp = []
    with open(ID_CACHE_DIR + "videoIDs-" + str(highest_depth) + "-" + channel_id + ".pkl", "rb") as f:
        tmp = pickle.load(f)
    
    #Only keep the desired depth! i.g. list = list[0:depth * 100]
    return tmp[0:depth * 100]




# ----
# Subtitle Caching
# ----

FILES_CACHE = []

def subtitle_cache_available(video_id):
    global FILES_CACHE
    st = time.time()
    if len(FILES_CACHE) == 0:
        FILES_CACHE = [f for f in listdir(CACHE_DIR) if isfile(join(CACHE_DIR, f))]
    et = time.time()

    lg.print_log("Directory took: " + str(et - st))

    return "subtitle_" + video_id + ".pkl" in FILES_CACHE


def save_subtitle(subtitle, video_id):
    #Save in file
    with open(CACHE_DIR + "subtitle_" + video_id + ".pkl", "wb") as f:
        pickle.dump(subtitle, f)


def load_subtitle(video_id):
    if video_id in LOADED_SUBTITLES:
        return LOADED_SUBTITLES[video_id]
    
    else:
        st = time.time()
        #Load file
        with open(CACHE_DIR + "subtitle_" + video_id + ".pkl", "rb") as f:
            r = pickle.load(f)

            et = time.time()
            lg.print_log("IO took: " + str(et - st))

            return r
        


def preload_subtitles():
    files = [f for f in listdir(CACHE_DIR) if isfile(join(CACHE_DIR, f))]

    for fl in files:
        video_id = fl.split("_", 1)[1][:-4]
        global LOADED_SUBTITLES
        LOADED_SUBTITLES[video_id] = load_subtitle(video_id)
    

    lg.set_box(True)

    lg.print_log("Loaded amount: " + str(len(LOADED_SUBTITLES)))
    
    lg.set_box(False)