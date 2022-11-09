import re
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import psycopg2 as db

class ConfigDB(tk.Frame):
    def __init__(self,container,controler):
        tk.Frame.__init__(self,container)
        page_frame = tk.Frame(self)
        page_frame.grid(sticky="nswe")

        #Variables
        username = tk.StringVar()
        password = tk.StringVar()
        db_address = tk.StringVar()
        db_name = tk.StringVar()
        self.db_status = tk.StringVar(value="Status: Desconectado")        

        #Structure
        top_label = tk.Label(page_frame,text="Configuração do Banco de Dados")
        top_label.grid(row=0,column=0,columnspan=100,sticky="nswe")
        ttk.Separator(page_frame, orient='horizontal').grid(column=0, row=1, columnspan=1000, sticky='nswe')
       
        user_label = tk.Label(page_frame,text="Usuário")
        user_label.grid(row=2,column=0,sticky="nswe")

        user_entry = tk.Entry(page_frame,textvariable=username)
        user_entry.grid(row=2,column=1,columnspan=3,sticky="nswe")

        password_label = tk.Label(page_frame,text="Senha")
        password_label.grid(row=3,column=0,sticky="nswe")

        password_entry = tk.Entry(page_frame,textvariable=password,show="*")
        password_entry.grid(row=3,column=1,columnspan=3,sticky="nswe")

        address_label = tk.Label(page_frame,text="IP")
        address_label.grid(row=2,column=4,sticky="nsew")

        address_entry = tk.Entry(page_frame,textvariable=db_address)
        address_entry.grid(row=2,column=5,columnspan=2,sticky="nsew")

        dbname_label = tk.Label(page_frame,text="Nome do BD")
        dbname_label.grid(row=3,column=4,sticky="nsew")

        dbname_entry = tk.Entry(page_frame,textvariable=db_name)
        dbname_entry.grid(row=3,column=5,columnspan=2,sticky="ew")

        database_status = tk.Label(page_frame,textvariable=self.db_status)
        database_status.grid(row=4,column=4,columnspan=2,sticky="nsew")

        submit_button = tk.Button(page_frame,text="Login",command= lambda : self.connect_db(username.get(),password.get(),db_address.get(),db_name.get()))
        submit_button.grid(row=4,column=2, columnspan=1,sticky="ew")
        
    def connect_db(self,username,password,ip,db_name):      
        try:
            self.db_object = db.connect(host='localhost',port='5433', database=db_name,
                                        user=username, password=password)
            
            self.db_status.set("Status: Conectado")  

            self.username = username
            self.password = password
            self.db_name = db_name     
                
        except:
            self.db_status.set("Status: Falha na conexão")
    
    def submit_search(self,query_value,query_type):
        self.connect_db(self.username,self.password,'localhost',self.db_name)
        
        cursor = self.db_object.cursor()
        command = f"SELECT * FROM Alunos WHERE {query_type}='{query_value}';"
        cursor.execute(command)
        result = cursor.fetchall()
        cursor.close()
        self.db_object.close()

        return result

    def submit_forms(self,**kwargs):
        
        self.connect_db(self.username,self.password,'localhost',self.db_name)
        
        nome = kwargs['nome']
        cpf = kwargs['cpf']
        data_nasc = kwargs['data_nasc']
        curso = kwargs['curso']
        sexo = kwargs['sexo']        

        cur = self.db_object.cursor()
        cur.execute("INSERT INTO alunos (nome,cpf,data_nasc,curso,sexo) VALUES (%s,%s,%s,%s,%s)",(nome,cpf,data_nasc,curso,sexo))  
        cur.execute('SELECT * FROM alunos')
        cur.fetchone()  
        self.db_object.commit()    
        cur.close()
        self.db_object.close()
        self.db_status.set("Standby")  

        #Para debug
        command = f"INSERT INTO alunos (nome,cpf,data_nasc,curso,sexo) VALUES ({nome},{cpf},{data_nasc},{curso},{sexo})"      
        print(command)        