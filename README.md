# Search Engine project
Information retrieval search engine project.

# Functions
1. Standardize: Standardize url folders and files
2. Tokenizer: Tokenize information folders.
3. Build dictionary.

## Requirements
1. Install docker.
- [Docker](https://docs.docker.com/engine/installation/) 
2. Install git.
- [Git](https://gist.github.com/derhuerst/1b15ff4652a867391f03)

# How to run the proyect
1. Clone this project.
```
git clone https://github.com/fahernandez/search-engine
```
2. Execute 
```
cd search-engine
docker run -ti -v $PWD/src:/src -v $PWD/../search-engine-data:/data fahernandez/search-engine:latest
```

# Problems
Adrian Quiros no coincide los archivos con el orden del archivo de urls, no se pudo
Adrian Vargas no tiene el archivo de urls y los archivos tienen los nombres de urls, no se pudo
Carlos son puras imagenes y no tiene el archivo de urls, no se pudo
Daniel Herrera no se puede hacer unzip, no se pudo
Deivert los archivos tienen nombres de la url y no tiene el archivo url, no se pudo
Esteban Rodriguez no le puso extension a los archivos y se llama documents.csv, los pdf estan rotos, pero se pudo
Michelle no tiene el archivo url, no se pudo
Pablo no tiene el content type, hay archivos vacios, el 66, 2251, 2252 no existe, tiene archivos de codigo, pero se pudo


Gerardo Sierra: Corpus Linguistico
Weka