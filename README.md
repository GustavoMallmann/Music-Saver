# Music-Saver
Simple app to add current playing Spotify music to an auxiliar playlist with a single click for later use so you dont have to lose focus on what you are doing.
All you need is your spotify: client ID, client secret, and one redirect URI of your choice. 


Use version 2.0

First run preparation.py to create the .env file with your information;
The app file is musicSaver.py. For practicality, you can use it with a .bat file, turn it into an exe or whatever.

How to use:
- To find your spotify, go to https://developer.spotify.com/dashboard/applications, create an application (name and description don't matter, you can delete it afterwards), there you'll find client id and client secret.
- Execute preparation.py, you'll be asked for your informations, just insert them in the order they're asked. For the redirect URI i use https://github.com/GustavoMallmann/.
- Whenever you want to keep memory of the song you're listening, just execute MusicSaver.py, if the playlist doesn't exist, it will be created.

OBS:
- Try to keep the MusicSaver playlist as much on top in the order as you can since it will improve the algorithm speed. If it goes past rank 50 in the order, the app will create a new playlist.
- If by some reason it stops working try to restart the entire process.
