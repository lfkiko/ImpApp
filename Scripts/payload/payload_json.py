import sys
from tkinter import *


# root = Tk()
# w = Label(root, text='Please enter your data in here')
# w.pack()
# json_text = Text(root, height=25, width=100)
# submit = Button(root, text='submit', width=25, command=root.destroy)
# cancel = Button(root, text='cancel', width=25, command=root.destroy)
# # t.grid(column=1, row=0)
# json_text.pack()
# submit.pack()
# cancel.pack()
# root.mainloop()

def print_shit(t: str() = "where's my input?"):
	print(t)


# def main(argv):
# 	root = Tk()
# 	root.title('Payload JSON input')
# 	# root.geometry("500X450")
#
# 	w = Label(root, text='Please enter your data in here')
# 	w.pack()
#
# 	json_text = Text(root, height=20, width=60)
# 	json_text.pack(pady=20)
#
# 	button_frame = Frame(root)
# 	button_frame.pack()
#
#
# 	submit = Button(button_frame, text='submit', width=25, command=print_shit("shit"))
# 	submit.grid(row=0, col=0)
# 	cancel = Button(button_frame, text='cancel', width=25, command=root.destroy)
# 	cancel.grid(row=0, col=1)
# 	# t.grid(column=1, row=0)
# 	root.mainloop()


if __name__ == "__main__":
	root = Tk()
	root.title('Payload JSON input')
	# root.geometry("500X450")

	w = Label(root, text='Please enter your data in here')
	w.pack()

	json_text = Text(root, height=20, width=60)
	json_text.pack(pady=20)

	button_frame = Frame(root)
	button_frame.pack()

	submit = Button(button_frame, text='submit', width=25, command=print_shit("shit"))
	submit.grid(row=0, col=0)
	cancel = Button(button_frame, text='cancel', width=25, command=root.destroy)
	cancel.grid(row=0, col=1)
	# t.grid(column=1, row=0)
	root.mainloop()