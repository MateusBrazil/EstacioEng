import re
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import psycopg2 as db

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