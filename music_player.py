from tkinter import *
from tkinter import filedialog
from pygame import mixer
import os

root = Tk()  # Initializes the main window using Tkinter.
root.title("Music Player")  # Title of the application
root.geometry("1000x520+1+10")  # dimension of window+intial screen positions *****
root.configure(bg="#333333")  # Configures the Background of the window
root.resizable(False, False)  # Restricting to resize
mixer.init()  # Intializing the pygame mixer for audio playback


def open_folder():  # Function to open dialog box for choosing folder
    path = filedialog.askdirectory()  # filedialogue popup
    if path:  # Checks if path exist
        os.chdir(path)  # choose directory
        songs = os.listdir(path)  # all the files in the path
        for song in songs:
            if song.endswith(".mp3"):  # if mp3 files
                List_of_songs.insert(
                    END, song
                )  # add to playlist(listbox) which displays in the application


def play_song():  # Function to play song
    music_name = List_of_songs.get(ACTIVE)  # retrives current playing songname from playlist
    mixer.music.load(music_name)  # loads the song into mixer for playback(playing)
    mixer.music.play()  # songs will start playing
    music.config(text=music_name[0:])  # Display the song name


image_icon = PhotoImage(file="logo.png")  # Logo is stored as Photo image
root.iconphoto(False, image_icon)  # Logo of the window
# Buttons
play_button = PhotoImage(file="play.png")  # Play button
Button(root, image=play_button, bg="#333333", bd=0, command=play_song).place(
    x=200, y=400
)
stop_button = PhotoImage(file="stop.png")  # Stop Button
Button(root, image=stop_button, bg="#333333", bd=0, command=mixer.music.stop).place(
    x=300, y=400
)
resume_button = PhotoImage(file="resume.png")  # Resume Button
Button(
    root, image=resume_button, bg="#333333", bd=0, command=mixer.music.unpause
).place(x=400, y=400)
pause_button = PhotoImage(file="pause.png")  # Pause Button
Button(root, image=pause_button, bg="#333333", bd=0, command=mixer.music.pause).place(
    x=500, y=400
)
music = Label(
    root, text="", font=("Helvetica", 12, "bold"), fg="white", bg="#333333"
)  # The Label that Displays Current Playing Song
music.place(relx=0.15, rely=0.5, anchor="s")#Position of label

logo_img = PhotoImage(file="logo.png")  # Logo on the application console
header_frame = Frame(root, bg="#333333")# Header frame for the application
header_frame.pack(side=TOP, fill=X)#Placed on the top of the window
logo_label = Label(
    header_frame, image=logo_img, bg="#333333"
)  # Logo placed on top left of the header frame
logo_label.pack(side=LEFT, padx=1, pady=1)#Position of the logo on header
text_label = Label(
    header_frame,
    text="Music Player",
    fg="#6fe3ff",
    bg="#333333",
    font=("Helvetica", 18, "bold"),
)  # Header Text
text_label.pack(side=LEFT, padx=5, pady=5)#Header text position
music_frame = Frame(root, bd=2, relief=RIDGE)  # Directory Mp3 files Frame
music_frame.place(x=430, y=100, width=560, height=250)#It represents the position of Directory mp3 files
image = PhotoImage(file="openfolder.png")#Open folder icon
combined_button = Button(
    root,
    text="Open Folder",
    image=image,
    width=160,
    height=77,
    compound="left",
    font=("Helvetica", 12, "bold"),
    fg="#dd95ff",
    bg="#333333",
    bd=0,
    command=open_folder,
)#Open folder icon is merged with text 'Open Folder'
combined_button.place(x=5, y=70)  # Open folder button position
scroll = Scrollbar(music_frame)  # Enables scrolling in mp3 files Listbox
List_of_songs = Listbox(
    music_frame,
    width=100,
    font=("arial", 10),
    bg="#333333",
    fg="grey",
    cursor="hand2",
    bd=0,
    yscrollcommand=scroll.set,
)#List of songs
scroll.config(command=List_of_songs.yview)  # To configure scroll bar to interact with vertical view of list_of_songs widget
scroll.pack(side=RIGHT, fill=Y)#It packs scroll bar within the window and placed on the right hand side
List_of_songs.pack(side=LEFT, fill=BOTH)#It fills list of songs from left on both x and y axis
root.mainloop()  # Main function
