#!venv\Scripts\pythonw.exe
import os
import fnmatch
import tkinter as tk
import pygame
import sqlite3


class Interface:


    def __init__(self):
        MusicInterface = tk.Tk()
        MusicInterface.title('mp3 player')
        MusicInterface.geometry('600x400')
        pygame.init()
        pygame.mixer.init()

        PlaylistFrame = tk.Listbox(MusicInterface, width=600, height=400)
        PlaylistFrame.pack(fill=tk.BOTH, expand=True)
        for path, directories, files in os.walk("\\users\\user pc\\Music\\"):
            absolutepath = os.path.abspath(path)
            for file in fnmatch.filter(files, '*.mp3'):
                filepath = os.path.join(absolutepath, file)
                PlaylistFrame.insert(tk.END, filepath)

        ScrollBar = tk.Scrollbar(PlaylistFrame, orient=tk.VERTICAL, command=PlaylistFrame.yview)
        ScrollBar.pack(side=tk.RIGHT, fill=tk.BOTH)
        PlaylistFrame['yscrollcommand'] = ScrollBar.set

        def playSong():
            pygame.mixer.music.load(PlaylistFrame.get(tk.ACTIVE))
            pygame.mixer.music.play()
            pygame.event.wait()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock()

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

        def nextSong():
            currentSong = PlaylistFrame.get(tk.ACTIVE)
            currentPosition = PlaylistFrame.index(currentSong)
            nextPosition = currentPosition + 1
            PlaylistFrame.select_clear(currentPosition)
            PlaylistFrame.select_set(nextPosition)
            # PlaylistFrame.selection_set(nextSong)

        def previousSong():
            currentSong = PlaylistFrame.get(tk.ACTIVE)
            currentPosition = PlaylistFrame.index(currentSong)
            previousPosition = currentPosition - 1
            PlaylistFrame.activate(previousPosition)

        ControlFrame = tk.Frame(width=600, height=50)
        PlayButton = tk.Button(text='Play', master=ControlFrame, command=playSong)
        PlayButton.pack(fill=tk.X, side=tk.RIGHT, expand=True)
        PauseButton = tk.Button(text='Pause', master=ControlFrame, command=pauseSong)
        PauseButton.pack(fill=tk.X, expand=True, side=tk.RIGHT)
        StopButton = tk.Button(text='Stop', master=ControlFrame, command=stopSong)
        StopButton.pack(fill=tk.X, expand=True, side=tk.RIGHT)
        NextButton = tk.Button(text='Next', master=ControlFrame, command=nextSong)
        NextButton.pack(fill=tk.X, expand=True, side=tk.RIGHT)
        PreviousButton = tk.Button(text='Previous', master=ControlFrame, command=previousSong)
        PreviousButton.pack(fill=tk.X, expand=True, side=tk.RIGHT)
        ReduceButton = tk.Button(text='Reduce Volume', master=ControlFrame, command=reduceVolume)
        ReduceButton.pack(fill=tk.X, expand=True, side=tk.RIGHT)
        IncreaseButton = tk.Button(text='Increase Volume', master=ControlFrame, command=increaseVolume)
        IncreaseButton.pack(fill=tk.X, expand=True, side=tk.RIGHT)
        ControlFrame.pack(fill=tk.X, expand=True,)
        MusicInterface.mainloop()


Interface()



