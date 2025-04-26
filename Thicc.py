import os
import sys
import urllib.request
import multiprocessing
import tkinter as tk
from pathlib import Path
from playsound import playsound
from PIL import Image, ImageTk
from screeninfo import get_monitors  # To get the monitor size

def Handling():
    """Handling the functions"""
    print("""
    ++++++++++++++++++++++++++++++++++++++++++++++++++
                    Starting Program...
    ++++++++++++++++++++++++++++++++++++++++++++++++++
    """)
    Folder()
    Files()
    try:
        SoundAndForm()
    except Exception as e:
        print("[ERROR]", e)
        input("Press ENTER to exit...")
    print("""
    ++++++++++++++++++++++++++++++++++++++++++++++++++
                    Finished Program
    ++++++++++++++++++++++++++++++++++++++++++++++++++
    """)
    input("Press any key to close...")

def Folder():
    """Creating Folder if missing"""
    print("""
    ==================================================
                    Creating Folder...
    ==================================================
    """)
    temp_path = Path(os.getenv('TEMP')) / 'Thicc'
    if not temp_path.exists():
        temp_path.mkdir()
        print(f"    [✓] Folder created at > {temp_path} <")

def Files():
    """Downloading Files"""
    print("""
    ==================================================
                    Downloading Files...
    ==================================================
    """)
    temp_path = Path(os.getenv('TEMP')) / 'Thicc'
    files = {
        "Thicc.png": "https://raw.githubusercontent.com/Bruchstein/Thicc/main/items/Thicc.png",
        "Thicc.mp3": "https://raw.githubusercontent.com/Bruchstein/Thicc/main/items/hotmilk.mp3"
    }
    for filename, url in files.items():
        file_path = temp_path / filename
        print(f"    [↩] Downloading {filename} from {url}...")
        urllib.request.urlretrieve(url, file_path)
        print(f"    [✓] Downloaded {filename} to > {file_path} <")

def resize_image(image_path):
    """Resize the image to fit the screen without white borders"""
    print("""
    ==================================================
                    Resizing Image...
    ==================================================
    """)
    monitor = get_monitors()[0]
    screen_width, screen_height = monitor.width, monitor.height

    with Image.open(image_path) as img:
        img_width, img_height = img.size
        # Resize the image to fit within the screen dimensions
        ratio = min(screen_width / img_width, screen_height / img_height)
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        resized_img.save(image_path)
        print(f"    [✓] Image resized from {img_width}x{img_height} to {new_width}x{new_height}")
        return resized_img

def SoundAndForm():
    """Setting up the form and playing the sound"""
    print("""
    ============================================================
                    Setting up Sound and Form...
    ============================================================
    """)
    temp_path = Path(os.getenv('TEMP')) / 'Thicc'
    sound_path = temp_path / 'Thicc.mp3'

    # Resize the image before displaying it
    resized_img = resize_image(temp_path / 'Thicc.png')

    # Initialize tkinter window
    root = tk.Tk()
    root.title("Thicc😮🤤🤤🤤")
    root.attributes('-fullscreen', True)

    # Create PhotoImage after initializing the root window
    bg_image = ImageTk.PhotoImage(resized_img)

    black_background = tk.Label(root, bg="black")
    black_background.place(x=0, y=0, relwidth=1, relheight=1)

    image_label = tk.Label(root, image=bg_image)
    image_label.place(x=0, y=0, relwidth=1, relheight=1)
    image_label.lower()

    print("    [✓] Form set up with resized background image")

    # Show times for the image to appear
    show_times = [5300, 8460, 11670, 14870, 18060, 21260, 24470, 27620, 30800, 33950, 37150]

    # Start playing sound in a separate process
    SoundProcess = multiprocessing.Process(target=playsound, args=(str(sound_path),))

    def ExitProgram(event=None):
        """Terminate the sound process and exit the program"""
        print("    [✘] Terminating program...")
        if SoundProcess.is_alive():
            SoundProcess.terminate()
        # Remove the entire folder and its contents
        if temp_path.exists():
            for item in temp_path.iterdir():
                item.unlink()  # Remove file or symbolic link
            temp_path.rmdir()  # Remove the empty folder
            print(f"    [✓] Temporary folder '{temp_path}' deleted.")
        root.quit()
        sys.exit()

    root.bind("<Escape>", ExitProgram)

    def show_image():
        """Show the image"""
        print(f"    [i] Displaying image...")
        image_label.lift()

    def show_black():
        """Hide the image and show the black background"""
        print(f"    [i] Hiding image...")
        image_label.lower()

    def schedule_timing():
        """Schedule the image display times"""
        for t in show_times:
            root.after(t, show_image)
            root.after(t + 850, show_black)

    SoundProcess.start()
    print("    [▶] Sound started...")
    root.after(200, schedule_timing)

    # Hardcoded duration (song duration in ms)
    duration_ms = 41100
    root.after(duration_ms, ExitProgram)

    root.mainloop()

if __name__ == "__main__":
    Handling()
