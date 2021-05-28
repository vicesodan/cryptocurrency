import requests
import asyncio
from bitcoinrpc import BitcoinRPC
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from datetime import datetime
import matplotlib.pyplot as plt
from tkinter import *
from PIL import ImageTk, Image 


canvas = Tk()
canvas.geometry("1000x600")
canvas.title("BitcoinStats")
canvas.iconbitmap('C:/Users/vices/Desktop/bitcoin.ico')


def trenutna_cijena():
    url="https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,JPY,EUR"
    response = requests.get(url).json()
    price = response["USD"]
    time=datetime.now().strftime("%H:%M:%S")
    image1 = Image.open("C:/Users/vices/Desktop/bitcoin.ico")
    test = ImageTk.PhotoImage(image1)
    label1 = Label(image=test)
    label1.image = test
    label1.place(x=380, y=250)
    labelTitle.config(text = "Cijena Bitcoina", font = f1)
    labelPrice.config(text = str(price) + "$")
    labelTime.config(text = "Vrijeme: " + time)
    
    canvas.after(1000, trenutna_cijena)

def blockinfo():

    rpc_connection = AuthServiceProxy("http://%s:%s@blockchain.oss.unist.hr:8332"%(rpc_user, rpc_password))
    best_block_hash = rpc_connection.getbestblockhash()
    info = Label(canvas, text=(rpc_connection.getblock(best_block_hash))).pack()

def graf():
    #PRIMJER NEKOG GRAFA
    # x axis values
    x = [1,2,3,4,5,6]
    # corresponding y axis values
    y = [2,4,1,5,2,6]
    
    # plotting the points 
    plt.plot(x, y, color='green', linestyle='dashed', linewidth = 3,
             marker='o', markerfacecolor='blue', markersize=12)
    
    # setting x and y axis range
    plt.ylim(1,8)
    plt.xlim(1,8)
    
    # naming the x axis
    plt.xlabel('x - axis')
    # naming the y axis
    plt.ylabel('y - axis')
    
    # giving a title to my graph
    plt.title('Some cool customizations!')
    
    # function to show the plot
    plt.show()

f1=("poppins", 24, "bold")
f2=("poppins", 22, "bold")
f3=("poppins", 18, "normal")

labelTitle = Label(canvas, font=f1)
labelTitle.pack(pady=20)

labelPrice = Label(canvas, font=f2)
labelPrice.pack(pady=20)

labelTime = Label(canvas, font=f3)
labelTime.pack(pady=20)

labelInfo = Label(canvas, font=f3)
labelInfo.pack(pady=20)

my_menu = Menu(canvas)
canvas.config(menu=my_menu)

pocetna = Menu(my_menu)
blockchain = Menu(my_menu)
ggraf = Menu(my_menu)

my_menu.add_cascade(label="Cijena", command=trenutna_cijena)
my_menu.add_cascade(label="BlockInfo", command=blockinfo)
my_menu.add_cascade(label="Graf", command=graf)



canvas.mainloop()



