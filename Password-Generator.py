from tkinter import *
import pyperclip as pc
import random as rd

root = Tk()
root.title("Password Generator")
root.geometry("400x600")

def contains(word, context):
    for i in word:
        if i in context:
            return True
    return False


def generate():
    
    alphabets = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    numbers = '1234567890'
    special_chars = '!@#$%^&*()_+{}|:<>?/.,;\][=-'
    chars = ''
    password = ''

    if input_password_length.get() == '' or int(input_password_length.get()) <  5:
        Label(root, text='Secure password must be atleast 5 characters long!').grid(row=4, column=0)
        return

    
    if len(root.grid_slaves(row=4)) > 0:
        root.grid_slaves(row=4)[0].destroy()
    
    if password_type.get() == 1:
        chars += numbers
    elif password_type.get() == 2:
        chars += alphabets
    else:
        chars += numbers + alphabets

    if special_characters.get() == 'yes':
        chars += special_chars
    
    
    for i in range(int(input_password_length.get())):
        password += rd.choice(chars)

    if password_type.get() == 1 and not contains(password, numbers):
        generate()
    elif password_type.get() == 2 and not contains(password, alphabets):
        generate()
    elif password_type.get() == 3 and (not contains(password, numbers) or not contains(password, alphabets)):
        generate()

    if special_characters.get() == 'yes' and not contains(password, special_chars):
        generate()
        
    print(password)

    frame_display_password = LabelFrame(root)
    frame_display_password.grid(row=4, column=0)
    Label(frame_display_password, text=f'{password}').grid(row=0, column=0)
    Button(frame_display_password, text='copy', command=lambda:pc.copy(password)).grid(row=0, column=1)



# Making the Intro Widget
frame_intro = LabelFrame(root, borderwidth=5, relief='groove')
frame_intro.grid(row=0, column=0, padx=30, ipadx=50, pady=20)
label_intro = Label(frame_intro, text="Welcome to the password generator!")
label_intro.pack()

# Making the Widget to get password length
frame_password_length = LabelFrame(root, relief='raised')
frame_password_length.grid(row=1, column=0, pady=(0, 20))
label_password_length = Label(frame_password_length, text="How long is your password?")
label_password_length.grid(row=0, column=0, ipady=10)
input_password_length = Entry(frame_password_length)
input_password_length.grid(row=0, column=1)

# Making the widget to get password type
frame_password_type = LabelFrame(root, relief='raised')
frame_password_type.grid(row=2, column=0)
label_password_type = Label(frame_password_type, text="What type of characters do you want in your password?")
label_password_type.pack()
password_type = IntVar()
Radiobutton(frame_password_type, variable=password_type, value=1, text='Numeric', anchor='w').pack(anchor='w')
Radiobutton(frame_password_type, variable=password_type, value=2, text='Alphabets', anchor='w').pack(anchor='w')
Radiobutton(frame_password_type, variable=password_type, value=3, text='Alphanumeric', anchor='w').pack(anchor='w')
password_type.set(1)
special_characters = StringVar()
special_characters_checkbutton = Checkbutton(frame_password_type, text='*Include Special Characters', variable=special_characters, onvalue='yes', offvalue='no', anchor='w')
special_characters_checkbutton.pack(anchor='w')
special_characters.set('yes')

# Making the button to generate password
button_password_generate = Button(root, text='Generate Password', command=generate)
button_password_generate.grid(row=3, column=0, pady=20)


