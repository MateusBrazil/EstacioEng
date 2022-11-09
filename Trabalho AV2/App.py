#Mateus Brazil de Oliveira
#Matricula: 202003447031
import re
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import psycopg2 as db

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


class SearchPage(tk.Frame):
    def __init__(self,container,controler):
        #Page init
        tk.Frame.__init__(self, container)
        page_frame = tk.Frame(self)
        page_frame.grid(sticky="nsew")
        #end of page init

        #variables
        search_text = tk.StringVar()
        search_type = tk.StringVar()

        self.db_reference = None
        #end of variables

        #Structure
        top_label = tk.Label(page_frame,text="CADO - SISTEMA DE GESTÃO DE ALUNOS")
        top_label.grid(row=0,column=0,columnspan=13,sticky="we")
        ttk.Separator(page_frame, orient='horizontal').grid(column=0, row=1, columnspan=1000, sticky='we')

        search_text_label = tk.Label(page_frame, text="Palavra chave")
        search_text_label.grid(row=2,column=0,sticky="nswe")
        search_entry = tk.Entry(page_frame,textvariable=search_text)
        search_entry.grid(row=2,column=1,columnspan=5, sticky="nsew")

        submit_button = tk.Button(page_frame,text="Procurar",command = lambda : self._submit_button(search_text,search_type))
        submit_button.grid(row=2,column=6,columnspan=5,sticky="nsew")

        search_filter_label = tk.Label(page_frame,text="Filtro")
        search_filter_label.grid(row=3,column=0,sticky="nsew")
        search_filter_CPF = tk.Radiobutton(page_frame,text="CPF",variable=search_type,value="cpf")
        search_filter_name = tk.Radiobutton(page_frame,text="Nome",variable=search_type,value="nome")
        search_filter_matricula = tk.Radiobutton(page_frame,text="Matricula",variable=search_type,value="matricula")
        search_filter_curso = tk.Radiobutton(page_frame,text="Curso",variable=search_type,value="curso")
        search_filter_CPF.grid(row=3,column=1,sticky="nsew")
        search_filter_name.grid(row=3,column=2,sticky="nsew")
        search_filter_matricula.grid(row=3,column=3,sticky="nsew")
        search_filter_curso.grid(row=3,column=4,sticky="nsew")

        search_filter_CPF.select()

        style = ttk.Style()
        style.configure('Treeview',columnweight=30)
        table_frame = tk.Frame(page_frame)
        table_frame.grid(row=4,column=0,rowspan=30,columnspan=6,sticky="nsew")
        self._tree = ttk.Treeview(table_frame,columns=('Matricula','Nome','CPF','Data de Nascimento','Curso','Sexo'),show='headings',height=9)

        verscrlbar = ttk.Scrollbar(table_frame,
                           orient ="vertical",
                           command = self._tree.yview)
        verscrlbar.grid(row=1,column=0,rowspan=6,sticky="nsew")

        horizontal_scrollbar = ttk.Scrollbar(table_frame,orient="horizontal",command=self._tree.xview)
        horizontal_scrollbar.grid(row=10,column=1,columnspan=11,sticky="nsew")

        self._tree.column("#1", anchor=tk.CENTER,width=80)
        self._tree.heading("#1", text="Matricula")
        self._tree.column("#2", anchor=tk.CENTER,width=150)
        self._tree.heading("#2", text="Nome")
        self._tree.column("#3", anchor=tk.CENTER,width=150)
        self._tree.heading("#3", text="CPF")
        self._tree.column("#4", anchor=tk.CENTER,width=130)
        self._tree.heading("#4", text="Data de Nascimento")
        self._tree.column("#5", anchor=tk.CENTER,width=110)
        self._tree.heading("#5", text="Curso")
        self._tree.column("#6", anchor=tk.CENTER,width=100)
        self._tree.heading("#6", text="Sexo")

        self._tree.grid(row=1,column=1,columnspan=5,rowspan=2,sticky="nsew")
        #end of structure
   
    def _clear_table(self):
        for item in self._tree.get_children():
            self._tree.delete(item)
   
    def _submit_button(self,search_text,search_type):
       result = self.db_reference.submit_search(search_text.get(),search_type.get())
       print(result)
       self.generate_view(result)

    def generate_view(self,values):
        self._clear_table()
        for row in values:
             self._tree.insert("", tk.END, values=row)

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


def startApp():
    app = App()
    app.mainloop()

if __name__ == '__main__':  startApp()
