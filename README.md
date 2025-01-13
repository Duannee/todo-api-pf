# *API de Gerenciamento de Tarefas (To-Do List)*
[![NPM](https://img.shields.io/npm/l/react)](https://github.com/Duannee/todo-api-pf/blob/main/LICENSE)

---

## **Index**

1. [Descrição](#descrição)  
2. [Tecnologias Utilizadas](#tecnologias-utilizadas)  
3. [Instalação e Configuração](#instalação-e-configuração)    
4. [Autenticação](#autenticação)   
5. [Endpoints](#endpoints)    
6. [Testes](#testes)  
7. [Linting e Formatação](#linting-e-formatação)
8. [Execução do Projeto](#execução-do-projeto)
9. [Contato](#contato)

---

## **Descrição**
Esta API foi desenvolvida utilizando FastAPI e permite o gerenciamento de tarefas (To-Do List). 
Ela fornece funcionalidades para criar, listar, atualizar, visualizar e deletar tarefas. 
Além disso, inclui autenticação via JWT e uma documentação interativa disponível no Swagger.

---

## **Tecnologias Utilizadas**
- *FastAPI* - Framework web para Python.
- *Poetry* - Gerenciador de dependências e ambiente virtual.
- *Pytest* - Framework para testes.
- *Ruff* - Linter para código Python.
- *Taskipy* - Ferramenta para simplificar a execução de comandos.

---

## **Instalação e Configuração**

1. Clone o repositório:

```
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>
```

2. Instale o Poetry caso não tenha:
```
pip install poetry
```

3. Instale as dependências:
   ```
   poetry install
   ```

4. Ative o ambiente virtual 
```
poetry shell
```


4. Execute a aplicação:
```
fastapi dev src/main.py
```

---

## *Autenticação*

A API utiliza JWT para autenticação. Para acessar as rotas protegidas:

1. Crie um usuário em /users/.

2. Faça login em /token/ e obtenha um token de acesso.

3. Utilize o token no header das requisições protegidas:
```
Authorization: Bearer <seu_token>
```

---

## *Endpoints*
- POST /users/ -> Cria um usuário
- POST /token/ -> Gera o token
- POST /tasks/ -> Cria uma tarefa
- GET /tasks/ -> Lista as tarefas
   - Filtro -> Filtra pelo status da tarefa.
- GET /tasks/{task_id} -> Visualiza uma tarefa específica pelo seu ID
- PATCH /tasks/{task_id} -> Atualiza uma tarefa existente
- DELETE /tasks/{task_id} -> Deleta uma tarefa

---

## *Testes*
Os testes são escritos utilizando pytest.
Para rodar os testes, execute:
```
task test
```

---

## *Linting e Formatação**
A API utiliza Ruff como linter e o taskipy para simplificar a execução de comandos. Para rodar a verificação:
```
task lint
```

Para formatar o código:
```
task format
```
## *Execução do Projeto*
```
task run
```

Essa documentação cobre todas as funcionalidades da API e como utilizá-la. Caso tenha dúvidas ou problemas, sinta-se à vontade para contribuir ou abrir uma issue no repositório!

## *Contato*
- Desenvolvedor: Duanne Moraes
- Email: duannemoraes.dev@gmail.com
- LinkedIn: [Duanne Moraes Linkedin](https://www.linkedin.com/in/duanne-moraes-7a0376278/)

















  




