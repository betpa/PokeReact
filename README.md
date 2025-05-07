# PokeReact

PokeReact is intended to generate pokemon showdown links to the various animated sprite gifs they host. It doesn't actually save any of the gifs to your local machine.

To grab the tool, just download the "dist" folder. If you don't trust my compile, you can compile it yourself easily by installing python and downloading the .pyw and then running the following commands:

pip install pyinstaller
pip install pyperclip
pip install thefuzz

and then in the folder with the code:
pyinstaller -F PokeReact.pyw


The intended workflow is to bind this program to a hotkey that you can press whenever you need a sprite. Once you find the relevant gif and hit "Copy!", PokeReact will close. 


To setup the hotkey, right click on the exe and create a shortcut. Then move the shortcut to C:\ProgramData\Microsoft\Windows\Start Menu\Programs (or wherever your start menu shortcuts are). Then right click the shortcut > Properties > shortcut and enter a shorcut key.
