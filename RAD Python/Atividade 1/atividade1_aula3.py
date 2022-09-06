#Q1
#Aluno: Mateus Brazil de Oliveira
#Matrícula: 202003447031

file = "crescente.txt"

#Cria um arquivo com o nome crescente.txt caso ele não exista
with open(file,"a"): pass

#Cria um arquivo com os numeros de 1 a 100
with open(file,"w") as f:
    for i in range(1,101,1):
        text = str(i) + "\n"
        f.write(text)
        

