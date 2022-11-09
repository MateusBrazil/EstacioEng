import re
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import psycopg2 as db

class RegisterPage(tk.Frame):
    def __init__(self,container,controler):
        #Page init
        tk.Frame.__init__(self, container)
        page_frame = tk.Frame(self)
        page_frame.grid(sticky="nsew")
        page_frame.configure(background="gray")        
        #end of page init

        #Variables
        self.gender_value = tk.StringVar()
        course_list = ('Pedagogia','Biologia','Letras','Matematica','Fisica','Historia','Admininstração','Psicologia','Direito','Medicina')
        cpf_string = tk.StringVar()       

        self.db_reference = None
        #end of variables

        #Structure        
        top_label = tk.Label(page_frame,text="SISTEMA DE CADASTRO DE ALUNOS")
        top_label.grid(row=0,column=0,columnspan=13,sticky="we")
        ttk.Separator(page_frame, orient='horizontal').grid(column=0, row=1, columnspan=1000, sticky='we')
        name_label = tk.Label(page_frame,text="Nome do Aluno")
        name_label.grid(row=2,column=0)

        self.name_entry = tk.Entry(page_frame)
        self.name_entry.grid(row=2,column=1,sticky="we",columnspan=6)

        cpf_label = tk.Label(page_frame,text="CPF do Aluno")
        cpf_label.grid(row=2,column=8)

        self.cpf_entry = tk.Entry(page_frame,textvariable=cpf_string,)

        self.cpf_entry.grid(row=2,column=9,columnspan=2,sticky="nswe")

        birthday_label = tk.Label(page_frame,text="Data de Nascimento")
        birthday_label.grid(row=4,column=0,columnspan=3,sticky="nswe")
        birthday_entry = Calendar(page_frame)
        #To access later pick the class reference
        self.birthday_entry = birthday_entry
        birthday_entry.grid(row=5,column=0,columnspan=3)

        submit_button = tk.Button(page_frame,text = "Registrar",borderwidth=3,command= lambda : self.db_submit())
        submit_button.grid(row=4,column=4,columnspan=5,sticky="nswe")
        submit_var = tk.StringVar(value="Aguardando ...")
        
        #To access later pick the class reference
        self.submit_var_Reference = submit_var

        submit_status = tk.Label(page_frame,textvariable=submit_var)
        submit_status.grid(row=4,column=10,columnspan=3,sticky="nwse")
        
        gender_label = tk.Label(page_frame,text="Sexo")
        gender_label.grid(row=3,column=0,sticky="nswe")
        
        gender_radio_masc = tk.Radiobutton(page_frame,text="Masculino",variable=self.gender_value,value="Masculino")

        #To access later pick the class reference
        self.gender_radio_reference = gender_radio_masc

        gender_radio_masc.grid(row=3,column=1)
        gender_radio_masc.select()

        gender_radio_fem = tk.Radiobutton(page_frame,text="Feminino",variable=self.gender_value,value="Feminino")
        gender_radio_fem.grid(row=3,column=2)

        course_label = tk.Label(page_frame,text="Curso")
        course_label.grid(row=3,column=8,columnspan=2,sticky="nswe")

        course_combobox = ttk.Combobox(page_frame, values=course_list,state="readonly")

        #To access later pick the class reference
        self.course_combobox_reference = course_combobox

        course_combobox.grid(row=3,column=10,sticky="nswe")
        course_combobox.set("Selecione o Curso")
        #end of structure

    def db_submit(self):
       
        cpf_entry = self.cpf_entry.get()        
        name_entry = self.name_entry.get()
        data_nasc = self.birthday_entry.get_date()
        curso = self.course_combobox_reference.get()
        sexo = self.gender_value.get()

        if not App.cpf_validate(cpf_entry):
            self.submit_var_Reference.set("CPF INVÁLIDO")
            print(cpf_entry)  
            return          
        
        if not App.check_name(name_entry):
            self.submit_var_Reference.set("Nome inválido!")
            print(name_entry)            
            return
        
        if self.course_combobox_reference.get() == "Selecione o Curso":
            self.submit_var_Reference.set("Curso inválido")
            return 

        self.db_reference.submit_forms(nome=name_entry,cpf=cpf_entry,data_nasc=data_nasc,curso=curso,sexo=sexo)
        self.submit_var_Reference.set("Registrado com Sucesso!")
        print(f"Nome: {self.name_entry.get()}\nCPF:{self.cpf_entry.get()}\nSexo: {self.course_combobox_reference.get()}\nData Nascimento: {self.birthday_entry.get_date()}")