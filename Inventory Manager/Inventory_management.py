from tkinter import *
from tkinter import ttk
import sqlite3 as sq
import datetime as dt

root = Tk()
root.title('Inventory Manager')
root.geometry('840x400')

def edit():
    conn = sq.connect('inventory.db')
    c = conn.cursor()

    
    top = Toplevel()
    top.title('Edit Inventory')
    top.geometry('380x400')

    def delete():
        if id_choice.get() == 0:
            return
    
        conn = sq.connect('inventory.db')
        c = conn.cursor()


        c.execute(f"DELETE FROM products WHERE ID={id_choice.get()}")
        for product in inventory_display.get_children():
            if inventory_display.item(product, 'values')[0] == str(id_choice.get()):
                inventory_display.delete(product)
                break

        conn.commit()
        c.close()

        

    def save():
        if input1.get() == '' or input2.get() == '' or input3.get() == '':
            return

        
        conn = sq.connect('inventory.db')
        c = conn.cursor()

        if len(inventory_display.selection()) == 0:
            c.execute(f"INSERT INTO products (Product_Name, Purchase_Price, Amount_Available) VALUES ('{input1.get()}', {input2.get()}, {input3.get()})")


            c.execute("SELECT oid FROM Products")
            ids = list(c.fetchall())[-1]

            inventory_display.insert(parent='', index='end', iid=ids, text='', values=(ids, input1.get(), input2.get(), input3.get()))

        else:
            c.execute(f"UPDATE products SET Product_Name='{input1.get()}' WHERE ID={inventory_display.item(inventory_display.selection()[0], 'values')[0]}")
            c.execute(f"UPDATE products SET Purchase_Price='{input2.get()}' WHERE ID={inventory_display.item(inventory_display.selection()[0], 'values')[0]}")
            c.execute(f"UPDATE products SET Amount_Available='{input3.get()}' WHERE ID={inventory_display.item(inventory_display.selection()[0], 'values')[0]}")
            inventory_display.item(inventory_display.item(inventory_display.selection()[0], 'values')[0] ,text='', values=(inventory_display.item(inventory_display.selection()[0], 'values')[0], input1.get(), input2.get(), input3.get()))
            if len(inventory_display.selection()) > 0:
                inventory_display.selection_remove(inventory_display.selection()[0])
            print(inventory_display.selection())


        input1.delete(0, END)
        input2.delete(0, END)
        input3.delete(0, END)


        conn.commit()
        c.close()
        

    frame_information = LabelFrame(top)
    frame_information.grid(row=0, column=0, padx=10, pady=10)


    Label1 = Label(frame_information, text='Product Name')
    Label1.grid(row=0, column=0, pady=10, padx=10)
    Label2 = Label(frame_information, text='Pruchase Price')
    Label2.grid(row=1, column=0, pady=10, padx=10)
    Label3 = Label(frame_information, text='Amount Available')
    Label3.grid(row=2, column=0, pady=10, padx=10)



    input1 = Entry(frame_information)
    input1.grid(row=0, column=1, padx=(20, 10))
    input2 = Entry(frame_information)
    input2.grid(row=1, column=1, padx=(20, 10))
    input3 = Entry(frame_information)
    input3.grid(row=2, column=1, padx=(20, 10))

    save_button = Button(top, text='Save', command=save)
    save_button.grid(row=1, column=0, ipadx=100, pady=10)

    if len(inventory_display.selection()) != 0:
        input1.insert(END , inventory_display.item(inventory_display.selection()[0], 'values')[1])
        input2.insert(END , inventory_display.item(inventory_display.selection()[0], 'values')[2])
        input3.insert(END , inventory_display.item(inventory_display.selection()[0], 'values')[3])


    
    c.execute("""SELECT oid FROM products""")

    ids = [number[0] for number in list(c.fetchall())]

    if len(ids) > 0:
        frame_delete = LabelFrame(top)
        frame_delete.grid(row=2, column=0)
        delete_button = Button(frame_delete, text='Delete', command=delete)
        delete_button.grid(row=0, column=0, padx=10)
        frame_delete_dropdown_label = LabelFrame(frame_delete)  
        frame_delete_dropdown_label.grid(row=0, column=1)
        label_delete_dropdown = Label(frame_delete_dropdown_label, text='ID:')
        label_delete_dropdown.grid(row=0, column=0)
        id_choice = IntVar()
        OptionMenu(frame_delete_dropdown_label, id_choice, *ids).grid(row=0, column=1)


    conn.commit()
    c.close()
    

