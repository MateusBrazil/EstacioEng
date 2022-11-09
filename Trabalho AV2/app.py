import re
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import psycopg2 as db
from ConfigDB import ConfigDB
from RegisterPage import RegisterPage
from SearchPage import SearchPage

class App(tk.Tk):
    def __init__(self,*args,**kwargs):

        tk.Tk.__init__(self,*args,**kwargs)
        self.geometry("560x300")
        self.resizable(False,False)
        main_container = tk.Frame(self)
        main_container.pack(fill="both",expand=1)

        button_container = tk.Frame(main_container)
        button_container.grid(column=0,sticky="ns",rowspan=10)

        page_container = tk.Frame(main_container)
        page_container.grid(row=0,column=1,sticky="nsew")

        self.createFrames(page_container)

        #Icons
        search_icon = tk.PhotoImage(file="resources/search.png")
        register_icon = tk.PhotoImage(file="resources/register.png")
        database_icon = tk.PhotoImage(file="resources/database.png")

        #Structure
        search_button = tk.Button(button_container,text="Procurar",image=search_icon,compound=tk.TOP,command= lambda : self.raiseFrame(SearchPage))                
        register_button = tk.Button(button_container,text="Registrar",image=register_icon,compound=tk.TOP, command = lambda : self.raiseFrame(RegisterPage))
        database_button = tk.Button(button_container,text="Config DB",image=database_icon,compound=tk.TOP, command =lambda : self.raiseFrame(ConfigDB))

        #Fix the garbage colector bug
        register_button.image = register_icon
        search_button.image = search_icon
        database_button.image = database_icon
        
        #Positioning the elements on the frame
        search_button.pack(side="top")
        register_button.pack(side="top")
        database_button.pack(side="top")

    def createFrames(self,container):
        self.frames = {}

        for F in (ConfigDB,SearchPage,RegisterPage):
            frame = F(container,self)
            frame.grid(row = 1, column = 1, sticky ="nsew")
            self.frames[F] = frame
        
        self.frames[SearchPage].db_reference = self.frames[ConfigDB] 
        self.frames[RegisterPage].db_reference = self.frames[ConfigDB]
            
    def raiseFrame(self,frame_name):
        print(f"Subindo o frame {frame_name}")
        if(frame_name == SearchPage):
            self.geometry("890x300")
        else:
            self.geometry("560x300")
        frame = self.frames[frame_name]
        frame.tkraise()    

    @staticmethod
    def check_name(name):

        if(len(name) < 5):
            return False
        
        for string in name.split(" "):
            if (bool(re.match('^[a-zA-Z]*$',string))==False):
                return False

        return True
    
    #Retirado do seguinte link https://www.vivaolinux.com.br/script/Validador-e-gerador-de-CPF-em-Python#:~:text=Duas%20fun%C3%A7%C3%B5es%20em%20Python%2C%20uma,que%20gera%20um%20CPF%20v%C3%A1lido.&text=from%20random%20import%20randint%20def,d%C3%ADgitos%20if%20len(cpf)%20!%3D
    @staticmethod
    def cpf_validate(numbers):
        #  Obtém os números do CPF e ignora outros caracteres ('-', '.')
        cpf = [int(char) for char in numbers if char.isdigit()]

        #  Verifica se o CPF tem 11 dígitos
        if len(cpf) != 11:
            return False

        #  Verifica se o CPF tem todos os números iguais, ex: 111.111.111-11
        #  Esses CPFs são considerados inválidos mas todos passam na validação dos dígitos.
        #  Antigo código para referência: if all(cpf[i] == cpf[i+1] for i in range (0, len(cpf)-1))
        if cpf == cpf[::-1]:
            return False

        #  Valida os dois dígitos verificadores
        for i in range(9, 11):
            value = sum((cpf[num] * ((i + 1) - num) for num in range(0, i)))
            digit = ((value * 10) % 11) % 10
            if digit != cpf[i]:
                return False
        return True

def startApp():
    app = App()
    app.mainloop()

if __name__ == '__main__':  startApp()
