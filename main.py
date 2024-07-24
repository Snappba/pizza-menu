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
        self.cart=[]
        header_label = tk.Label(root, text="Welcome to the Pizza Palace!", relief="sunken")
        header_label.place(relx = 0.5, rely= 0.1, anchor= "center")

        self.delivery_button = tk.Button(root, text="Delivery", command= self.deliveryButton)
        self.delivery_button.place(relx= 0.5, rely= 0.3, anchor = "center")

        self.pickup_button = tk.Button(root, text = "Pickup", command = self.pickupButton)
        self.pickup_button.place(relx= 0.5, rely=0.7, anchor = "center")

        self.summary_label= tk.Label(root, text="", relief= "sunken")
        self.summary_label.place(relx= 0.9, rely= 0.1, anchor="ne")

        #button to manage items
        self.manage_items_button = tk.Button(root, text = "Open Cart", command = self.open_cart_view, state = "disabled")
        self.manage_items_button.place(relx = 0.5, rely= 0.8, anchor = "center")
        
        #overview window
        self.overview_frame = tk.Frame(root)

        #checkout button - not created until the cart is closed. 
        self.checkout_button = tk.Button(root, text = "Proceed to Checkout", command = self.open_checkout)
        self.summary_mode = None 

    def buttonRemoval(self):
        #gets rid of the pickup and delivery buttons when one has been selected
        self.delivery_button.destroy()
        self.pickup_button.destroy()
        
    def deliveryButton(self):
        #calls for the creation of the delivery window, prompt for address, calls for buttonRemoval
        delivery_window = tk.Toplevel(self.root)
        DeliveryWindow(delivery_window, self)
        self.summary_mode = "delivery"
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

    def create_overview(self):
        self.overview_frame.place(relheight= 0.3, relwidth = 0.3, relx = 0.5, rely= 0.5, anchor= "center")

        #clear existing content in the overview
        for widget in self.overview_frame.winfo_children():
            widget.destroy()

        #create overview content
        overview_label= tk.Label (self.overview_frame, text = "Order Summary", font=("Arial", 16))
        overview_label.pack(pady=10)

        for price, name, note, _ in self.cart:
            display_text= f"{name} - ${price:.2f}"
            if note:
                display_text+= f" (Note: {note})"
            item_label=tk.Label(self.overview_frame, text = display_text)
            item_label.pack()

        total_label= tk.Label(self.overview_frame, text = f"Total: ${sum(item[0] for item in self.cart):.2f}")
        total_label.pack()

    def open_cart_view(self):
        CartView(self.root, self.cart, self)
        self.manage_items_button.config(state = tk.DISABLED)

    def reenable_cart_button(self):
        self.manage_items_button.config(state = tk.NORMAL)
        self.checkout_button.place(relx = 0.9, rely = 0.5, anchor = "center")
        self.checkout_button.config (state = tk.NORMAL)

    def open_checkout(self):
        summary_text = self.summary_label.cget("text")
        
        CheckoutWindow(self.root, self.cart, summary_text, self.summary_mode)
        

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


class CheckoutWindow(tk.Toplevel):
    def __init__(self,root,cart,summary_text, summary_mode):
        super().__init__(root)
        self.title("Checkout")
        self.geometry("400x500")

        tk.Label(self, text = "Order Summary", font = ("Arial",16)).pack(pady=10)


        summary_label = tk.Label(self, text =summary_text)
        summary_label.pack(pady=5)

        #Calculate the subtotal
        subtotal = sum(price for price, name, note, _ in cart)
        tax = subtotal *0.07
        total = subtotal + tax 


        for price, name, note, _ in cart:
            display_text = f"{name} - ${price:.2f}"
            if note:
                display_text += f" (Note: {note})"
            item_label = tk.Label(self, text = display_text)
            item_label.pack()

        

        #display subtotal, tax, then total
        tk.Label(self, text=f"Subtotal: ${subtotal}").pack(pady=5)
        if summary_mode == "delivery":
            delivery_fee = 6.00
            tk.Label(self, text=f"Delivery Fee - ${delivery_fee:.2f}").pack()
            subtotal += delivery_fee  # Add delivery fee to subtotal
            total = subtotal + tax  # Recalculate total with delivery fee
        tk.Label(self, text=f"Tax: ${tax:.2f}").pack(pady=5)
        tk.Label(self, text=f"Total: ${total:.2f}").pack(pady=10)

        tk.Button(self, text="Confirm Order", command=self.confirm_order).pack(pady=5)
        tk.Button(self, text="Cancel", command=self.cancel_order).pack(pady=5)


    def confirm_order(self):
        messagebox.showinfo("Order Confirmed", "Your order has been confirmed!")
        self.destroy()
    
    def cancel_order(self):
        self.destroy()

