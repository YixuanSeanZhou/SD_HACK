import pyaudio # server playback requires ffplay/avplay
import pydub # requires ffmpeg (and thus lame)
from pydub.playback import play
import sys

path = "Wild_Battle_Crowd_Approach.mp3"

sound = pydub.AudioSegment.from_mp3(path)

play(sound)

# pydub apparently good for manipulating audio files,
# possibly better libraries for serializing out there
