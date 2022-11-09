## Trabalho AV2 RAD Python

# Como iniciar o programa

Para iniciar a aplicação basta executar o arquivo app.py. Certifique-se que as imagens estejam no mesmo path do arquivo e na pasta resources.

# Como conectar ao banco de dados

A versão utilizada foi a 12 do Postgres. 

Para que o programa funcione corretamente certifique-se que há uma tabela "alunos" no seu banco de dados.

Para conectar ao banco de dados vá na aba Config DB e insira as informações solicitadas. O campo IP não esta sendo utilizado, o ip padrão é o localhost. Caso queira conectar a um servidor externo basta editar as propriedades de conexão dentro da classe Config DB

Após inserir as informações solicitadas, clique em login. O status deverá ser atualizado para "Conectado"

As informações de login não são persistentes, ou seja, assim que fechar o programa na próxima execução elas deverão ser inseridas novamente.

**As demais páginas funcionam somente se a conexão for estabelecida, certifique-se de conectar-se antes ao BD**

# Como registrar um aluno

Para registrar um aluno no banco de dados vá até a pagina Registrar e insira os dados solicitados. Todos os campos são verificados, então nao aceitará caracteres especiais no nome e nem cpf inválido.
