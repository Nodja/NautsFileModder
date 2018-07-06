# NautsFileModder
Awesomenauts File Modder with built-in game patching

# Usage
 1) [Download](https://github.com/Nodja/NautsFileModder/releases) from releases  
 2) **For technical reaasons you must extract it inside the same drive as the game** (it uses hard links)  
 3) Add mods inside the ```mods``` folder, file extension must be .nfm (samples inside)
 4) run nfm.bat to launch the modder 
 5) run dumper.bat to dump game contents into ```_dumps```  
 
 Note: nfm.cfg is preloaded with a setting modification that will zoom out after you land your droppod.
 
# What does it do?

1) Find where you installed the game by looking for the game executable inside the folders listed in the cfg file.  
2) Create a hard link copy of every file in the game folder and place it inside ```_env```
3) See which files you want to modify by looking at sections that start with ```settings=``` or ```file=```, you must provide the whole relative path for the decryption/encryption to be valid.  
4) Decrypt the original file, do the modifications and re-encrypt it, placing the modified file inside ```_env```. This will not affect your original game files.
5) Launch the game from inside ```_env```
6) Patch the game memory so it skip integrity checks. This is needed for the game to accept the modified file.

# Improvement that I will never get to

1) Support easy binded files modding, you'll have to bind them manually yourself
2) Tell the game to reload game settings live
3) Make the patch on the executable itself rather than memory. (harder to detect)
