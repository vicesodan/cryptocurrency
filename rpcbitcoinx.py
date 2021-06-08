import requests
import pandas as pd
import pandas_datareader as pdr
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from bitcoinrpc import BitcoinRPC
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from datetime import datetime, timedelta
from tkinter import *
from tkinter import scrolledtext
from PIL import ImageTk, Image


canvas = Tk()
canvas.geometry("1000x600")
canvas.title("BitcoinStats")
canvas.iconbitmap('C:/Users/vices/Desktop/bitcoin.ico')


rpc_connection = AuthServiceProxy("http://%s:%s@blockchain.oss.unist.hr:8332"%(rpc_user, rpc_password))

def clearFrame():
    for widget in frame1.winfo_children():
        widget.destroy()

    for widget in frame2.winfo_children():
        widget.destroy()

    for widget in frame3.winfo_children():
        widget.destroy()

    frame1.pack_forget()
    frame2.pack_forget()
    frame3.pack_forget()


def trenutna_cijena():
    clearFrame()
    frame1.pack(fill="both", expand=1)
    url="https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,JPY,EUR&api_key=06efcda2677d688ac20177063ed6af2a3e341d19db249029ec66e7072c6f932c"
    response = requests.get(url).json()
    price = response["USD"]
    time=datetime.now().strftime("%H:%M:%S")
    image1 = Image.open("C:/Users/vices/Desktop/bitcoin.ico")
    test = ImageTk.PhotoImage(image1)
    label1 = Label(frame1, image=test)
    label1.image = test
    label1.place(x=380, y=250)
    label= Label(frame1, text = "Bitcoin price", font = f1).pack(pady=20)
    label= Label(frame1, text = str(price) + "$", font = f2).pack(pady=10)
    label= Label(frame1, text = "Time: " + time, font = f3).pack(pady=10)
    b= Button(frame1, text = "Refresh!", pady=5, padx=10, command=trenutna_cijena, bg="#f7931a").pack()
    

def blockinfo():
    clearFrame()
    frame2.pack(fill="both", expand=1)
    best_block_hash = rpc_connection.getbestblockhash()
    info=rpc_connection.getblock(best_block_hash)
    label= Label(frame2, text = "Best block hash", font = f1).pack(pady=20)
    label= Label(frame2, text = 'Hash = ' + info['hash']+ '\n\nDifficulty = ' + str(info['difficulty'])+ '\nNonce = ' + str(info['nonce'])+ '\nConfirmations = ' + str(info['confirmations'])+ '\nVersion = ' + str(info['version']) + '\nMerkleroot = ' + str(info['merkleroot']) + '\n\nPreviousBlockHash = \n' + info['previousblockhash'], font = f3).pack()

    
def transactions():
    clearFrame()
    frame3.pack(fill="both", expand=1)
    label= Label(frame3, text = "Transaction list:", font = f2).pack(pady=10)
    text = Text(frame3, cursor="arrow")
    vsb = Scrollbar(frame3, command=text.yview)
    text.configure(yscrollcommand=vsb.set)

    vsb.pack(side="right", fill="y")
    text.pack(side="left", fill="both", expand=True)

    trans = rpc_connection.getrawmempool()
    buttons=[]
    vars=[]
    for i in trans:
        var = IntVar(value=0)
        b= Button(text, text=i, pady=5, padx=300, command=click)
        b.pack()
        text.window_create("end", window=b)
        text.insert("end", "\n")
        buttons.append(b)
        vars.append(var)
    text.configure(state="disabled")

def click():
    top= Toplevel()
    size=rpc_connection.getrawmempool()
    for i in size:
        txid = rpc_connection.getrawtransaction(i, True)
    lbl = Label(top, text= 'Transaction info:', font=f1).pack()
    lbl = Label(top, text= '\n\nHash = ' + txid['hash'] + '\nTxid = ' + str(txid['txid'])+ '\nSize = ' + str(txid['size']) + '\nVsize = ' + str(txid['vsize'])+ '\nWeight = ' + str(txid['weight']), font=f3).pack()

def graf():
    CRYPTO = 'BTC'
    CURRENCY = 'USD'

    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    last_year_date = (now - timedelta(days=365)).strftime("%Y-%m-%d")

    start = pd.to_datetime(last_year_date)
    end = pd.to_datetime(current_date)

    crypto_data = pdr.get_data_yahoo(f'{CRYPTO}-{CURRENCY}', start, end)

    fig = go.Figure(
    data = [
        go.Scatter(
            x = crypto_data.index, 
            y = crypto_data.Close.rolling(window=20).mean(),
            mode = 'lines', 
            name = '20SMA',
            line = {'color': '#ff006a'}
        ),
        ]
    )

    fig.update_layout(
    title = f'The price graph for {CRYPTO}',
    xaxis_title = 'Date',
    yaxis_title = f'Price ({CURRENCY})',
    xaxis_rangeslider_visible = True
    )
    fig.update_yaxes(tickprefix='$')

    fig.show()
    



f1=("poppins", 24, "bold")
f2=("poppins", 22, "bold")
f3=("poppins", 18, "normal")


my_menu = Menu(canvas)
canvas.config(menu=my_menu)

pocetna = Menu(my_menu)
opcije = Menu(my_menu)
blockchain = Menu(my_menu)
popist = Menu(my_menu)



my_menu.add_cascade(label="BTC Price",  menu=opcije)
opcije.add_command(label="BTC Current price", command=trenutna_cijena)
opcije.add_command(label="BTC Price graph", command=graf)
my_menu.add_cascade(label="Block info", command=blockinfo)
my_menu.add_cascade(label="Transaction list", command=transactions)


frame1=Frame(canvas, width=1000, height=600)
frame2=Frame(canvas, width=1000, height=600)
frame3=Frame(canvas, width=1000, height=600)

trenutna_cijena()
canvas.mainloop()



