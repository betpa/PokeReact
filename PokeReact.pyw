from tkinter import *
from tkinter import ttk
from thefuzz import fuzz
import pyperclip
import json
import os
import sys

SHOWDOWN_LINK = "https://play.pokemonshowdown.com/sprites/"
SHINY_LINK = "ani-shiny/"
NORMAL_LINK = "ani/"
FAVORITES = "favorites.json"
POKEDEX = "pokedex.json"

class PokeReact():

    def __init__(self):

        self.pokedex = []
        self.load_pokedex()
        self.favorites = []
        self.load_favorites()

        root = Tk()
        root.title("PokeReact")
        icon = PhotoImage(file  = "quick-claw.png")
        root.iconphoto(True,icon)
        root.geometry("400x300")

        style = ttk.Style(root)
        style.configure('lefttab.TNotebook', tabposition='ws')

        tabControl = ttk.Notebook(root, style='lefttab.TNotebook', height=280 , width=200)
        tabControl.grid(row = 0, column = 0, columnspan= 3, rowspan= 3)

        
        self.selectedPoke = StringVar()
        self.selectedName = StringVar()
        self.isFav = BooleanVar()
        self.shiny = BooleanVar(root, False)

        # selected pokemon
        selectedLabel = ttk.Label(root, textvariable=self.selectedName)
        selectedLabel.grid(row = 0, column= 3, sticky="NE")

        
        favCheck = ttk.Checkbutton(root,text='Fav ', variable=self.isFav, command=self.add_favorite)
        favCheck.grid(row = 0, column= 3, sticky="NW")

        
        shinyCheck= ttk.Checkbutton(root,text='Shiny?', variable=self.shiny)

        shinyCheck.grid(row = 0, column= 3, sticky="S")

        self.formeList = Listbox(root, selectmode='single',)
        self.formeList.grid(row = 1, column= 3, sticky="N")


        button = ttk.Button(root, text="Copy!", command=self.to_clip)
        button.grid(row = 2, column = 3, sticky= "S" )
    
        # search tab
        search = ttk.Frame(tabControl, width=300, height=400)
        self.search_string = StringVar()
        self.search_string.trace_add("write", self.search_callback)
        search_string_entry = ttk.Entry(search, width=31, textvariable=self.search_string,).grid()

        self.list = Listbox(search, selectmode="single", width=32, height=16)
        self.list.grid()
        self.search_list("",loadAll = True)
        self.list.bind("<<ListboxSelect>>", self.poke_selected)
  
        tabControl.add(search, text ='Search')

        # favorites tab
        favTab = ttk.Frame(tabControl, width=300, height=400)

        self.favList = Listbox(favTab, selectmode="single", width=32, height=17)
        self.favList.grid()
        self.favorites_list()
        self.favList.bind("<<ListboxSelect>>", self.poke_selected)

        tabControl.add(favTab, text ='Favorites')
        
        # grab first mon
        self.set_selected(list(self.pokedex.keys())[0])

        #search_string_entry.focus()
        root.bind("<Return>", self.to_clip)

        try: 
            root.mainloop()
        finally:
            self.save_favorites()


    def set_selected(self, selected):
        self.selectedPoke.set(selected)
        self.selectedName.set(self.pokedex[selected]['name'])

        if selected in self.favorites:
            self.isFav.set(True)
        else:
            self.isFav.set(False)

        self.formeList.delete(0, 'end')

        if 'otherFormes' in self.pokedex[selected]:
            for p in self.pokedex[selected]['otherFormes']:
                if "Mega" not in p:
                    self.formeList.insert(END,p)

    def poke_selected(self, event, *args):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            pokeName = event.widget.get(index)
            pokeKey = name_to_key(pokeName)
            self.set_selected(pokeKey)
                        
    def build_link(self):
        sdLink = SHOWDOWN_LINK
        if self.shiny.get():
            sdLink = sdLink + SHINY_LINK
        else:
            sdLink = sdLink + NORMAL_LINK

        if self.formeList.curselection():
            forme = self.formeList.get(self.formeList.curselection())
            if forme:
                poke = forme.lower()
        else: 
            poke = self.selectedPoke.get().lower()

        return sdLink+poke+".gif"

    def to_clip(self, *args):
        pyperclip.copy(self.build_link())
        sys.exit()

    def load_favorites(self):
        try:
            with open(FAVORITES,"r",errors="ignore") as f:
                self.favorites = json.load(f)
                f.close()
        except:
            pass

    def save_favorites(self):
        try:
            os.remove(FAVORITES)
        except:
            pass
        with open(FAVORITES, 'w') as f:
            json.dump(self. favorites, f, indent=4)

    def add_favorite(self):
        self.favorites.insert(len(self.favorites), self.selectedPoke.get())
        self.favorites_list()

    def load_pokedex(self):
        with open(POKEDEX,"r",errors="ignore") as f:
            self.pokedex = json.load(f)
            f.close()

        #remove formes and unreleased
        for key in list(self.pokedex):
            p = self.pokedex[key]
            if "forme" in p:
                self.pokedex.pop(key)
            # fsr kinggambit is the limit?
            if (p['num'] >= 983 or p['num']<1) and (key in self.pokedex):
                self.pokedex.pop(key)

    def search_callback(self, *args):
        self.search_list(self.search_string.get())

    def favorites_list(self):
        self.favList.delete(0, 'end')
        for f in self.favorites:
            self.favList.insert(END,self.pokedex[f]['name'])


    def search_list(self, searchString, loadAll = False):
        self.list.delete(0, 'end')

        for p in self.pokedex.values():
            add = False

            if loadAll == True:
                add = True
            elif fuzz.partial_ratio(searchString, p['name']) > 80:
                add = True
            elif searchString in p['name']:
                add = True
            if add == False: 
                continue
            self.list.insert(END,p['name'])
        return

def name_to_key(str):
    str = str.lower()
    str = str.replace(" ","")
    str = str.replace("-","")

    #stupid farfetch'd
    str = str.replace("'","")
    return str

PokeReact()
