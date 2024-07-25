Pizza Palace Ordering System User Guide: 
run "main.py"
    choose order mode: delivery, or pickup
        if pickup:
            Enter a name to be associated with the order
            Enter a phone number that can be contacted regarding the order (if needed)
        if delivery:
            Enter Street, City, and Zip code, where the order will be delivered
    Click on the "Open Cart" button to open the cart view (Cart View Window will appear)
    Click on "add new item" button in the "cart view" Window (add to cart window will appear)
    Select an item from the drop down menu, adding a note for the item if needed, then click "add Item" to add that item to your cart
        "proceed" button is to close the "add to cart view"
        When the "add item" button is pressed the "add to cart window" will close and the cart in "cart view" will be updated, as well as the total
        When an item is added to the cart, an order summary will also be created on the main menu
        Repeat for each item
    When cart has necessary items, close the cart view window via the X in the corner
        the "proceed to checkout" button on the main menu will appear, click it if you are ready to check out, or open cart if you wish to add or remove items
    "Proceed to checkout" will open the Checkout window
        Will show: the delivery address, if delivery was picked. || The name and contact number if pickup was chosen. 
                all items in the cart, as well as their individual prices
                a subtotal
                the amount of tax based on the current subtotal (7%)
                * a delivery fee, if delivery was chosen
                All of which will be combined to create the final total
            A confirm order button - to confirm your order details. ( will generate an "order confirmed" popup, closing the checkout menu)
            A cancel button, to return to the main menu