def sale():

    conn = sq.connect('inventory.db')
    c = conn.cursor()

    top = Toplevel()
    top.title("Sales Information")
    top.geometry('1040x600')

    frame_sales_so_far = LabelFrame(top)
    frame_sales_so_far.grid(row=0, column=0, padx=20, pady=20)
    Label(frame_sales_so_far, text='Sales So Far').pack()

    sales_display = ttk.Treeview(frame_sales_so_far)
    sales_display['columns'] = ('ID','Product Name', 'Date Sold', 'Selling Price', 'Quantity Sold')
    sales_display.column('#0', width=0, stretch=NO)
    sales_display.column('ID', anchor=CENTER)
    sales_display.column('Product Name', anchor=W)
    sales_display.column('Date Sold', anchor=W)
    sales_display.column('Selling Price', anchor=W)
    sales_display.column('Quantity Sold', anchor=W)

    sales_display.heading('ID', text='ID Number', anchor=CENTER)
    sales_display.heading('Product Name', text='Product Name', anchor=W)
    sales_display.heading('Date Sold', text='Date Sold', anchor=W)
    sales_display.heading('Selling Price', text='Selling Price', anchor=W)
    sales_display.heading('Quantity Sold', text='Quantity Sold', anchor=W)

    sales_display.pack()


    c.execute("SELECT * FROM products")
    records = c.fetchall()

    
    products = []
    for record in records:
        products.append(record[1])


    if len(products) > 0:
        def delete():
            if delete_selection.get() == 0:
                return

            conn = sq.connect('inventory.db')
            c = conn.cursor()

            c.execute(f"DELETE FROM sales WHERE ID={delete_selection.get()}")

            for sale in sales_display.get_children():
                if sales_display.item(sale, 'values')[0] == str(delete_selection.get()):
                    sales_display.delete(sale)
                    break
            

            

            conn.commit()
            c.close()


        
        def submit():
            conn = sq.connect('inventory.db')
            c = conn.cursor()

            date = dt.date(year.get(), month.get(), day.get())

            c.execute(f"INSERT INTO sales(Product_Name, Date_Sold, Selling_Price, Quantity_Sold) VALUES ('{prod_name_choice.get()}', '{str(date)}', {sell_price.get()}, {amount_chosen.get()})")
            c.execute("SELECT * FROM sales")
            ids = c.fetchall()[-1][0]
            sales_display.insert(parent='', index='end', iid=ids, text='', values=(ids, prod_name_choice.get(), str(date), sell_price.get(), amount_chosen.get()))


            c.execute(f"SELECT * FROM products WHERE Product_Name='{prod_name_choice.get()}'")
            quantity = c.fetchall()[0][-1]
            
            c.execute(f"""UPDATE products SET Amount_Available={int(quantity) - int(amount_chosen.get())} WHERE Product_Name='{prod_name_choice.get()}'""")

            if int(quantity) - int(amount_chosen.get()) == 0:
                c.execute("DELETE FROM products WHERE Amount_Available=0")
                for product in inventory_display.get_children():
                    if inventory_display.item(product, 'values')[1] == str(prod_name_choice.get()):
                        inventory_display.delete(product)
                        break
                

            conn.commit()
            c.close()

            

        
        def deploy_quantity_dropdown(*args):
            conn = sq.connect('inventory.db')
            c = conn.cursor()

            c.execute("SELECT * FROM products")
            records = c.fetchall()

            
            for record in records:
                if record[1] == prod_name_choice.get():
                    max_quantity = record[-1]
                    break

            global amount_chosen
            amount_chosen = IntVar()
            OptionMenu(frame_add_sales, amount_chosen, *[i for i in range(1, max_quantity + 1)]).grid(row=4, column=1)


            conn.commit()
            c.close()

        
        frame_add_sales = LabelFrame(top)
        frame_add_sales.grid(row=1, column=0, pady=10)
        Label(frame_add_sales, text='Add A New Sale').grid(row=0, column=0, columnspan=2)

        Label1 = Label(frame_add_sales, text='Product Name')
        Label1.grid(row=1, column=0, pady=10, padx=10)
        Label2 = Label(frame_add_sales, text='Date Sold')
        Label2.grid(row=2, column=0, pady=10, padx=10)
        Label3 = Label(frame_add_sales, text='Selling Price')
        Label3.grid(row=3, column=0, pady=10, padx=10)
        Label4 = Label(frame_add_sales, text='Quantity Sold')
        Label4.grid(row=4, column=0, pady=10, padx=10)


        prod_name_choice = StringVar()
        OptionMenu(frame_add_sales, prod_name_choice, *products).grid(row=1, column=1)
        frame_dates = LabelFrame(frame_add_sales)
        frame_dates.grid(row=2, column=1)
        year = IntVar()
        OptionMenu(frame_dates, year, *[i for i in range(1980, int(dt.date.today().year) + 1)]).grid(row=0, column=0)
        month = IntVar()
        OptionMenu(frame_dates, month, *[i for i in range(1,13)]).grid(row=0, column=1)
        day = IntVar()
        OptionMenu(frame_dates, day, *[i for i in range(1,32)]).grid(row=0, column=2)
        sell_price = Entry(frame_add_sales)
        sell_price.grid(row=3, column=1, padx=10)


        prod_name_choice.trace_add('write', deploy_quantity_dropdown)

        submit = Button(frame_add_sales, text='Submit', command=submit)
        submit.grid(row=5, column=0, columnspan=2)

        delete_frame = LabelFrame(top)
        delete_frame.grid(row=2, column=0)
        delete_button = Button(delete_frame, text='Delete', command=delete)
        delete_button.grid(row=0, column=0, padx=10)
        delete_selection = IntVar()

        c.execute('SELECT * FROM sales')
        records = c.fetchall()
        ids = []
        for record in records:
            ids.append(record[0])

        
        OptionMenu(delete_frame, delete_selection, *ids).grid(row=0, column=1, padx=10)
            
        



    c.execute('SELECT * FROM sales')
    records = c.fetchall()

    for record in records:
        sales_display.insert(parent='', index='end', iid=record[0], text='', values=record)



    
    
    

        
    conn.commit()
    c.close()



    


