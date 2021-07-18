# Atividade de DataOps

## Manual de uso

### Pré-requisito
- Para o uso da ferramenta, é necessário ter instalado em seu computador e configurado na variável de ambiente da Data Science Anaconda.
A instalação desta ferramenta assim como instruções pode ser feita aqui: [Site oficial do anaconda](https://www.anaconda.com/)

- Também é necessário ter o git instalado em teu computador.

```bash
# crie uma pasta para o download do projeto
# após a pasta ter sido criada, com o prompt de comando ou terminal na paste, digite o seguinte comando
$ git clone https://github.com/rickymal/speedio_test.git

# em seguida será necessário criar o ambiente. Digite o seguinte comando para ambiente windows 
$ conda env create -f dependencies.yml

# ou em sistemas Unix
$ source conda env create -f dependencies.yml

# agora você deve ativar o ambiente
$ conda activate speedio

# ou em sistemas Unix
$ source conda activate ./speedio

# por último, para executar, basta digitar o comando abaixo
$ python main.py

# ou em sistemas Unix
# ./main.py
```