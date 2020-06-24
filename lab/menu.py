from tkinter import *
import aiohttp
import pandas as pd

root = Tk()
mylabel1 = Label(root,text="Twitter sentiment analysis tool")
mylabel2 = Label(root,text="  - desinged by Noven")

# mylabel1.grid(row=0,column=0)
# mylabel2.grid(row=1,column=6)

mybutton = Button(root, text = "start analysis",padx = 50,pady=50)
mybutton.pack()
root.mainloop()


if __name__ == "__main__":
    the_file = pd.read_csv('news\\corona.csv')
    