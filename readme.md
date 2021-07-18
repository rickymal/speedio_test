# Atividade de DataOps

## Manual de uso

### Pré-requisito
- Para o uso da ferramenta, é preferível ter instalado em seu computador e configurado na variável de ambiente a plataforma Anaconda ou miniconda.
A instalação desta ferramenta assim como instruções pode ser feita aqui: [Site oficial do anaconda](https://www.anaconda.com/products/individual). Caso não queira instalar o Anaconda, apenas instale o Python e as seguintes bibliotecas: pymongo, pandas, requests, openpyxl. A versão Python testada foi a 3.9.5

- Também é necessário ter o git instalado em teu computador.


### Instalando e utilizando

- crie uma pasta para o download do projeto
- após a pasta ter sido criada, com o prompt de comando ou terminal na pasta, digite o seguinte comando
```bash
git clone https://github.com/rickymal/speedio_test.git
```
- em seguida digite
```bash
cd speedio_test
```
- Será necessário criar o ambiente. Digite o seguinte comando para ambiente windows 
```bash
conda env create -f dependencies.yml
```
ou
```bash
source conda env create -f dependencies.yml
```
- agora você deve ativar o ambiente
```bash
conda activate speedio
```
ou
```bash
source conda activate ./speedio
```
- Crie uma pasta com o nome 'data' e insira os dados da receita federal (descompactados)
- por último, para executar, basta digitar o comando abaixo
```bash
python main.py
```
ou
```
./main.py
```

Observação: os comandos para sistemas Linux e MacOS não foram testados

