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

"""The head and tail pointers are connected to form a circular structure.
head.prev points to the last node (tail), and tail.next points to the first node (head), creating a loop in the linked list."""


class Node:
    def __init__(
        self, data
    ):  # Initialize a Node with data and pointers to the previous and next nodes.
        self.data = data  # Store the data in the node
        self.prev = None  # Pointer to the previous node (initialized to None)
        self.next = None  # Pointer to the next node (initialized to None)


class CircularDoublyLinkedList:
    def __init__(
        self,
    ):  # Initialize the doubly linked list with head, tail, and current node pointers set to None
        self.head = None
        self.tail = None
        self.current_node = None

    def append(self, data):
        new_node = Node(data)  # Create a new node with the provided data
        if self.head is None:  # Check if the list is empty
            self.head = (
                self.tail
            ) = new_node  # If the list is empty, set the new node as both head and tail
        else:  # If the list is not empty, add the new node to the end of the list
            new_node.prev = self.tail  # Update new node's previous pointer
            self.tail.next = new_node  # Update previous tail's next pointer to new node
            self.tail = new_node  # Update tail pointer to the new node
        # Make the connections for a circular doubly linked list
        self.head.prev = self.tail  # Connect the head's previous to the tail
        self.tail.next = self.head  # Connect the tail's next to the head

    def play_next(self):
        if (
            self.current_node and self.current_node.next
        ):  # Move to the next node and return its data if it exists
            self.current_node = (
                self.current_node.next
            )  # Updating current node with next node
            return self.current_node.data  # Returning the updated node
        # Handle circular traversal to the head if currently at the tail
        elif self.current_node == self.tail:  # If current node is the last node then
            self.current_node = self.head  # Link the circular loop
            return self.current_node.data  # Return the current node data
        return None  # If nothing was there return None

    def play_previous(self):
        if (
            self.current_node and self.current_node.prev
        ):  # Move to the previous node and return its data if it exists
            self.current_node = (
                self.current_node.prev
            )  # Updating current node with prev node
            return self.current_node.data  # Returning the updated node
        # Handle circular traversal to the head if currently at the tail
        elif self.current_node == self.head:  # If current node is the first node then
            self.current_node = self.tail  # Link the circular loop
            return self.current_node.data  # Return the current node data
        return None  # If nothing was there return None

    def get_song_at(
        self, index
    ):  # Traverse the list to find the node at the given index and return its data
        current = self.head  # Start traversal from the head of the linked list
        count = 0  # Temp variable for counting
        while (
            current
        ):  # Traverse the list until the current node is not None (end of the list)
            if count == index:  # If the value of count equals to index the
                return current.data  # return its data
            count += 1  # else increment count
            current = current.next  # update the current node with next node
        return None  # If nothing was there return None


playlist = CircularDoublyLinkedList()  # Creating object for CircularDoublyLinkedList


def play_next_song():  # Function to play next song
    next_song = playlist.play_next()  # Retrieve the next song from the playlist
    if next_song:  # If next song exist
        mixer.music.load(next_song)  # Load song into mixer
        mixer.music.play()  # Play the loaded song
        music.config(
            text=os.path.basename(next_song)
        )  # Update the display with the song name
    else:  # If the song doesn't exist
        first_song = playlist.get_song_at(0)  # Retrive the first song
        if first_song:  # If first song exists
            mixer.music.load(first_song)  # Load song into mixer
            mixer.music.play()  # Play the loaded song
            music.config(
                text=os.path.basename(first_song)
            )  # Update the display with the song name
        playlist.current_node = (
            playlist.head
        )  # Set the current node to the beginning of the playlist


