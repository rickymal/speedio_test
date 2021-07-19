# Atividade de DataOps

## Manual de uso

### Pré-requisito
- Para o uso da ferramenta, é preferível ter instalado em teu computador e configurado na variável de ambiente a plataforma Anaconda ou miniconda.
A instalação desta ferramenta assim como instruções pode ser feita aqui: [Página de download do Anaconda](https://www.anaconda.com/products/individual) ou [Página de download do Miniconda](https://docs.conda.io/en/latest/miniconda.html). Caso não queira instalar o Anaconda ou miniconda, você pode utilizar o gerenciador de pacotes integrado do python sem problemas.

- Também é necessário ter o git instalado em teu computador.

Observação: os comandos para sistemas Linux e MacOS não foram testados

### Instalando e utilizando

- crie uma pasta para o download do projeto por uma questão de organização (opcional)
- após a pasta ter sido criada, com o prompt de comando ou terminal na pasta, digite o seguinte comando
```bash
git clone https://github.com/rickymal/speedio_test.git
```
- em seguida digite
```bash
cd speedio_test
```
- Crie uma pasta com o nome 'data' e insira os dados da receita federal (descompactados)
#### Apenas para os usuários do Anaconda e miniconda
- Será necessário criar o ambiente. Digite o seguinte comando para ambiente windows 
```bash
conda env create -f dependencies.yml
```
ou derivados do Unix
```bash
source conda env create -f dependencies.yml
```
- agora você deve ativar o ambiente
```bash
conda activate speedio
```
ou derivados do Unix
```bash
source conda activate ./speedio
```
#### Para usuários que contenham apenas o python
- Instale as seguinte dependências com o comando pip:
```bash
pip install pandas pymongo openpyxl
```
- O script foi testado com o python na versão 3.9.5


### Executando
- por último, para executar, basta digitar o comando abaixo
```bash
python main.py
```
ou derivados do Unix
```
./main.py
```