class CartView(tk.Toplevel):
    def __init__(self, root, cart, main_window):
        super().__init__(root)
        self.title("Cart View")
        self.geometry("400x500")
        self.cart = cart
        self.total = 0
        self.main_window=main_window

        self.cart_with_ids = [(price, name, note, i) for i, (price, name, note, _) in enumerate(self.cart)]

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

        #initialize total label here
        self.total_label = tk.Label(self, text="Total: $0.00")
        self.total_label.pack(side=tk.BOTTOM, pady=5)
        #add new item button
        self.add_item_button = tk.Button(self, text="Add New Item", command=self.open_add_to_cart)
        self.add_item_button.pack(side=tk.BOTTOM, pady=10)

        self.update_items()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.main_window.reenable_cart_button()
        self.main_window.create_overview()
        self.destroy()

    def update_items(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.update_cart()
    def update_cart(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()  # Clear existing items

        self.total = 0  # Reset total to 0 for recalculation
        for price, name, note, item_id in self.cart_with_ids:
            display_text = f"{name} - ${price:.2f}"
            if note:
                display_text += f" (Note: {note})"
            item_frame = tk.Frame(self.content_frame)
            item_frame.pack(fill=tk.X, pady=5)
            tk.Label(item_frame, text=display_text).pack(side=tk.LEFT, padx=5)
            remove_button = tk.Button(item_frame, text="X", command=lambda id= item_id: self.remove_item(id))
            remove_button.pack(side=tk.RIGHT, padx=5)
            self.total += price
        self.total_label.config(text=f"Total: ${self.total:.2f}")

    def open_add_to_cart(self):
        AddToCart(self,self)
    
    def remove_item(self, item_id):
        self.cart_with_ids = [item for item in self.cart_with_ids if item[3] != item_id]
        self.update_items()
        self.main_window.cart = [item for i, item in enumerate(self.main_window.cart) if i != item_id]
        self.main_window.create_overview()

    def add_item_to_cart(self, item_name, price, note, item_id):
        self.cart_with_ids.append((price, item_name, note, item_id))
        self.update_items()
        self.main_window.cart.append((price, item_name, note, item_id))
        self.main_window.create_overview()


class AddToCart(tk.Toplevel):
    def __init__(self, root, cart_view):
        super().__init__(root)
        self.title("Add to Cart")
        self.geometry("500x400")
        self.cart_view = cart_view
        self.menu_items = {
            "Margherita Pizza": (10.00, "Tomato, Mozzarella, Basil"),
            "Pepperoni Pizza": (12.00, "Tomato, Mozzarella, Pepperoni"),
            "Veggie Pizza": (11.00, "Tomato, Mozzarella, Bell Pepper, Onion, Mushroom"),
            "Meat Lovers Pizza": (15.00, "Tomato, Mozzerella, Sausage, Ham, Bacon, Pepperoni, Ground Beef" ),
            "Buffalo Chicken Pizza": (14.00, "Buffalo-ranch, Mozzerlla, Onion, Chicken"),
            "Philly Cheesesteak Pizza": (14.00, "Ranch, Mozzerella, 3 Cheese, Steak, Green Peppers, Onions"),
            "6 Cheese Pizza" : (11.00, "Tomato, Parmesean, Romano, Mozzerella, Provolone, Fontina, Asiago"),
            "Burger Pizza" : (13.00, "'Burger Sauce', Mozzerella, Beef, Pickle, Tomato"),
            "The Works" : (18.00, "Tomato, Mozzerella, Italian Sausage, Canadian Bacon, Mushroom, Onion, Green Pepper, Black Olive, Pepperoni"),
            "BBQ Chicken Pizza" : (14.00, "BBQ, Mozzerella, Chicken, Bacon, Onion"),
            "Hawaiian Pizza" : (12.00, "Tomato, Mozzerella, Canadian Bacon, Bacon, Pineapple, 3 Cheese")
        }

        self.frame = tk.Frame(self)
        self.frame.pack(fill=tk.BOTH, padx=10, pady=10)

        tk.Label(self.frame, text="Select Item:").pack(pady=5)
        self.item_menu = ttk.Combobox(self.frame, values=list(self.menu_items.keys()))
        self.item_menu.set(next(iter(self.menu_items)))
        self.item_menu.pack(pady=5)

        tk.Label(self.frame, text="Note:").pack(pady=5)
        self.note_entry = tk.Entry(self.frame)
        self.note_entry.pack(pady=5)

        add_button = tk.Button(self.frame, text="Add Item", command=self.add_item)
        add_button.pack(pady=5)

        proceed_button = tk.Button(self.frame, text="Proceed", command=self.proceed)
        proceed_button.pack(pady=10)

    def add_item(self):
        item_name = self.item_menu.get()
        note = self.note_entry.get()
        if item_name in self.menu_items:
            price, _ = self.menu_items[item_name]
            item_id = len(self.cart_view.cart_with_ids)
            self.cart_view.add_item_to_cart(item_name, price, note, item_id)
            self.update_cart()
            self.destroy()
        else:
            messagebox.showerror("Item Error", "Selected item is not available.")

    def update_cart(self):
        self.cart_view.update_items()  # Call CartView's update_items method

    def proceed(self):
        self.destroy()


# Create the main application window
if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
