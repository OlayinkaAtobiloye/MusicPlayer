#!venv\Scripts\pythonw.exe
import os
import fnmatch
import tkinter as tk
import pygame
import sqlite3
from tkinter import *


class Interface:

    def __init__(self):
        MusicInterface = tk.Tk()
        MusicInterface.title('mp3 player')
        MusicInterface.geometry('600x500')
        pygame.init()
        pygame.mixer.init()

        con = sqlite3.connect("general.db")
        MusicPlaylist = con.cursor()
        MusicPlaylist.execute('''CREATE TABLE IF NOT EXISTS General (filepath)''')

        MusicFrame = Frame(MusicInterface)

        NewPlaylist = Entry(MusicFrame)
        NewPlaylist.pack(fill=X, side=LEFT)

        def createplaylist():
            MusicPlaylist.execute('''CREATE TABLE IF NOT EXISTS {} (filepath)'''.format(NewPlaylist.get()))
            NewPlaylist.delete(0, END)

        new_playlist = Button(MusicFrame, text='Create Playlist', command=createplaylist)
        new_playlist.pack(fill=X, side=LEFT)

        options = MusicPlaylist.execute("SELECT name FROM sqlite_master where type='table';")
        options = options.fetchall()
        variable = StringVar(MusicFrame)
        variable.set(options[0])
        dropdown = OptionMenu(MusicFrame, variable, *options)
        dropdown.pack(fill=X, side=LEFT)

        PlaylistFrame = tk.Listbox(MusicInterface, width=500, height=4)
        for path, directories, files in os.walk("\\users\\user pc\\Music\\"):
            absolutepath = os.path.abspath(path)
            for file in fnmatch.filter(files, '*.mp3'):
                filepath = os.path.join(absolutepath, file)
                PlaylistFrame.insert(tk.END, filepath)


        def chooseplaylist():
            PlaylistFrame.delete(0, END)
            playlist = variable.get().split("'")[1]
            songs = MusicPlaylist.execute('SELECT * FROM {};'.format(playlist))
            # songs = MusicPlaylist.execute('SELECT * FROM General')
            songs = songs.fetchall()
            for song in songs:
                PlaylistFrame.insert(END, song[0])

        button2 = Button(text='Choose Playlist', master=MusicFrame, bg='red', command=chooseplaylist)
        button2.pack(side=LEFT)

        MusicFrame.pack(fill=X, expand=True)
        PlaylistFrame.pack(fill=tk.BOTH, expand=True)

        ScrollBar = tk.Scrollbar(PlaylistFrame, orient=tk.VERTICAL, command=PlaylistFrame.yview)
        ScrollBar.pack(side=tk.RIGHT, fill=tk.BOTH)
        PlaylistFrame['yscrollcommand'] = ScrollBar.set

        def playSong():
            pygame.mixer.music.load(PlaylistFrame.get(tk.ACTIVE))
            pygame.mixer.music.play()
            pygame.event.wait()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock()
        def addtoplaylist():
            song = PlaylistFrame.get(ACTIVE)
            print(table.get().split("'")[1])
            print(song)
            MusicPlaylist.execute('INSERT INTO {0} VALUES(?);'.format(table.get().split("'")[1]), (song,))

        def pauseSong():
            pygame.mixer.music.pause()

        def resumeSong():
            pygame.mixer.music.unpause()

        def stopSong():
            pygame.mixer.music.stop()

        def reduceVolume():
            volume = pygame.mixer.music.get_volume() - 0.1
            pygame.mixer.music.set_volume(volume)

        def increaseVolume():
            volume = pygame.mixer.music.get_volume() + 0.1
            pygame.mixer.music.set_volume(volume)


        ControlFrame = tk.Frame(width=600, height=50)
        tables = MusicPlaylist.execute("SELECT name FROM sqlite_master where type='table';")
        tables = tables.fetchall()
        table = StringVar(ControlFrame)
        table.set(tables[0])
        tables_dropdown = OptionMenu(ControlFrame, table, *tables)
        tables_dropdown.pack(fill=X, side=LEFT)
        playbutton = tk.Button(text='Play', master=ControlFrame, command=playSong)
        playbutton.pack(fill=tk.X, side=tk.RIGHT, expand=True)
        pausebutton = tk.Button(text='Pause', master=ControlFrame, command=pauseSong)
        pausebutton.pack(fill=tk.X, expand=True, side=tk.RIGHT)
        StopButton = tk.Button(text='Stop', master=ControlFrame, command=stopSong)
        StopButton.pack(fill=tk.X, expand=True, side=tk.RIGHT)
        ReduceButton = tk.Button(text='Reduce Volume', master=ControlFrame, command=reduceVolume)
        ReduceButton.pack(fill=tk.X, expand=True, side=tk.RIGHT)
        IncreaseButton = tk.Button(text='Increase Volume', master=ControlFrame, command=increaseVolume)
        IncreaseButton.pack(fill=tk.X, expand=True, side=tk.RIGHT)
        addtoplaylistButton = tk.Button(text='Add to Playlist', master=ControlFrame, command=addtoplaylist, bg='blue')
        addtoplaylistButton.pack(fill=tk.X, expand=True, side=tk.RIGHT)
        ControlFrame.pack(fill=tk.X, expand=True)
        MusicInterface.mainloop()
        con.commit()
        con.close()


Interface()



