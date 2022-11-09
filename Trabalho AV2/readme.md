# Trabalho para a Matéria de RAD Desenvolvimento Rápido em Python 

## Como esta distribuido o código?

O código esta distribuido em 4 arquivos, cada um desses contém uma página do aplicativo. 

## Onde inciar o código.

Para iniciar o código basta executar o arquivo app.py, ele é a pagina principal e quem gerencia todos os outros frames.

## Como conectar ao banco de dados.

O BD utilizado é o POSTGRES versão 12. Para conectar ao banco de dados você primeiramente precisa ter uma tabela chamada alunos dentro do BD no qual você irá conectar, do contrário o programa irá retornar falha na conexão.

Para configurar o BD, inicie o programa e vá na aba "ConfigDB". Dentro desta aba você tera as opções Usuário,Senha,IP e Nome do DB.

O campo IP não esta sendo utilizado na interface, por padrão é o localhost, caso queira conectar a um servidor externo basta ir no código da página CONFIG DB e modificar os padróes de conexáo. 

O campo "Nome do DB" é onde você deverá inserir o nome do Banco de dados no qual você irá se conectar.

Após configurar todas os campos, exceto o "IP", basta clicar no botão de login e no Status deverá aparecer "Conectado"

Uma vez configurado o banco de dados na sessão do programa, você podera utilizar todas as outras funções normalmente. Lembrando que as informações de login não são persistentes, assim que o programa for finalizado todas as configurações de conexão deverão ser refeitas.


## Registro de alunos

Na tela de registro de alunos você deverá inserir os seguintes dados(Nome,CPF,Sexo,Curso e data de nascimento). Todos os campos passam por verifição, então só são aceitos CPF válidos (Que respeitam o padrão matemático de geração) e nomes que não contenham caracteres especiais.

## Procura de alunos

Na tela de procura de alunos, você pode selecionar alguns filtros para encontrar o aluno registrado no BD, tais como, CPF, NOME, MATRICULA e CURSO. Na implementação do código do banco de dados não foi separado o nome por nome e sobrenome e também não implementei uma função para encontrar nomes parecidos, então para encontrar um aluno pelo nome você deve digitar exatamente o nome como foi cadastrado
