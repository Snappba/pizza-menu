import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

class BaseWindow:
    #basic, shared attributes for other windows to be created with. 
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
    #the main window, which holds the order summary. 
    def __init__(self, root):
        super().__init__(root, "Pizza Palace Ordering", 612, 430, "pizza_bg.png")

        header_label = tk.Label(root, text="Welcome to the Pizza Palace!", relief="sunken")
        header_label.place(relx = 0.5, rely= 0.1, anchor= "center")

        self.delivery_button = tk.Button(root, text="Delivery", command= self.deliveryButton)
        self.delivery_button.place(relx= 0.5, rely= 0.4, anchor = "center")

        self.pickup_button = tk.Button(root, text = "Pickup", command = self.pickupButton)
        self.pickup_button.place(relx= 0.5, rely=0.6, anchor = "center")

        self.summary_label= tk.Label(root, text="", relief= "sunken")
        self.summary_label.place(relx= 0.9, rely= 0.1, anchor="ne")

        #button to manage items
        self.manage_items_button = tk.Button(root, text = "manage items", command = self.open_cart_view, state = "disabled")
        self.manage_items_button.place(relx = 0.5, rely= 0.8, anchor = "center")
        

    def buttonRemoval(self):
        #gets rid of the pickup and delivery buttons when one has been selected
        self.delivery_button.destroy()
        self.pickup_button.destroy()
        
    def deliveryButton(self):
        #calls for the creation of the delivery window, prompt for address, calls for buttonRemoval
        delivery_window = tk.Toplevel(self.root)
        DeliveryWindow(delivery_window, self)
        delivery_window.grab_set()
        self.buttonRemoval()
        
    def pickupButton(self):
        #calls for creation of the Pickup window prompt for name & contact, calls for buttonRemoval
        pickup_window = tk.Toplevel(self.root)
        PickupWindow(pickup_window, self)
        pickup_window.grab_set() # keeps it on top
        self.buttonRemoval()

    def update_summary(self, mode, *args):
        if mode == "delivery":
            summary = f"Delivery to:\n{args[0]}, \n{args[1]}, {args[2]}"
            self.summary_label.config(text=summary)
        elif mode == "pickup":
            summary = f"Pickup for:\n{args[0]}\n Contact: {args[1]}"
        self.summary_label.config(text=summary)

    def open_cart_view(self):
        CartView(self.root)

class DeliveryWindow(BaseWindow):
    #defines the delivery window, inheriting from the basewindow class
    def __init__(self,root, main_window):
        super().__init__(root, "Enter Delivery Address", 300, 250)
        self.main_window= main_window
        
        tk.Label(root, text ="Street:").pack (pady= 5)
        self.street_entry = tk.Entry(root)
        self.street_entry.pack(pady=5)

        tk.Label(root, text="City:").pack(pady=5)
        self.city_entry = tk.Entry(root)
        self.city_entry.pack(pady=5)

        tk.Label(root, text="Zip Code:").pack(pady=5)
        self.zip_entry = tk.Entry(root)
        self.zip_entry.pack(pady=5)

        save_button = tk.Button(root, text="Save", command=self.save_address)
        save_button.pack(pady=10)

    def save_address(self):
        street= self.street_entry.get()
        city= self.city_entry.get()
        zip_code= self.zip_entry.get()
        

        if not street or not city or not zip_code:
            empty_fields = []
            if not street:
                empty_fields.append("Street")
            if not city:
                empty_fields.append("City")
            if not zip_code:
                empty_fields.append("Zip Code")
            messagebox.showerror("Input Error", f"{', '.join(empty_fields)} cannot be empty")
        else:
            self.main_window.update_summary("delivery", street, city, zip_code)
            self.root.destroy()
        self.main_window.manage_items_button.config(state=tk.NORMAL)

