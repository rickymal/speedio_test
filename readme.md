# Atividade de DataOps

## Manual de uso

### Pré-requisito
- Para o uso da ferramenta, é necessário ter instalado em seu computador e configurado na variável de ambiente a plataforma Anaconda.
A instalação desta ferramenta assim como instruções pode ser feita aqui: [Site oficial do anaconda](https://www.anaconda.com/)

- Também é necessário ter o git instalado em teu computador.


### Instalando e utilizando

- crie uma pasta para o download do projeto
- após a pasta ter sido criada, com o prompt de comando ou terminal na paste, digite o seguinte comando
```bash
git clone https://github.com/rickymal/speedio_test.git
```
- em seguida será necessário criar o ambiente. Digite o seguinte comando para ambiente windows 
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
- por último, para executar, basta digitar o comando abaixo
```bash
python main.py
```
ou
```
./main.py
```



