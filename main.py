import tkinter as tk
from PIL import Image, ImageTk

class BaseWindow:
    def __init__(self, root, title, width, height, background_image=None):
        self.root = root
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(True, True)
        self.root.iconbitmap(r'favicon.ico')

        if background_image:
            self.background_image_path = background_image
            self.original_image = Image.open(self.background_image_path)
            self.background_label = tk.Label(self.root)
            self.background_label.place(relwidth=1, relheight=1)
            self.update_background_image()
            self.root.bind("<Configure>", self.on_resize)

    def update_background_image(self):
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        resized_image = self.original_image.resize((width, height), Image.Resampling.LANCZOS)
        self.background_image = ImageTk.PhotoImage(resized_image)
        self.background_label.config(image=self.background_image)
        self.background_label.image = self.background_image  #

    def on_resize(self, event):
        self.update_background_image()

class MainWindow(BaseWindow):
    def __init__(self, root):
        super().__init__(root, "Pizza Palace Ordering", 612, 430, "pizza_bg.png")

        header_label = tk.Label(root, text="Welcome to the Pizza Palace!", relief="sunken")
        header_label.place(relx = 0.5, rely= 0.1, anchor= "center")

        
        #button purely to test creation of a new window
        #self.open_button = tk.Button(root, text="Open Second Window", command=self.open_second_window)
        #self.open_button.pack(side = "bottom", padx=20, pady=20)

        self.delivery_button = tk.Button(root, text="Delivery", command= self.deliveryButton)
        self.delivery_button.place(relx= 0.5, rely= 0.4)

        self.pickup_button = tk.Button(root, text = "Pickup", command = self.pickupButton)
        self.pickup_button.place(relx= 0.5, rely=0.6)
       
                
    def open_second_window(self):
        #creates a new window
        #self.open_button.config(state=tk.DISABLED)
        second_window = tk.Toplevel(self.root)
        SecondWindow(second_window, self.open_button)

    def buttonRemoval(self):
        #gets rid of the pickup and delivery buttons when one has been selected
        self.delivery_button.destroy()
        self.pickup_button.destroy()
        

    def deliveryButton(self):
        #sets the mode to delivery, *prompt for address, calls for buttonRemoval
        self.buttonRemoval()
        self.open_second_window()

    def pickupButton(self):
        #sets mode to pickup, *prompt for name, calls for buttonRemoval
        self.buttonRemoval()

    def orderCreation(self):
        #called when user chooses delivery or pickup, 
        1

class SecondWindow(BaseWindow):
    def __init__(self, root, open_button):
        super().__init__(root, "Second Window", 400, 300)
        self.open_button = open_button
        
        label = tk.Label(root, text="This is the second window")
        label.pack(padx=20, pady=20)

        root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.open_button.config(state=tk.NORMAL)
        self.root.destroy()

# Create the main application window
if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
