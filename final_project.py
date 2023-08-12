import tkinter as tk
import csv


class ShoppingCartApp:
    def __init__(self, window: tk.Tk) -> None:
        """
        Funtion purpose: Responsible for most of the gui interface by
        establishing variables, buttons, titles etc..
        :param window: None
        """
        self.window = window
        self.items = {"Cookie": 2.00, "Sandwich": 6.00, "Water": 2.00, "Candy": 1.00, "Soda": 3.00}
        self.__item_counts = {"Cookie": 0, "Sandwich": 0, "Water": 0, "Candy": 0, "Soda": 0}
        self.__grand_count = 0
        self.__total_price = 0.0

        self.menu_label = tk.Label(self.window, text="Menu:")
        self.menu_label.pack()

        self.menu_display = tk.Text(self.window, height=6, width=30)
        for item, price in self.items.items():
            self.menu_display.insert(tk.END, f"{item}: ${price:.2f}\n")
            self.menu_display.tag_configure("center", justify="center")
            self.menu_display.tag_add("center", "1.0", "end")
        self.menu_display.pack()

        self.item_label = tk.Label(self.window, text="Enter the item quantity you would like in the boxes below.")
        self.item_label.pack()

        self.item_entries = {}
        for item in self.items:
            item_frame = tk.Frame(self.window)
            item_label = tk.Label(item_frame, text=item)
            item_label.pack(side=tk.LEFT)
            item_entry = tk.Entry(item_frame)
            item_entry.pack(side=tk.LEFT)
            self.item_entries[item] = item_entry
            item_frame.pack()

        self.add_button = tk.Button(self.window, text="Add Items", command=self.add_to_cart)
        self.add_button.pack()

        self.cart_label = tk.Label(self.window, text="Shopping Cart:")
        self.cart_label.pack()

        self.cart_display = tk.Text(self.window, height=7, width=40)
        self.cart_display.pack()

        self.total_label = tk.Label(self.window, text="Grand Total: $0.00")
        self.total_label.pack()

        self.exit_button = tk.Button(self.window, text="Exit", command=self.save_and_quit)
        self.exit_button.pack()

    def add_to_cart(self) -> None:
        """
        Function purpose: Gets the user's input and determines
        if it's valid before updating the totals.
        :return: None
        """
        self.__total_price = 0.0
        self.__grand_count = 0

        for item, entry in self.item_entries.items():
            try:
                quantity = int(entry.get())
                if quantity < 0:
                    raise TypeError
                self.__item_counts[item] = quantity
                item_price = self.items[item]

                if quantity > 0:
                    self.__total_price += item_price * quantity
                    self.__grand_count += quantity

            except TypeError:
                self.item_label.config(text="Please enter positive whole numbers only.")
                return

            except ValueError:
                if entry.get() != "":
                    self.item_label.config(text="Please enter only whole numbers for the item quantities.")
                    return
                else:
                    continue # If user leaves a box blank

        self.item_label.config(text="Enter the item quantity you would like in the boxes below.")  # Reset label
        self.clear_entry_fields()  # Clear all entry fields
        self.update_cart_display()

    def clear_entry_fields(self) -> None:
        """Clears the contents of all user input entry fields."""
        for entry in self.item_entries.values():
            entry.delete(0, tk.END)

    def update_cart_display(self) -> None:
        """
        Function purpose: Takes the updated data in the variables
        and updates the cart information on the display.
        :return: None
        """
        self.cart_display.delete(1.0, tk.END)
        for item, count in self.__item_counts.items():
            if count > 0:
                item_total = self.items[item] * count
                self.cart_display.insert(tk.END, f"{item}: {count} x ${self.items[item]:.2f} = ${item_total:.2f}\n")
                self.cart_display.tag_configure("center", justify="center")
                self.cart_display.tag_add("center", "1.0", "end")
        self.total_label.config(text=f"GRAND TOTAL: ${self.__total_price:.2f}")

    def save_and_quit(self) -> None:
        """
        Function purpose: Writes the data it takes from the
        user's input on the gui and writes it to a csv before
        closing the gui.
        :return: None
        """
        with open("data.csv", "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Category", "Total Quantity", "Total Cost"])
            for item, count in self.__item_counts.items():
                if count > 0:
                    csv_writer.writerow([item, count, "${:.2f}".format(self.items[item] * count)])
            csv_writer.writerow(["GRAND TOTAL:", self.__grand_count, "${:.2f}".format(self.__total_price)])

        self.window.quit()



