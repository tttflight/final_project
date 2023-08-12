from tkinter import Tk

from final_project import *


def main():
    window = Tk()
    window.title("Snack Shack")
    window.geometry('400x500')
    window.resizable(False, False)

    ShoppingCartApp(window)
    window.mainloop()


if __name__ == "__main__":
    main()
