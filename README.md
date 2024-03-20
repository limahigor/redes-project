
# Projeto de Redes de Computadores

Este projeto é uma aplicação que explora os conceitos fundamentais de sockets em Python, utilizando funções primitivas como `socket()`, `input()` e `print()`.

## Instalação

Para preparar e executar este projeto, siga as instruções abaixo.

### Requisitos

É necessário ter Python instalado em sua máquina.

### Configuração do Ambiente

Primeiro, crie um ambiente virtual para gerenciar as dependências do projeto:

```bash
python -m venv /reds
```

Ative o ambiente virtual. No Windows, execute:

```bash
/reds/Scripts/activate
```

No Unix ou MacOS, execute:

```bash
source /reds/bin/activate
```

### Instalação das Dependências

Com o ambiente virtual ativado, instale as dependências do projeto utilizando o seguinte comando:

```bash
pip install pygame
```

## Execução

Para executar o projeto, você precisará inicializar o servidor e, em seguida, executar duas instâncias do cliente.

1. Abra um terminal e navegue até o diretório do projeto.
2. Execute o servidor:

```bash
python server.py
```

3. Em dois novos terminais, execute o cliente duas vezes para iniciar duas instâncias:

```bash
python client.py
```

Siga as instruções na tela para interagir com a aplicação.

## Equipe do Projeto

| Nome                          | E-mail                |
| ----------------------------- | --------------------- |
| Rita de Kássia Lemos Pereira  | rklp@ic.ufal.br       |
| Higor de Lima Gomes           | hlg@ic.ufal.br        |
| Guilherme Oliveira Silva Gomes| gosg@ic.ufal.br       |
| José Anderson da Silva        | jandersons@ic.ufal.br |