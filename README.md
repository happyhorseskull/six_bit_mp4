# six_bit_mp4
converts a string of text into an mp4 with audio


### FAQ

#
##### what do I need to run this?
   Python 3 and ffmpeg

#
##### how to use it:
    $ echo "Pick a lane and drive like hell." | python3 six_bit_mp4.py
   
   A file called hexbit.mp4 should appear in the directory when it's done.

#
##### what it does:
   Takes a string from the command line and converts it to video and audio.
   The video is a series of varying patterns but the audio tends towards headache inducing frequencies.
	 There's a 1000Hz low pass filter but if you want high tones that your dog will hate you can comment it out.

#
##### how:
   -converts characters from strings into 6 bits: 'a' to '100100' and squishes them together
   -then it puts the big bunch of bits together repeatedly until there's enough to make a 360x360 jpg
   
   the first iteration will contain only the first letter of the string: PPPPPPPPP..
   
   the second iteration: PiPiPiPiPi..
   
   and so on until all the characters are exhausted

#
##### which characters does it accept?
   - [0-9], [A-Z], [a-z], [_], [.]
   
   '0' = '000000'
   
   ...
   
   '.' = '111111'

#
##### the image on my media player doesn't change but the audio works:
   Yeah this happened to me with VLC. I think the 2 fps rate is unusual and scrambles the media player's brain.

#
##### what if I want a different frame-per-second rate?
   It's possible but you'll have to figure out how to make the audio accept the increased or decreased video byte rate. To increase try changing the mp4's pix_fmt to rgb8 and changing fps from 2 to 6.

#
##### will it work on Windows?
   Probably. You'll have to install ffmpeg which is free and available here: http://www.ffmpeg.org/download.html#build-windows
   
   Then alter the subprocess.call command:
     - change ffmpeg to [ffmpeg directory]\ffmpeg.exe
     
     - delete ', shell=True' from the end of the subprocess.call command

#
##### can I use this code for my own projects?
   Yeah sure totally go for it and you don't even have to credit me. It's a public domain license.

   If you build a twitter bot please let me know so I can make videos.

#
##### why is this Python 3 only?
   It uses int.to_bytes which isn't available in Python 2. Sorry!
   
#   
#####If you have questions or whatever I'm on twitter as @happyhorseskull
