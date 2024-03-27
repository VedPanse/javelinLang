from tkinter import *

window = Tk()
#CONFIG style/trial.cfg
javelinLang = Label(window, text="javelinLang", fg='black')
javelinLang.place(x=4, y=4)

window.config(bg='blueviolet')
window.geometry('500x800')
window.geometry('800x500')
window.title('javelinLang')
javelinLang.config(bg='blueviolet')
javelinLang.config(font=('', 72))
javelinLang.config(fg='white')
javelinLang.place(x=250.0, y=250.0)

window.mainloop()