conn = sq.connect('inventory.db')
c = conn.cursor()

'''
c.execute("""CREATE TABLE products (
          ID INTEGER PRIMARY KEY,
          Product_Name TEXT,
          Purchase_Price REAL,
          Amount_Available INTEGER)""")


c.execute("""CREATE TABLE sales (
          ID INTEGER PRIMARY KEY,
          Product_Name TEXT,
          Date_Sold TEXT,
          Selling_Price REAL,
          Quantity_Sold INTEGER)""")
'''


frame_intro = LabelFrame(root, relief='groove')
frame_intro.grid(row=0, column=0, padx=20, pady=10, ipadx=30)
label_intro = Label(frame_intro, text='Welcome to the Inventory Management System')
label_intro.pack()


inventory_display = ttk.Treeview(root)
inventory_display['columns'] = ('ID', 'Product Name', 'Purchase Price', 'Amount Available')
inventory_display.column('#0', width=0, stretch=NO)
inventory_display.column('ID', anchor=CENTER)
inventory_display.column('Product Name', anchor=W)
inventory_display.column('Purchase Price', anchor=W)
inventory_display.column('Amount Available', anchor=W)

inventory_display.heading('ID', text='ID Number', anchor=CENTER)
inventory_display.heading('Product Name', text='Product Name', anchor=W)
inventory_display.heading('Purchase Price', text='Purchase Price', anchor=W)
inventory_display.heading('Amount Available', text='Amount Available', anchor=W)

c.execute("""SELECT * FROM products""")
records = c.fetchall()

for record in records:
    inventory_display.insert(parent='', index='end', iid=record[0], text='', values=record)

inventory_display.grid(row=1, column=0, padx=20)

frame_buttons = LabelFrame(root, relief='groove')
frame_buttons.grid(row=2, column=0, pady=20)
edit_inventory = Button(frame_buttons, text='Edit Inventory', command=edit)
edit_inventory.grid(row=0, column=0, padx=10)
sales_button = Button(frame_buttons, text=' Access Sales', command=sale)
sales_button.grid(row=0, column=1, padx=10)



conn.commit()
c.close()

root.mainloop()
