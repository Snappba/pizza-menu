import tkinter as tk
from tkinter import PhotoImage

def openSecondWindow():
    # Create a new top-level window
    secondWindow = tk.Toplevel(root)
    secondWindow.title("Second Window")
    
    # Add some content to the second window
    label = tk.Label(secondWindow, text="This is the second window")
    label.pack(padx=20, pady=20)

# Create the main application window
root = tk.Tk()
root.title("Pizza Palace Ordering")
root.geometry("612x430")
# Load the background image (make sure the extension is correct)
background_image = PhotoImage(file="pizza_bg.png")  # Adjust file extension as needed

# Create a label with the image
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)  # Fill the entire window

# Add a button to the main window
button = tk.Button(root, text="Open Second Window", command=openSecondWindow)
button.pack(padx=20, pady=20)  # Use pack() to display the button

# Run the application
root.mainloop()