def play_previous_song():
    if mixer.music.get_busy():  # Check if the mixer is currently playing a song
        current_song = mixer.music.get_pos()  # Get the position of the current song
        if (
            playlist.current_node == playlist.head
        ):  # If the current song is the first one
            playlist.current_node = (
                playlist.tail
            )  # Move the current node to the last song in the playlist
            mixer.music.load(playlist.current_node.data)  # Load song into mixer
            mixer.music.play()  # Play the loaded song
            music.config(
                text=os.path.basename(playlist.current_node.data)
            )  # Update the display with the song name
        else:  # If the current song is not the first one
            previous_song = (
                playlist.play_previous()
            )  # Get the previous song from the playlist
            if not previous_song:  # if there is no previous song
                previous_song = playlist.tail.data  # Move to the last song of the list
            mixer.music.load(previous_song)  # Load song into mixer
            mixer.music.play()  # Play the loaded song
            music.config(
                text=os.path.basename(previous_song)
            )  # Update the display with the song name


def open_folder():  # Function to open dialog box for choosing folder
    path = filedialog.askdirectory()  # file dialogue popup
    if path:  # Checks if path exist
        os.chdir(path)  # choose directory
        songs = os.listdir(path)  # all the files in the path
        for song in songs:
            if song.endswith(".mp3"):  # if mp3 files
                full_path = os.path.join(path, song)  # Get the full path of mp3 files
                List_of_songs.insert(END, song)  # Inserts the song into the GUI list
                playlist.append(
                    full_path
                )  # Adds the full path of the song to the playlist which is used to retrive data for Linkedlist


def play_song():
    if List_of_songs.curselection():  # Check if a song is selected
        index = int(
            List_of_songs.curselection()[0]
        )  # Retrieves the index of the selected song
        if index < List_of_songs.size():  # Check if index is within the playlist length
            music_name = List_of_songs.get(
                index
            )  # Get the name of the song using index from the list
            full_path = playlist.get_song_at(index)  # Get the full path of the song
            if full_path:  # If the path exists
                mixer.music.load(full_path)  # Load song into mixer
                mixer.music.play()  # Play the loaded song
                music.config(text=music_name)  # Update the display with the song name
                playlist.current_node = (
                    playlist.head
                )  # Adds the full path of the song to the playlist which is used to retrive data for Linkedlist


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
music.place(relx=0.2, rely=0.5, anchor="s")  # Position of label

logo_img = PhotoImage(file="logo.png")  # Logo on the application console
header_frame = Frame(root, bg="#333333")  # Header frame for the application
header_frame.pack(side=TOP, fill=X)  # Placed on the top of the window
logo_label = Label(
    header_frame, image=logo_img, bg="#333333"
)  # Logo placed on top left of the header frame
logo_label.pack(side=LEFT, padx=1, pady=1)  # Position of the logo on header
text_label = Label(
    header_frame,
    text="Music Player",
    fg="#6fe3ff",
    bg="#333333",
    font=("Helvetica", 18, "bold"),
)  # Header Text
text_label.pack(side=LEFT, padx=5, pady=5)  # Header text position
music_frame = Frame(root, bd=2, relief=RIDGE)  # Directory Mp3 files Frame
music_frame.place(
    x=430, y=100, width=560, height=250
)  # It represents the position of Directory mp3 files
image = PhotoImage(file="openfolder.png")  # Open folder icon
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
)  # Open folder icon is merged with text 'Open Folder'
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
)  # List of songs
scroll.config(
    command=List_of_songs.yview
)  # To configure scroll bar to interact with vertical view of list_of_songs widget
scroll.pack(
    side=RIGHT, fill=Y
)  # It packs scroll bar within the window and placed on the right hand side
List_of_songs.pack(
    side=LEFT, fill=BOTH
)  # It fills list of songs from left on both x and y axis
next_button = PhotoImage(file="next.png")

# Create the "Next" button with the play_next_song function as the command
Button(root, image=next_button, bg="#333333", bd=0, command=play_next_song).place(
    x=600, y=400  # Adjust the coordinates as needed
)
previous_button = PhotoImage(file="prev.png")
Button(
    root, image=previous_button, bg="#333333", bd=0, command=play_previous_song
).place(
    x=500, y=400  # Adjust the coordinates as needed
)

root.mainloop()  # Main function
