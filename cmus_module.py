#!/usr/bin/python
# py3status module for displaying status of cmus music player
"""
Displays status of cmus music player

Displays the current status (playing, stopped, paused) of songs.
Contains options for formatting output, and supports fetching of plenty of parameters such as:
    - song name
    - song artist
    - song album
    - song duration
    - song position

Configuration Parameters:
    - cache_timeout     : time in seconds per refresh of this module
    - play_icon         : character to use as a play icon, default is f04b
    - pause_icon        : character to use as a pause icon, default is f04c
    - stop_icon         : character to use as a stop icon, defualt is f04d
    - strformat         : string output format, available options shown here:
        + {name}        : name of song currently playing
        + {artist}      : name of artist currently playing
        + {album}       : name of album currently playing
        + {time}        : current song time in format %min:%sec, minutes can go above 60 for long songs
        + {duration}    : current song duration in format %min:%sec, minutes can go above 60 for long songs
        + {statusicon}  : icon of the current status, uses play-stop-pause icons
    - use_colors        : use color_good, color_degraded, and color_default for play, pause, and stop statuses
    - error_text        : text to display if there is an error or cmus is not running


"""
from time import time
import subprocess

class Py3status:

    cache_timeout = 1
    play_icon = ""
    pause_icon = ""
    stop_icon = ""
    strformat = "{statusicon}  {time}/{duration} {name} by {artist}"
    use_colors = False
    error_text = "error"

    def __init__(self):
        pass

    def kill(self, i3s_output_list, i3s_config):
        pass

    def on_click(self, i3s_output_list, i3s_config):
        pass

    def _get_cmus_attributes(self):
        cmus_subprocess = subprocess.Popen(["cmus-remote","-Q"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        status_out = cmus_subprocess.communicate()[0].decode()
        if status_out == "":
            return {}

        tokens = {}

        for line in status_out.splitlines():
            attributes = line.split(None, 2)

            if attributes[0] in {"status", "duration", "position", "file"}:
                tokens[attributes[0]] = ''.join(attributes[1:])
            else:
                try:
                    tokens[attributes[1]] = attributes[2]
                except IndexError:
                    continue

        return tokens

    def cmus_update(self, i3s_output_list, i3s_config):
        output = {}
        output["cached_until"] = time() + self.cache_timeout

        status = self._get_cmus_attributes()

        if status:
            icon = None
            if status["status"] == "playing": icon = self.play_icon
            elif status["status"] == "paused": icon = self.pause_icon
            else: icon = self.stop_icon

            if self.use_colors == True:
                if status["status"] == "playing": output["color"] = i3s_config["color_good"]
                elif status["status"] == "paused": output["color"] = i3s_config["color_degraded"]

            pos_form = str( int(status["position"]) // 60) + ':' + str( int(status["position"]) % 60).zfill(2)
            dur_form = str( int(status["duration"]) // 60) + ':' + str( int(status["duration"]) % 60).zfill(2)

            filename_short = status["file"][(status["file"].rfind("/")+1):] 

            out_str = self.strformat.format(name=status["title"] if "title" in status else filename_short,
                                         artist=status["artist"] if "artist" in status else "Unknown",
                                         album=status["album"] if "album" in status else "Unknown",
                                         time=pos_form,
                                         duration=dur_form,
                                         statusicon=icon)

            output["full_text"] = out_str
        else:
            output["full_text"] = self.error_text

        return output

if __name__ == "__main__":
    from time import sleep
    x = Py3status()
    while True:
        print(x.cmus_update([],{}))
        sleep(1)
