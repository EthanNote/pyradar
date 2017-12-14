from tkinter import *
root = Tk()

root.title("窗口测试")




def eventhandler(event):
    print('！')


btn = Button(root, text='button')
btn.bind_all('<F1>',eventhandler)
btn.pack()

root.mainloop()