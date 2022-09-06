
#Q2 - Aula 3
#Voltando ao cenário apresentado na situação-problema, que trata de um sistema de registro de notas
#de alunos em uma pequena instituição de ensino, desenvolver uma solução capaz de persistir

#Aluno: Mateus Brazil de Oliveira - Matricula: 202003447031

database = "alunos.txt"

def convert_to_csv():
    pass

#Abre e fecha o arquivo, caso ele não exista, ele cria um.
def verifica_arquivo():
    with open(database,"a"):pass    

#Extrai e trata os dados da linha que esta sendo lida
def extrai_dados(linha):
    index_nome = linha.find("nome:")
    index_email = linha.find("email:")
    index_curso = linha.find("curso:")
    
    nome = linha[index_nome+5:linha.find(";",index_nome)]
    email = linha[index_email+6:linha.find(";",index_email)]
    curso = linha[index_curso+6:linha.find(";",index_curso)]

    return nome,email,curso

#Pesquisa o aluno pelo nome e retorna positivo caso encontre a correspondência exata
def pesquisa_aluno(aluno):
    
    arquivo_array = txt_array(database)
    tamanho_array = len(arquivo_array)

    for i,linha in enumerate(arquivo_array):
        nome,email,curso = extrai_dados(linha)
        if nome.lower() == aluno.lower():
            #print(f"Nome: {nome}\nE-mail:{email}\nCurso:{curso}\n")
            return True
        elif i == tamanho_array-1:
            return False

#Recebe o nome de um arquivo e retorna um array com todas as linhas do arquivo
def txt_array(arquivo):
    txt_array = []
    with open(arquivo,"r") as f:
        txt_array = f.readlines()
    return txt_array
    
def cadastra_aluno(nome,email,curso):
    dados = "nome:"+nome+";"+"email:"+email+";"+"curso:"+curso+";"
    if not pesquisa_aluno(nome):
        with open(database,"a") as f:
            f.write(dados)
            f.write("\n")
            print("\nAluno cadastrado com sucesso!\n")
            return True
    else:
        print("Aluno já cadastrado")
        return False

def listar_alunos():
    with open(database,"r") as f:
        for linha in txt_array(database):
            nome,email,curso = extrai_dados(linha)
            print(f"Nome: {nome} - E-mail: {email} - Curso: {curso}")

def check_nome(nome):
    nome = nome.replace(" ","")
    if nome.isalpha() and nome.isascii():
        return True
    else:
        return False

def check_email(email):
    if email.find("@") != -1 and email.find(".",email.find("@")) != -1:
        return True
    else:
        return False

def check_curso(curso):
    curso = curso.replace(" ","")
    if curso.isalpha() and curso.isascii():
        return True
    else:
        return False

#Interface de cadastro de alunos(CMD)
def cadastra_aluno_interface():
    nome, email, curso = "","",""
    controle = True
    print("### Cadastro de Alunos ###")

    while controle:
        
        while True:
            print("Insira o nome do aluno.")
            nome = input("Nome: ").title()
            if not check_nome(nome):
                print("O nome contem caracteres especiais!!\nPor favor, verifique!")
                nome = ""
                continue
            break

        while True:
            print("Insira o email do aluno.")
            email = input("Email: ").casefold()
            if not check_email(email):
                print("Verifique o formato do e-mail")
                email = ""
                continue
            break
        
        while True:
            print("Insira o curso do aluno")
            curso = input("Curso: ").title()
            if not check_curso(curso):
                print("O nome do curso contem caracteres especiais!!")
            break
        
        while controle:
            print(f"Deseja cadastrar o seguinte aluno?\nNome: {nome} Email: {email} Curso: {curso}")
            print("(1) Sim (2) Não (3) Sair")
            opcao = input()
            if opcao == "1":
                controle = False
            elif opcao == "2":
                nome, email, curso = "","",""
                print("Apagando dados e retornando... \n\n\n")
                break
            elif opcao == "3":
                print("Retornando ...")
                return
            else:
                print("Opcao invalida! Tente novamente\n")
                continue
    
    cadastra_aluno(nome,email,curso)

    print("Deseja continuar incluindo alunos?")
    print("(1) Sim (2) Não")
    opcao = input()
    
    if opcao == "1":
        cadastra_aluno_interface()
    elif opcao == "2":
        return
    else:
        print("\nOpcao incorreta! Retornando ao menu...")

#Menu de opções principal
def opcoes():

    #Verifica se o arquivo existe, caso não cria um.
    verifica_arquivo()

    while True:
        print("\n\n### Sistema de alunos ###")
        print("Digite: (1) Para pesquisar aluno (2) Para cadastrar um aluno (3) Listar Alunos (4) Sair")
        opcao = input("insira a opcao --> ")

        if opcao == "1":
            print("Insira o nome do aluno para efetuar a pesquisa!")
            nome = input("Insira o nome: ")
            if check_nome(nome):
                if pesquisa_aluno(nome):
                    print(f"Aluno {nome} encontrado!")
                    print("Nome: {} Email {} Curso {}".format(extrai_dados(nome)))
                else:
                    print("Aluno não encontrado")
            else:
                print("Verifique o nome!\n")
                continue
        elif opcao == "2":
            cadastra_aluno_interface()
        elif opcao == "3":
            listar_alunos()
        elif opcao == "4":
            print("Saindo...")
            break
        else:
            print("Por favor insira uma opcao valida!!")
            continue
        
opcoes()