class PickupWindow(BaseWindow):
    #defines the pickup window, inheriting from the basewindow class
    def __init__(self,root,main_window):
        super().__init__(root, "Name for Pickup", 300, 200)
        self.main_window = main_window
        
        tk.Label(root, text="Please provide a name for the order:").pack(pady=5)
        self.name_on_order_entry = tk.Entry(root)
        self.name_on_order_entry.pack(pady=5)

        tk.Label(root, text= "Please provide a contact number:").pack (pady=5)
        self.contact_number_entry = tk.Entry(root)
        self.contact_number_entry.pack(pady=5)
        
        save_button = tk.Button(root, text= "Save", command = self.save_reference)
        save_button.pack(pady=10)

    def save_reference(self):
        contact_number= self.contact_number_entry.get()
        name_on_order = self.name_on_order_entry.get()
        
        #makes sure there are no empty fields before closing the window
        if not name_on_order or not contact_number:
            empty_fields = []
            if not name_on_order:
                empty_fields.append("Name")
            if not contact_number:
                empty_fields.append("Contact Number")
            messagebox.showerror("Input Error", f"{', '.join(empty_fields)} cannot be empty")
        else:
            self.main_window.update_summary("pickup", name_on_order, contact_number)
            self.root.destroy()
        self.main_window.manage_items_button.config(state=tk.NORMAL)

class CartView(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.title("Cart View")
        self.geometry("400x300")

        self.item_frame = tk.Frame(self)
        self.item_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.scrollbar = tk.Scrollbar(self.item_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = tk.Canvas(self.item_frame, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar.config(command=self.canvas.yview)

        self.content_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.content_frame, anchor=tk.NW)

        self.content_frame.bind("<Configure>", lambda e: self.canvas.config(scrollregion=self.canvas.bbox("all")))

        self.add_item_button = tk.Button(self, text="Add New Item", command=self.open_add_to_cart)
        self.add_item_button.pack(side=tk.BOTTOM, pady=10)

        self.items = []

    def open_add_to_cart(self):
        AddToCart(self)

    def add_item_to_cart(self, item_name, price):
        item_frame = tk.Frame(self.content_frame)
        item_frame.pack(fill=tk.X, pady=5)

        item_label = tk.Label(item_frame, text=f"{item_name} - ${price:.2f}")
        item_label.pack(side=tk.LEFT, padx=5)

        remove_button = tk.Button(item_frame, text="Remove", command=lambda: self.remove_item(item_frame))
        remove_button.pack(side=tk.RIGHT, padx=5)

        self.items.append(item_frame)
        self.canvas.yview_moveto(1)

    def remove_item(self, item_frame):
        if item_frame in self.items:
            self.items.remove(item_frame)
            item_frame.destroy()
            for idx, item in enumerate(self.items):
                item.pack_configure(pady=(5 if idx == 0 else 2))


class AddToCart(BaseWindow):
    def __init__(self, cart_view):
        super().__init__(tk.Toplevel(cart_view), "Add to Cart", 400, 300)
        self.cart_view = cart_view

        # Define the menu items, their prices, and their ingredients using a dict
        self.menu_items = {
            "Margherita Pizza": (10.00, "Tomato, Mozzarella, Basil"),
            "Pepperoni Pizza": (12.00, "Tomato, Mozzarella, Pepperoni"),
            "Veggie Pizza": (11.00, "Tomato, Mozzarella, Bell Peppers, Onions, Mushrooms"),
            # Add more items as needed
        }

        # Create a frame for the dropdown and buttons
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, padx=10, pady=10)

        # Create dropdown for selecting an item
        tk.Label(self.frame, text="Select Item:").pack(pady=5)
        self.item_menu = ttk.Combobox(self.frame, values=list(self.menu_items.keys()))
        self.item_menu.set(next(iter(self.menu_items)))  # Set default value to the first item
        self.item_menu.pack(pady=5)

        # Add button to add selected item
        add_button = tk.Button(self.frame, text="Add Item", command=self.add_item)
        add_button.pack(pady=5)

        # Listbox to display cart items
        self.cart_listbox = tk.Listbox(self.frame, width=50, height=10)
        self.cart_listbox.pack(pady=10)

        # Label to display total price
        self.total_label = tk.Label(self.frame, text="Total: $0.00")
        self.total_label.pack(pady=5)

        # Add a button to proceed or exit
        proceed_button = tk.Button(self.frame, text="Proceed", command=self.proceed)
        proceed_button.pack(pady=10)

    def add_item(self):
        item_name = self.item_menu.get()  # Get selected item from Combobox
        if item_name in self.menu_items:
            price, _ = self.menu_items[item_name]
            self.cart_view.add_item_to_cart(item_name, price)
        else:
            messagebox.showerror("Item Error", "Selected item is not available.")

    def proceed(self):
        # Handle proceeding logic (if needed)
        self.root.destroy()



# Create the main application window
if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
